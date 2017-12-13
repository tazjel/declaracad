# -*- coding: utf-8 -*-
"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Dec 13, 2017

@author: jrm
"""
from atom.api import List
from declaracad.core.api import Plugin
from enaml.application import timed_call
from .part import Part


class ViewerPlugin(Plugin):
    #: List of parts to display
    parts = List(Part)

    def _observe_parts(self, change):
        """ When changed, do a fit all """
        if change['type'] == 'update':
            timed_call(500, self.fit_all)

    def fit_all(self):
        viewer = self.get_viewer()
        viewer.proxy.display.FitAll()

    def get_viewer(self):
        ui = self.workbench.get_plugin('enaml.workbench.ui')
        area = ui.workspace.content.find('dock_area')
        return area.find('viewer-item').viewer