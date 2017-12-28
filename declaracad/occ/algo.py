"""
Created on Sep 28, 2016

@author: jrm
"""
from atom.api import (
    Instance, ForwardInstance, Typed, ForwardTyped, ContainerList, Enum, Float,
    Bool, Coerced, observe
)
from enaml.core.declarative import d_

from .shape import ProxyShape, Shape


def WireFactory():
    #: Deferred import of wire
    from .draw import Wire
    return Wire


class ProxyOperation(ProxyShape):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: Operation)


class ProxyBooleanOperation(ProxyOperation):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: BooleanOperation)
    
    def set_shape1(self, shape):
        raise NotImplementedError

    def set_shape2(self, shape):
        raise NotImplementedError
    
    def set_pave_filler(self, pave_filler):
        raise NotImplementedError
    
    def _do_operation(self, shape1, shape2):
        raise NotImplementedError


class ProxyCommon(ProxyBooleanOperation):
    declaration = ForwardTyped(lambda: Common)


class ProxyCut(ProxyBooleanOperation):
    declaration = ForwardTyped(lambda: Cut)


class ProxyFuse(ProxyBooleanOperation):
    declaration = ForwardTyped(lambda: Fuse)


class ProxyFillet(ProxyOperation):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: Fillet)
    
    def set_radius(self, r):
        raise NotImplementedError
    
    def set_edges(self, edges):
        raise NotImplementedError
    
    def set_shape(self, shape):
        raise NotImplementedError


class ProxyChamfer(ProxyOperation):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: Chamfer)
    
    def set_distance(self, d):
        raise NotImplementedError
    
    def set_distance2(self, d):
        raise NotImplementedError
    
    def set_edges(self, edges):
        raise NotImplementedError
    
    def set_faces(self, faces):
        raise NotImplementedError


class ProxyOffset(ProxyOperation):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: Offset)
    
    def set_offset(self, offset):
        raise NotImplementedError
    
    def set_offset_mode(self, mode):
        raise NotImplementedError
    
    def set_intersection(self, enabled):
        raise NotImplementedError
    
    def set_join_type(self, mode):
        raise NotImplementedError


class ProxyThickSolid(ProxyOffset):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: ThickSolid)
    
    def set_closing_faces(self, faces):
        raise NotImplementedError


class ProxyPipe(ProxyOffset):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: Pipe)
    
    def set_spline(self, spline):
        raise NotImplementedError
    
    def set_profile(self, profile):
        raise NotImplementedError
    
    def set_fill_mode(self, mode):
        raise NotImplementedError


class ProxyAbstractRibSlot(ProxyOperation):
    #: Abstract class 
    
    def set_shape(self, shape):
        raise NotImplementedError
    
    def set_contour(self, contour):
        raise NotImplementedError
    
    def set_plane(self, plane):
        raise NotImplementedError
    
    def set_fuse(self, fuse):
        raise NotImplementedError


class ProxyLinearForm(ProxyAbstractRibSlot):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: LinearForm)
    
    def set_direction(self, direction):
        raise NotImplementedError
    
    def set_direction1(self, direction):
        raise NotImplementedError

    def set_modify(self, modify):
        raise NotImplementedError


class ProxyRevolutionForm(ProxyAbstractRibSlot):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: RevolutionForm)
    
    def set_height1(self, direction):
        raise NotImplementedError
    
    def set_height2(self, direction):
        raise NotImplementedError
    
    def set_sliding(self, sliding):
        raise NotImplementedError


class ProxyThruSections(ProxyOperation):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: ThruSections)
    
    def set_solid(self, solid):
        raise NotImplementedError
    
    def set_ruled(self, ruled):
        raise NotImplementedError
    
    def set_precision(self, pres3d):
        raise NotImplementedError


class ProxyTransform(ProxyOperation):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: Transform)
    
    def set_shape(self, shape):
        raise NotImplementedError
    
    def set_mirror(self, axis):
        raise NotImplementedError
    
    def set_rotate(self, rotation):
        raise NotImplementedError
    
    def set_scale(self, scale):
        raise NotImplementedError
    
    def set_translate(self, translation):
        raise NotImplementedError


class Operation(Shape):
    """ Base class for Operations that are applied to other shapes.
    
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyOperation)
    
    def _update_proxy(self, change):
        if change['name'] == 'axis':
            dx, dy, dz = self.x, self.y, self.z
            if change.get('oldvalue'):
                old = change['oldvalue'].Location()
                dx -= old.X()
                dy -= old.Y()
                dz -= old.Z()
            for c in self.children:
                if isinstance(c, Shape):
                    c.position = (c.x+dx, c.y+dy, c.z+dz)
        else:
            super(Operation, self)._update_proxy(change)
        self.proxy.update_display(change)


class BooleanOperation(Operation):
    """ A base class for a boolean operation on two or more shapes.
    
    Attributes
    ----------
    
    shape1: Shape
        The first shape argument of the operation.
    shape2: Shape
        The second shape argument of the operation.
    
    """

    shape1 = d_(Instance(object))
    
    shape2 = d_(Instance(object))
    
    #: Optional pave filler
    pave_filler = d_(Instance(object))#BOPAlgo_PaveFiller))
    
    @observe('shape1', 'shape2', 'pave_filler')
    def _update_proxy(self, change):
        super(BooleanOperation, self)._update_proxy(change)
        
        
class Common(BooleanOperation):
    """ An operation that results in the intersection or common volume
    of the two shapes. This operation is repeated to give the intersection 
    all child shapes.

    Examples
    ----------
    
    Common:
        Box:
            pass
        Circle:
            radius = 2
        Torus:
            radius = 1
    
    
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyCommon)


class Cut(BooleanOperation):
    """ An operation that results in the subtraction of the second and 
    following shapes the first shape.  This operation is repeated for all 
    additional child shapes if more than two are given.

    Examples
    ----------
    
    Cut:
        Box:
            dx = 2
            dy = 2
            dz = 2
        Box:
            pass
        
        # etc...
    
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyCut)


class Fuse(BooleanOperation):
    """ An operation that results in the addition all of the child shapes. 
    
   Examples
   ----------
   
   Fuse:
       Box:
           pass
       Box:
           position = (1,0,0)
       
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyFuse)


class LocalOperation(Operation):
    """ A base class for operations on the edges of shapes. 
    
    """


class Fillet(LocalOperation):
    """ Applies fillet operation to the first child shape. 
    
    Attributes
    ----------
    
    shape: String
        The fillet shape type apply
    radius: Float
        Radius of the fillet. Must be less than the face width.
    edges: List of edges, optional
        List of edges to apply the operation to. If not given all edges will
        be used.  Used in conjunction with the `shape_edges` attribute. 
    
    Examples
    --------
    
    Fillet:
        #: Fillet the first 4 edges of the box (left side) 
        edges = [e for i, e in enumerate(box.shape_edges) if i < 4]
        radius = 0.1
        Box: box:
            pass
        
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyFillet)
    
    #: Fillet shape type
    shape = d_(Enum('rational', 'angular', 'polynomial')).tag(view=True,
                                                              group='Fillet')
    
    #: Radius of fillet
    radius = d_(Float(1, strict=False)).tag(view=True, group='Fillet')
    
    #: Edges to apply fillet to
    #: Leave blank to use all edges of the shape 
    edges = d_(ContainerList(object)).tag(view=True, group='Fillet')
    
    @observe('shape', 'radius', 'edges')
    def _update_proxy(self, change):
        super(Fillet, self)._update_proxy(change)


class Chamfer(LocalOperation):
    """ Applies Chamfer operation to the first child shape. 
   
    Attributes
    ----------
    
    distance: Float
       The distance of the chamfer to apply
    distance2: Float
       The second distance of the chamfer to apply
    edges: List of edges, optional
       List of edges to apply the operation to. If not given all edges will
       be used.  Used in conjunction with the `shape_edges` attribute.
    faces: List of faces, optional
       List of faces to apply the operation to. If not given, all faces will
       be used.  Used in conjunction with the `shape_edges` attribute. 
    
    Examples
    --------
    
    Chamfer:
        #: Fillet the top of the cylinder
        faces = [cyl.shape_faces[0]]
        distance = 0.2
        Cylinder: cyl:
           pass
       
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyChamfer)
    
    #: Distance of chamfer
    distance = d_(Float(1, strict=False)).tag(view=True, group='Chamfer')
    
    #: Second of chamfer (leave 0 if not used)
    distance2 = d_(Float(0, strict=False)).tag(view=True, group='Chamfer')
    
    #: Edges to apply chamfer to
    #: Leave blank to use all edges of the shape 
    edges = d_(ContainerList()).tag(view=True, group='Chamfer')

    #: Faces to apply the chamfer to
    faces = d_(ContainerList()).tag(view=True, group='Chamfer')
    
    @observe('distance', 'distance2', 'edges', 'faces')
    def _update_proxy(self, change):
        super(Chamfer, self)._update_proxy(change)


class Offset(Operation):
    """ An operation that create an Offset of the first child shape.
    
    Attributes
    ----------
    
    offset: Float
        The offset distance
    offset_mode: String
        Defines the construction type of parallels applied to the free edges 
        of the shape
    intersection: Bool
        Intersection specifies how the algorithm must work in order to limit 
        the parallels to two adjacent shapes
    join_type: String
        Defines how to fill the holes that may appear between parallels to 
        the two adjacent faces
    
        
    Examples
    --------
    
    See examples/operations.enaml
        
    """

    #: Reference to the implementation control
    proxy = Typed(ProxyOffset)
    
    #: Offset
    offset = d_(Float(1, strict=False)).tag(view=True, group='Offset')
    
    #: Offset mode
    offset_mode = d_(Enum('skin', 'pipe', 'recto_verso')).tag(view=True,
                                                              group='Offset')
    
    #: Intersection
    intersection = d_(Bool(False)).tag(view=True, group='Offset')
    
    #: Join type
    join_type = d_(Enum('arc', 'tangent', 'intersection')).tag(view=True,
                                                               group='Offset')
        
    @observe('offset', 'offset_mode', 'intersection', 'join_type')
    def _update_proxy(self, change):
        super(Offset, self)._update_proxy(change)


class ThickSolid(Offset):
    """ An operation that creates a hollowed out solid from shape.
    
    Attributes
    ----------
    
    closing_faces: List, optional
        List of faces that bound the solid.
        
    Examples
    --------
    
    ThickSolid:
        #: Creates an open box with a thickness of 0.1
        offset = 0.1
        Box: box1:
            position = (4,-4,0)
        # Get top face
        closing_faces << [sorted(box1.shape_faces,key=top_face)[0]] 
        
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyThickSolid)
    
    #: Closing faces
    closing_faces = d_(ContainerList()).tag(view=True, group='ThickSolid')
    
    @observe('closing_faces')
    def _update_proxy(self, change):
        super(ThickSolid, self)._update_proxy(change)


class Pipe(Operation):
    """ An operation that extrudes a profile along a spline, wire, or path.
    
    Attributes
    ----------
    
    spline: Edge or Wire
        The spline to extrude along.
    profile: Wire
        The profile to extrude.
    fill_mode: String, optional
        The fill mode to use.
    
        
    Examples
    --------
    
    See examples/pipes.enaml
        
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyPipe)
    
    #: Spline to make the pipe along
    spline = d_(Instance(Shape))
    
    #: Profile to make the pipe from
    profile = d_(ForwardInstance(WireFactory))
    
    #: Fill mode
    fill_mode = d_(Enum(None, 'corrected_frenet', 'fixed', 'frenet',
                        'constant_normal', 'darboux', 'guide_ac', 'guide_plan',
                        'guide_ac_contact', 'guide_plan_contact',
                        'discrete_trihedron')).tag(view=True, group='Pipe')
    
    @observe('spline', 'profile', 'fill_mode')
    def _update_proxy(self, change):
        super(Pipe, self)._update_proxy(change)


class AbstractRibSlot(Operation):
    #: Base shape
    shape = d_(Instance(Shape))
    
    #: Profile to make the pipe from
    contour = d_(Instance(Shape))
    
    #: Profile to make the pipe from
    plane = d_(Instance(Shape))
    
    #: Fuse (False to remove, True to add)
    fuse = d_(Bool(False)).tag(view=True)


class LinearForm(AbstractRibSlot):
    #: Reference to the implementation control
    proxy = Typed(ProxyLinearForm)
    
    #: Direction
    direction1 = d_(Instance((list, tuple))).tag(view=True)
    
    #: Modify
    modify = d_(Bool(False)).tag(view=True)


class RevolutionForm(AbstractRibSlot):
    #: Reference to the implementation control
    proxy = Typed(ProxyRevolutionForm)
    
    #: Height 1
    height1 = d_(Float(1.0, strict=False)).tag(view=True)
    
    #: Height 2
    height2 = d_(Float(1.0, strict=False)).tag(view=True)
    
    #: Sliding
    sliding = d_(Bool(False)).tag(view=True)
    
        
class ThruSections(Operation):
    """ An operation that extrudes a shape by means of going through a series
     of profile sections along a spline or path.  
    
    Attributes
    ----------
    
    solid: Bool
        If True, build a solid otherwise build a shell.
    ruled: Bool
        If False, smooth out the surfaces using approximation
    precision: Float, optional
        The precision to use for approximation.
        
    Examples
    --------
    
    See examples/thru_sections.enaml
        
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyThruSections)
    
    #: isSolid is set to true if the construction algorithm is required 
    #: to build a solid or to false if it is required to build a shell
    #: (the default value),
    solid = d_(Bool(False)).tag(view=True, group='Through Sections')
    
    #: ruled is set to true if the faces generated between the edges 
    #: of two consecutive wires are ruled surfaces or to false
    #: (the default value)
    #: if they are smoothed out by approximation
    ruled = d_(Bool(False)).tag(view=True, group='Through Sections')
    
    #: pres3d defines the precision criterion used by the approximation
    #:  algorithm;
    #: the default value is 1.0e-6. Use AddWire and AddVertex to define 
    #: the successive sections of the shell or solid to be built.
    precision = d_(Float(1e-6)).tag(view=True, group='Through Sections')
    
    @observe('solid', 'ruled', 'precision')
    def _update_proxy(self, change):
        super(ThruSections, self)._update_proxy(change)


class Transform(Operation):
    """ An operation that Transform's an existing shape (or a copy).
    
    Attributes
    ----------
    
    shape: Shape or None
        Shape to transform. If none is given it will use the first child. If
        given it will make a transformed copy the reference shape.
    mirror: Tuple or List
        Mirror transformation to apply to the shape. Should be a list for each
        axis (True, False, True).
    scale: Tuple or List
        Scale to apply to the shape. Should be a list of float values 
        for each axis ex. (2, 2, 2).
    rotate: Tuple or List
        Rotation to apply to the shape. Should be a list of float values 
        (in radians) for each axis ex. (0, math.pi/2, 0).
    translate: Tuple or List
        Translation to apply to the shape. Should be a list of float values 
        for each axis ex. (0, 0, 100).
        
    Examples
    --------
    
    Transform:
        rotate = (math.pi/4, 0, 0) 
        Box: box:
            pass
            
    #: Or
    Cylinder: cyl
        pass
    
    Transform:
        #: Create a copy and move it
        shape = cyl
        translate = (10, 20, 0)
        
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyTransform)
    
    #: Shape to transform
    #: if none is given the first child will be used
    shape = d_(Instance(Shape))
    
    #: Mirror
    mirror = d_(Instance((tuple, list)))
    
    #: Scale
    scale = d_(Instance((tuple, list)))
    
    #: Rotation
    rotate = d_(Instance((tuple, list)))
    
    #: Translation
    translate = d_(Instance((tuple,list)))
    
    @observe('shape', 'mirror', 'scale', 'rotate', 'translate')
    def _update_proxy(self, change):
        super(Transform, self)._update_proxy(change)
