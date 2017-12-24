# -*- coding: utf-8 -*-
"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Dec 10, 2015

@author: jrm
"""
from atom.api import Unicode
from declaracad.core.api import Plugin


class DocsPlugin(Plugin):

    #: List of tools or
    url = Unicode()

    #: Raw source to display
    source = Unicode()

    # -------------------------------------------------------------------------
    # Docs API
    # -------------------------------------------------------------------------
    def set_url(self, url):
        self.url, self.source = url, ""

    def set_source(self, source):
        self.url, self.source = "", source