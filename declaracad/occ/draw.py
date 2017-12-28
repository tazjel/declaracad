"""
Created on Sep 27, 2016

@author: jrm
"""
from atom.api import (
    Bool, ContainerList, Float, Typed, ForwardTyped, observe
)
from enaml.core.declarative import d_

from .shape import ProxyShape, Shape
from OCC.TopoDS import TopoDS_Edge, TopoDS_Wire


class ProxyPoint(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Point)
    
    def set_position(self, position):
        raise NotImplementedError


class ProxyVertex(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Vertex)


class ProxyEdge(ProxyShape):
    declaration = ForwardTyped(lambda: Edge)


class ProxyLine(ProxyEdge):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Line)


class ProxySegment(ProxyEdge):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Segment)


class ProxyArc(ProxyEdge):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Arc)
    
    def set_radius(self, r):
        raise NotImplementedError
    
    def set_alpha1(self, a):
        raise NotImplementedError
    
    def set_alpha2(self, a):
        raise NotImplementedError
    

class ProxyCircle(ProxyEdge):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Circle)
    
    def set_radius(self, r):
        raise NotImplementedError


class ProxyEllipse(ProxyEdge):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Ellipse)
    
    def set_major_radius(self, r):
        raise NotImplementedError
    
    def set_minor_radius(self, r):
        raise NotImplementedError


class ProxyHyperbola(ProxyEdge):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Hyperbola)
    
    def set_major_radius(self, r):
        raise NotImplementedError
    
    def set_minor_radius(self, r):
        raise NotImplementedError


class ProxyParabola(ProxyEdge):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Parabola)
    
    def set_focal_length(self, l):
        raise NotImplementedError


class ProxyPolygon(ProxyEdge):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Polygon)
    
    def set_closed(self, closed):
        raise NotImplementedError


class ProxyWire(ProxyShape):
    declaration = ForwardTyped(lambda: Wire)


class Point(Shape):
    """ A Point at a specific position.
    
    Examples
    --------
    
    Point:
        position = (10, 100, 0)
    
    """
    proxy = Typed(ProxyPoint)


class Vertex(Shape):
    """ A Vertex at a specific position.
    
    Examples
    --------
    
    Vertex:
        position = (10, 100, 0)
    
    """
    proxy = Typed(ProxyVertex)


class Edge(Shape):
    """ An Edge is a base class for Lines and Wires.
    
    """
    proxy = Typed(ProxyEdge)


class Line(Edge):
    """ Creates a Line passing through the position and parallel to vector 
    given by the direction.
    
    Attributes
    ----------
        position: Tuple
            The position of the line.
        direction: Tuple
            The direction of the line.
             
    Examples
    --------
    
    Line:
        position = (10, 10, 10)
        direction = (0, 0, 1)
    
    """
    proxy = Typed(ProxyLine)


class Segment(Line):
    """ Creates a line Segment from two child points. 
    
    Examples
    --------
    
    Segment:
        Point:
            position = (0, 0, 0)
        
        Point:
            position = (10, 0, 0)
    
    
    """
    proxy = Typed(ProxySegment)


class Arc(Line):
    """ Creates an Arc that can be used to build a Wire. 
    
    Attributes
    ----------
    
    radius: Float, optional
        The radius of the arc.
    alpha1: Float, optional
        The starting angle of the arc. 
    alpha2: Float, optional
        The ending angle of the arc. 
    
    Notes
    ------
    An arc can be constructed using:
    
    1. three child Points
    2. axis, radius, alpha 1, alpha 2
    3. axis, radius, and two child Points
    4. axis, radius, one child Point and alpha 1
     
    Examples
    ---------
    import math
    Wire:
        Arc: 
            attr deg = 5
            radius = 1
            alpha1 = math.radians(deg)
            alpha2 = math.radians(deg+2)
    Wire:
        Arc:
            Point:
                position = (1, 0, 0)
            Point:
                position = (2, 5, 0)
            Point:
                position = (3, 0, 0)
    
    """
    proxy = Typed(ProxyArc)
    
    #: Radius of the circle (optional)
    radius = d_(Float(0, strict=False)).tag(view=True)
    
    #: Angle circle (optional)
    alpha1 = d_(Float(0, strict=False)).tag(view=True)
    
    #: 2nd Angle circle (optional)
    alpha2 = d_(Float(0, strict=False)).tag(view=True)


class Circle(Edge):
    """ Creates a Circle.   
    
    Attributes
    ----------
    
    radius: Float
        The radius of the circle
    
    Examples
    --------
    
    Circle:
        radius = 5
        position = (0, 0, 10)
        direction = (1, 0, 0)
    
    """
    proxy = Typed(ProxyCircle)
    
    #: Radius of the circle
    radius = d_(Float(1, strict=False)).tag(view=True)
    
    @observe('radius')
    def _update_proxy(self, change):
        super(Circle, self)._update_proxy(change)


class Ellipse(Edge):
    """ Creates an Ellipse.
    
    Attributes
    ----------

    major_radius: Float
        The radius of the circle
    minor_radius: Float
        The second radius of the circle
    
    Examples
    --------
    
    Ellipse:
        major_radius = 5
        minor_radius = 7
    
    """
    proxy = Typed(ProxyEllipse)
    
    #: Radius of the ellipse
    major_radius = d_(Float(1, strict=False)).tag(view=True)
    
    #: Minor radius of the ellipse
    minor_radius = d_(Float(1, strict=False)).tag(view=True)
    
    @observe('major_radius', 'minor_radius')
    def _update_proxy(self, change):
        super(Ellipse, self)._update_proxy(change)


class Hyperbola(Edge):
    """ Creates a Hyperbola. 
    
    Attributes
    ----------

    major_radius: Float
        The major radius of the hyperbola
    minor_radius: Float
        The minor radius of the hyperbola
    
    Notes
    ------
    
    The hyperbola is positioned in the space by the coordinate system A2 such 
    that:

    - the origin of A2 is the center of the hyperbola,
    - the "X Direction" of A2 defines the major axis of the hyperbola, that is, 
        the major radius MajorRadius is measured along this axis, and
    - the "Y Direction" of A2 defines the minor axis of the hyperbola, that is, 
        the minor radius MinorRadius is measured along this axis.
    
    This class does not prevent the creation of a hyperbola where:
    - MajorAxis is equal to MinorAxis, or
    - MajorAxis is less than MinorAxis. Exceptions Standard_ConstructionError 
        if MajorAxis or MinorAxis is negative. 
    
    Raises ConstructionError if MajorRadius < 0.0 or MinorRadius < 0.0 Raised 
        if MajorRadius < 0.0 or MinorRadius < 0.0
    
    Examples
    --------
    
    Wire:
        Hyperbola:
            major_radius = 5
            minor_radius = 3
    
    """
    proxy = Typed(ProxyHyperbola)
    
    #: Major radius of the hyperbola
    major_radius = d_(Float(1, strict=False)).tag(view=True)
    
    #: Minor radius of the hyperbola
    minor_radius = d_(Float(1, strict=False)).tag(view=True)
    
    @observe('major_radius', 'minor_radius')
    def _update_proxy(self, change):
        super(Hyperbola, self)._update_proxy(change)


class Parabola(Edge):
    """ Creates a Parabola with its local coordinate system given by the
    `position` and `direction` and it's focal length `focal_length`.
     
    Attributes
    ----------
    
    focal_length: Float
        The focal length of the parabola.
    
    Notes
    -----
    The XDirection of A2 defines the axis of symmetry of the parabola. 
    The YDirection of A2 is parallel to the directrix of the parabola. 
    The Location point of A2 is the vertex of the parabola 
    Raises ConstructionError if Focal < 0.0 Raised if Focal < 0.0.
    
    Examples
    ---------
    
    Wire:
        Parabola:
            focal_length = 10
        
    
    """
    proxy = Typed(ProxyParabola)
    
    #: Focal length of the parabola
    focal_length = d_(Float(1, strict=False)).tag(view=True)
    
    @observe('focal_length')
    def _update_proxy(self, change):
        super(Parabola, self)._update_proxy(change)     


class Polygon(Edge):
    """ A Polygon that can be built from any number of points or vertices, 
    and consists of a sequence of connected rectilinear edges.
    
    Attributes
    ----------
    
    closed: Bool,
        Automatically close the polygon.
         
    Examples
    ---------
    
    Wire:
        Polygon:
            closed = True
            Looper:
                iterable = [(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)]
                Point:
                    position = loop_item
    
    
    """
    proxy = Typed(ProxyPolygon)
    
    #: Polygon is closed
    closed = d_(Bool(False)).tag(view=True)
    
    @observe('closed')
    def _update_proxy(self, change):
        super(Polygon, self)._update_proxy(change) 


class Wire(Shape):
    """ A Wire is a Path or series of Segment, Arcs, etc... All child items
    must be connected or an error will be thrown.
    
    Attributes
    ----------
    
    edges: List, optional
        Edges used to build the wire.  
         
    Examples
    ---------
    
    Wire:
        Polygon:
            closed = True
            Looper:
                iterable = [(0, 0, 0), (10, 0, 0), (10, 10, 0), (0, 10, 0)]
                Point:
                    position = loop_item
    
    
    """
    proxy = Typed(ProxyWire)
    
    #: Edges used to create this wire 
    edges = d_(ContainerList((TopoDS_Edge, TopoDS_Wire)))
    
    @observe('edges')
    def _update_proxy(self, change):
        super(Wire, self)._update_proxy(change)
