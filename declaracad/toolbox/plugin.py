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
    item = Subclass(Atom)
    doc = Unicode()

    def _observe_name(self, change):
        from declaracad.occ import api
        self.item = getattr(api, self.name)
        self.doc = inspect.getdoc(self.item)


class ToolboxPlugin(Plugin):

    #: List of tools or
    tools = List(Tool)

    def _default_tools(self):
        from declaracad.occ import api
        return [Tool(name=it) for it in dir(api) if not it.startswith("_")]
