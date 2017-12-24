# -*- coding: utf-8 -*-
"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Dec 10, 2015

@author: jrm
"""
import inspect
from atom.api import Atom, Subclass, List, Unicode
from declaracad.core.api import Plugin, Model


class Tool(Model):
    name = Unicode()
    declaration = Subclass(Atom)
    proxy = Subclass(Atom)
    doc = Unicode()

    def _observe_name(self, change):
        from enaml.qt.qt_application import QtApplication
        app = QtApplication.instance()

        from declaracad.occ import api
        self.declaration = getattr(api, self.name)
        factory = app.resolver.factories.get(self.name)
        if factory:
            self.proxy = factory()
        self.doc = inspect.getdoc(self.declaration)


class ToolboxPlugin(Plugin):

    #: List of tools or
    tools = List(Tool)

    def _default_tools(self):
        from declaracad.occ import api
        return [Tool(name=it) for it in dir(api) if not it.startswith("_")]
