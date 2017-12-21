"""
Created on Sep 30, 2016

@author: jrm
"""
from atom.api import Typed
from ..part import ProxyPart
from .occ_shape import OccDependentShape, OccShape

from OCC.TopoDS import TopoDS_Compound
from OCC.BRep import BRep_Builder


class OccPart(OccDependentShape, ProxyPart):
    #: A reference to the toolkit shape created by the proxy.
    builder = Typed(BRep_Builder)

    #: The compound shape
    shape = Typed(TopoDS_Compound, ())
    
    @property
    def shapes(self):
        return [child for child in self.children()
                if isinstance(child, OccShape)]

    def update_shape(self, change):
        """ Create the toolkit shape for the proxy object.

        """
        builder = BRep_Builder()
        shape = self.shape
        builder.MakeCompound(shape)
        for s in self.shapes:
            builder.Add(shape, s.shape.Shape())
        self.builder = builder
