# -*- coding: utf-8 -*-
"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Dec 10, 2015

@author: jrm
"""
import os
import re
import jedi
import enaml
import traceback
from atom.api import (
    Enum, ContainerList, Unicode, Tuple, Bool, List, Int, Instance, observe
)

from declaracad.core.api import Plugin, Model, log
from enaml.scintilla.themes import THEMES
from enaml.application import timed_call
from enaml.core.enaml_compiler import EnamlCompiler
from enaml.core.parser import parse
from enaml.layout.api import InsertTab, RemoveItem
from types import ModuleType
from future.utils import exec_
from glob import glob
from . import inspection


def EditorDockItem(*args, **kwargs):
    with enaml.imports():
        from .view import EditorDockItem
    return EditorDockItem(*args, **kwargs)


class Document(Model):
    #: Name of the current document
    name = Unicode().tag(config=True)

    #: Source code
    source = Unicode()
    cursor = Tuple(default=(0, 0))

    #: Any unsaved changes
    unsaved = Bool(True).tag(config=True)

    #: Any linting errors
    errors = List().tag(config=True)

    #: Any autocomplete suggestions
    suggestions = List().tag(config=True)

    #: Checker instance
    checker = Instance(inspection.Checker)

    def _default_source(self):
        """ Load the document from the path given by `name`.
        If it fails to load, nothing will be returned and an error
        will be set.
        """
        try:
            print("Loading '{}' from disk.".format(self.name))
            with open(self.name) as f:
                return f.read()
        except Exception as e:
            self.errors = [str(e)]
        return ""

    def _observe_source(self, change):
        self._update_errors(change)
        self._update_suggestions(change)
        if change['type'] == 'update':
            try:
                with open(self.name) as f:
                    self.unsaved = f.read() != self.source
            except:
                pass

    def _update_errors(self, change):
        """ Parse the source and try to detect any errors
         
        """
        if self.errors and change['type'] == 'create':
            #: Don't squash load errors
            return
        checker, reporter = inspection.run(self.source, self.name)
        warnings = [l for l in reporter._stdout.getvalue().split("\n") if l]
        errors = [l for l in reporter._stderr.getvalue().split("\n") if l]

        #: Ignore for enaml
        #if os.path.splitext(self.name)[-1] == '.enaml':
        #    errors = []

        self.errors = warnings + errors
        self.checker = checker

    def _update_suggestions(self, change):
        """ Determine code completion suggestions for the current cursor
        position in the document.
        """
        from declaracad.core.workbench import DeclaracadWorkbench
        workbench = DeclaracadWorkbench.instance()
        plugin = workbench.get_plugin('declaracad.editor')
        self.suggestions = plugin.autocomplete(self.source, self.cursor)


class EditorPlugin(Plugin):
    #: Opened files
    documents = ContainerList(Document).tag(config=True)
    active_document = Instance(Document, ()).tag(config=True)
    last_path = Unicode(os.path.expanduser('~/')).tag(config=True)
    project_path = Unicode(os.path.expanduser('~/')).tag(config=True)

    #: Editor settings
    theme = Enum('friendly', *THEMES.keys()).tag(config=True)
    zoom = Int(0).tag(config=True)  #: Relative to default

    #: Editor sys path
    sys_path = List().tag(config=True)
    _area_saves_pending = Int()

    # -------------------------------------------------------------------------
    # Editor API
    # -------------------------------------------------------------------------
    @observe('documents')
    def _update_area_layout(self, change):
        """ When a document is opened or closed, add or remove it
        from the currently active TabLayout.
        
        The layout update is deferred so it fires after the items are
        updated by the Looper.
        
        """
        if change['type'] == 'create':
            return

        #: Get the dock area
        area = self.get_dock_area()

        #: Refresh the dock items
        #area.looper.iterable = self.documents[:]

        #: Determine what change to apply
        removed = set()
        added = set()
        if change['type'] == 'container':
            op = change['operation']
            if op in ['append', 'insert']:
                added = set([change['item']])
            elif op == 'extend':
                added = set(change['items'])
            elif op in ['pop', 'remove']:
                removed = set([change['item']])
        elif change['type'] == 'update':
            old = set(change['oldvalue'])
            new = set(change['value'])

            #: Determine which changed
            removed = old.difference(new)
            added = new.difference(old)

        #: Update operations to apply
        ops = []

        #: Remove any old items
        for doc in removed:
            ops.append(RemoveItem(
                item='editor-item-{}'.format(doc.name)
            ))

        #: Add any new items
        for doc in added:
            targets = ['editor-item-{}'.format(d.name) for d in self.documents
                       if d.name != doc.name]
            item = EditorDockItem(area, plugin=self, doc=doc)
            ops.append(InsertTab(
                item=item.name,
                target=targets[0] if targets else ''
            ))

        #: Now apply all layout update operations
        print("Updating dock area: {}".format(ops))
        area.update_layout(ops)
        self.save_dock_area(change)

    def save_dock_area(self, change):
        """ Save the dock area """
        self._area_saves_pending += 1

        def do_save():
            self._area_saves_pending -= 1
            if self._area_saves_pending != 0:
                return
            #: Now save it
            ui = self.workbench.get_plugin('enaml.workbench.ui')
            ui.workspace.save_area()
        timed_call(350, do_save)

    def get_dock_area(self):
        ui = self.workbench.get_plugin('enaml.workbench.ui')
        return ui.workspace.content.find('dock_area')

    def get_editor(self):
        """ Get the editor item for the currently active document 
        
        """
        item = 'editor-item-{}'.format(self.active_document.name)
        dock_item = self.get_dock_area().find(item)
        if not dock_item:
            return None
        return dock_item.children[0].editor

    # -------------------------------------------------------------------------
    # Document API
    # -------------------------------------------------------------------------
    def _default_documents(self):
        return [Document()]

    def _default_active_document(self):
        if not self.documents:
            self.documents = self._default_documents()
        return self.documents[0]

    def new_file(self, event):
        """ Create a new file with the given path
        
        """
        path = event.parameters.get('path')
        if not path:
            return
        doc = Document(name=os.path.join(self.project_path, path))
        self.documents.append(doc)
        self.active_document = doc

    def close_file(self, event):
        """ Close the file with the given path and remove it from
        the document list. If multiple documents with the same file
        are open this only closes the first one it finds.
        
        """
        path = event.parameters.get('path', self.active_document.name)
        docs = self.documents
        opened = [d for d in docs if d.name == path]
        if not opened:
            return
        print("Closing '{}'".format(path))
        doc = opened[0]
        self.documents.remove(doc)

        #: If we closed the active document
        if self.active_document == doc:
            self.active_document = docs[0] if docs else Document()

    def open_file(self, event):
        """ Open a file from the local filesystem 
        
        """
        path = event.parameters['path']

        #: Check if the document is already open
        for doc in self.documents:
            if doc.name == path:
                self.active_document = doc
                return
        print("Opening '{}'".format(path))

        #: Otherwise open it
        doc = Document(name=path, unsaved=False)
        with open(path) as f:
            doc.source = f.read()
        self.documents.append(doc)
        self.active_document = doc
        editor = self.get_editor()
        if editor:
            editor.set_text(doc.source)

    def save_file(self, event):
        """ Save the currently active document to disk
        
        """
        doc = self.active_document
        assert doc.name, "Can't save a document without a name"
        file_dir = os.path.dirname(doc.name)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        with open(doc.name, 'w') as f:
            f.write(doc.source)
        doc.unsaved = False

    def save_file_as(self, event):
        """ Save the currently active document as the given name
        overwriting and creating the directory path if necessary.
        
        """
        doc = self.active_document
        path = event.parameters['path']

        if not doc.name:
            doc.name = path
            doc.unsaved = False

        doc_dir = os.path.dirname(path)
        if not os.path.exists(doc_dir):
            os.makedirs(doc_dir)

        with open(path, 'w') as f:
            f.write(doc.source)

    @observe('active_document', 'active_document.source')
    def refresh_view(self, change):
        """ Refresh the compiled view object.
    
        This method will (re)compile the view for the given view text
        and update the 'compiled_view' attribute. If a compiled model
        is available and the view has a member named 'model', the model
        will be applied to the view.
    
        """
        viewer = self.workbench.get_plugin('declaracad.viewer')
        doc = self.active_document
        try:
            ast = parse(doc.source, filename=doc.name)
            code = EnamlCompiler.compile(ast, doc.name)
            module = ModuleType('__main__')
            module.__file__ = doc.name
            namespace = module.__dict__
            with enaml.imports():
                exec_(code, namespace)
            assembly = namespace.get('Assembly', lambda: None)()
            viewer.parts = [assembly] if assembly else []
        except Exception as e:
            errors = doc.errors[:]
            log.warning(traceback.format_exc())
            tb = traceback.format_exc().strip().split("\n")
            print(tb[-3])
            m = re.search(r'File "(.+)", line (\d+),', tb[-3])
            if m:
                errors.append("{}:{}: {}".format(m.group(1), m.group(2),
                                                tb[-1]))
            doc.errors = errors
            viewer.parts = []

    # -------------------------------------------------------------------------
    # Code inspection API
    # -------------------------------------------------------------------------
    def _default_sys_path(self):
        """ Determine the sys path"""
        return [self.project_path]

    @observe('project_path')
    def _refresh_sys_path(self, change):
        if change['type'] == 'update':
            self.sys_path = self._default_sys_path()

    def autocomplete(self, source, cursor):
        """ Return a list of autocomplete suggestions for the given text.
        Results are based on the modules loaded.
        
        Parameters
        ----------
            source: str
                Source code to autocomplete
            cursor: (line, column)
                Position of the editor
        Return
        ------
            result: list
                List of autocompletion strings
        """
        try:
            #: Use jedi to get suggestions
            line, column = cursor
            script = jedi.Script(source, line+1, column,
                                 sys_path=self.sys_path)

            #: Get suggestions
            results = []
            for c in script.completions():
                results.append(c.name)

                #: Try to get a signature if the docstring matches
                #: something Scintilla will use (ex "func(..." or "Class(...")
                #: Scintilla ignores docstrings without a comma in the args
                if c.type in ['function', 'class', 'instance']:
                    docstring = c.docstring()

                    #: Remove self arg
                    docstring = docstring.replace("(self,", "(")

                    if docstring.startswith("{}(".format(c.name)):
                        results.append(docstring)
                        continue

            return results
        except Exception:
            #: Autocompletion may fail for random reasons so catch all errors
            #: as we don't want the editor to exit because of this
            return []

