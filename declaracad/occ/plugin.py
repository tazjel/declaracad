# -*- coding: utf-8 -*-
"""
Copyright (c) 2017, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on Dec 13, 2017

@author: jrm
"""
import os
from atom.api import List, Unicode, Float, Bool
from declaracad.core.api import Plugin, Model
from enaml.application import timed_call
from .part import Part

from OCC.TopoDS import TopoDS_Compound
from OCC.BRep import BRep_Builder

class ExportError(Exception):
    """ Raised if export failed """


class ExportOptions(Model):
    path = Unicode()
    linear_deflection = Float(0.05, strict=False)
    angular_deflection = Float(0.5, strict=False)
    relative = Bool()
    binary = Bool(False)


class ViewerPlugin(Plugin):
    #: List of parts to display
    parts = List(Part)

    def _observe_parts(self, change):
        """ When changed, do a fit all """
        if change['type'] == 'update':
            timed_call(500, self.fit_all)

    def fit_all(self, event=None):
        viewer = self.get_viewer()
        viewer.proxy.display.FitAll()

    def get_viewer(self):
        ui = self.workbench.get_plugin('enaml.workbench.ui')
        area = ui.workspace.content.find('dock_area')
        return area.find('viewer-item').viewer

    def export(self, event):
        """ Export the current model to stl """
        from OCC.StlAPI import StlAPI_Writer
        from OCC.BRepMesh import BRepMesh_IncrementalMesh
        #: TODO: All parts
        options = event.parameters.get('options')
        if not isinstance(options, ExportOptions):
            return False

        exporter = StlAPI_Writer()
        exporter.SetASCIIMode(not options.binary)

        #: Make a compound of compounds (if needed)
        compound = TopoDS_Compound()
        builder = BRep_Builder()
        builder.MakeCompound(compound)
        for part in self.parts:
            #: Must mesh the shape first
            if isinstance(part, Part):
                builder.Add(compound, part.proxy.shape)
            else:
                builder.Add(compound, part.proxy.shape.Shape())

        #: Build the mesh
        mesh = BRepMesh_IncrementalMesh(
            compound,
            options.linear_deflection,
            options.relative,
            options.angular_deflection
        )
        mesh.Perform()
        if not mesh.IsDone():
            raise ExportError("Failed to create the mesh")

        exporter.Write(compound, options.path)
