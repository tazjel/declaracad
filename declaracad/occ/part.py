"""
Created on Sep 28, 2016

@author: jrm
"""
from atom.api import (
    Typed, ForwardTyped, Unicode
)
from enaml.core.declarative import d_

from .shape import Shape, ProxyShape


class ProxyPart(ProxyShape):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: Part)
    
    def update_display(self, change):
        self.parent().update_display(change)

    
class Part(Shape):
    """ A Part is a compound shape. It may contain
    any number of nested parts and is typically subclassed.
    
    Attributes
    ----------
    name: String
        An optional name for the part
    description: String
        An optional description for the part
    
    Examples
    --------
    
    enamldef Case(Part):
        TopCover:
            # etc..
        BottomCover:
            # etc..
    
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyPart)
    
    #: Optional name of the part
    name = d_(Unicode())
    
    #: Optional description of the part
    description = d_(Unicode())
    
    @property
    def shapes(self):
        return [child for child in self.children if isinstance(child, Shape)]
