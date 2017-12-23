"""
Created on Sep 30, 2016

@author: jrm
"""
from atom.api import (
    Tuple, Instance, Bool, Str, Float, Property, Coerced, Typed, ForwardTyped, 
    Enum, observe
)

from contextlib import contextmanager
from enaml.core.declarative import d_
from enaml.widgets.control import ProxyControl
from enaml.widgets.toolkit_object import ToolkitObject

#: TODO: This breaks the proxy pattern
from OCC.gp import gp_Pnt,gp_Ax2, gp_Dir
from OCC.TopoDS import TopoDS_Face, TopoDS_Shell, TopoDS_Shape


class ProxyShape(ProxyControl):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: Shape)
    
    def set_position(self, position):
        pass
    
    def set_direction(self, direction):
        pass
    
    def set_axis(self, axis):
        raise NotImplementedError
    
    def set_color(self, color):
        pass
    
    def set_transparency(self, alpha):
        pass


class ProxyFace(ProxyShape):
    #: A reference to the Shape declaration.
    declaration = ForwardTyped(lambda: Face)


def coerce_axis(value):
    pos = gp_Pnt(*value[0])
    v = gp_Dir(*value[1])
    return gp_Ax2(pos, v)


class ProxyBox(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Box)
    
    def set_dx(self, dx):
        raise NotImplementedError
    
    def set_dy(self, dy):
        raise NotImplementedError
    
    def set_dz(self, dz):
        raise NotImplementedError


class ProxyCone(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Cone)
    
    def set_radius(self, r):
        raise NotImplementedError
    
    def set_radius2(self, r):
        raise NotImplementedError
    
    def set_height(self, height):
        raise NotImplementedError
    
    def set_angle(self, angle):
        raise NotImplementedError


class ProxyCylinder(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Cylinder)
    
    def set_radius(self, r):
        raise NotImplementedError
    
    def set_height(self, height):
        raise NotImplementedError
    
    def set_angle(self, angle):
        raise NotImplementedError


class ProxyHalfSpace(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: HalfSpace)
    
    def set_surface(self, surface):
        raise NotImplementedError


class ProxyPrism(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Prism)
    
    def set_shape(self, surface):
        raise NotImplementedError
    
    def set_vector(self, vector):
        raise NotImplementedError
    
    def set_infinite(self, infinite):
        raise NotImplementedError
    
    def set_copy(self, copy):
        raise NotImplementedError
    
    def set_canonize(self, canonize):
        raise NotImplementedError


class ProxySphere(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Sphere)
    
    def set_radius(self, r):
        raise NotImplementedError
    
    def set_angle(self, a):
        raise NotImplementedError
    
    def set_angle2(self, a):
        raise NotImplementedError
    
    def set_angle3(self, a):
        raise NotImplementedError


class ProxyTorus(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Torus)
    
    def set_radius(self, r):
        raise NotImplementedError
    
    def set_radius2(self, r):
        raise NotImplementedError
    
    def set_angle(self, a):
        raise NotImplementedError
    
    def set_angle2(self, a):
        raise NotImplementedError


class ProxyWedge(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Wedge)
    
    def set_dx(self, dx):
        raise NotImplementedError
    
    def set_dy(self, dy):
        raise NotImplementedError
    
    def set_dz(self, dz):
        raise NotImplementedError
    
    def set_itx(self, itx):
        raise NotImplementedError 


class ProxyRevol(ProxyShape):
    #: A reference to the shape declaration.
    declaration = ForwardTyped(lambda: Revol)
    
    def set_shape(self, shape):
        raise NotImplementedError
    
    def set_angle(self, angle):
        raise NotImplementedError
    
    def set_copy(self, copy):
        raise NotImplementedError


class Shape(ToolkitObject):
    """ Most basic shape component that can be displayed on the screen 
    and represented by the framework. 
    
    This shape's proxy holds an internal reference to the underlying shape 
    which can be accessed using `self.proxy.shape` if needed. The topology
    of the shape can be accessed using the `topology` attribute.
    
    Notes
    ------
    
    - A shape's position can be changed using the `position`, or `x`, `y`, and
    `z`..
    
    - The orientation of the cone can be changed using 
    the `direction` and `axis`.
    
    - The edges and faces of the shape (when applicable) can be accessed using
    the `shape_edges` and `shape_faces` attributes respectively.
    
    - The `color`, `transparency` and `material` can be set to change the 
    how the shape is rendered.
    
    
    """
    #: Reference to the implementation control
    proxy = Typed(ProxyShape)
    
    #: Tolerance
    tolerance = d_(Float(10**-6, strict=False))
    
    #: Color
    color = d_(Str()).tag(view=True, group='Display')

    #: Texture material
    material = d_(Enum(None, 'aluminium', 'brass', 'bronze', 'charcoal',
                       'chrome', 'copper', 'default', 'diamond', 'glass',
                       'gold', 'jade', 'metalized', 'neon_gnc', 'neon_phc',
                       'obsidian', 'pewter', 'plaster', 'plastic', 'satin',
                       'shiny_plastic', 'silver', 'steel', 'stone', 'water')
                  ).tag(view=True, group='Display')
    
    #: Transparency
    transparency = d_(Float(strict=False)).tag(view=True, group='Display')
    
    #: x position
    x = d_(Float(0, strict=False)).tag(view=True, group='Position')
    
    #: y position
    y = d_(Float(0, strict=False)).tag(view=True, group='Position')
    
    #: z position
    z = d_(Float(0, strict=False)).tag(view=True, group='Position')
    
    #: Position
    position = d_(Coerced(gp_Pnt, (0, 0, 0),
                          coercer=lambda args: gp_Pnt(*args)))
    
    #: Direction
    direction = d_(Coerced(gp_Dir, (0, 0, 1),
                           coercer=lambda args: gp_Dir(*args)))
    
    #: Axis
    axis = d_(Coerced(gp_Ax2, ((0, 0, 0), (0, 0, 1)), coercer=coerce_axis))
    
    def _get_edges(self):
        topo = self.proxy.topology
        if not topo:
            return []
        return [e for e in topo.edges()]
    
    #: Edges of this shape
    shape_edges = Property(lambda self: self._get_edges(), cached=True)
    
    def _get_faces(self):
        topo = self.proxy.topology
        if not topo:
            return []
        return [e for e in topo.faces()]
    
    #: Faces of this shape
    shape_faces = Property(lambda self: self._get_faces(), cached=True)

    def _get_shells(self):
        topo = self.proxy.topology
        if not topo:
            return []
        return [e for e in topo.shells()]

    #: Shells of this shape
    shape_shells = Property(lambda self: self._get_shells(), cached=True)
    
    #: Block change updates to prevent loops when updated synced properties
    _block_updates = Bool()

    @contextmanager
    def suppress_updates(self):
        self._block_updates = True
        try:
            yield
        finally:
            self._block_updates = False

    @observe('x', 'y', 'z')
    def _update_position(self, change):
        """ Keep position in sync with x,y,z """
        if change['type'] != 'update':
            return
        pt = gp_Pnt(self.x, self.y, self.z)
        if not pt.IsEqual(self.position, self.tolerance):
            self.position = pt 
        
    @observe('position')
    def _update_xyz(self, change):
        """ Keep x,y,z in sync with position """
        self.x, self.y, self.z = (self.position.X(), self.position.Y(),
                                  self.position.Z())
    
    @observe('position', 'direction')
    def _update_axis(self, change):
        """ Keep axis in sync with position and direction """
        if not self._block_updates:
            self.axis = self._default_axis()
    
    @observe('axis')
    def _update_state(self, change):
        """ Keep position and direction in sync with axis """
        with self.suppress_updates():
            self.position = self.axis.Location()
            self.direction = self.axis.Direction()

    def _default_axis(self):
        return gp_Ax2(self.position, self.direction)
    
    @observe('axis', 'color', 'transparency')
    def _update_proxy(self, change):
        super(Shape, self)._update_proxy(change)
        if self.proxy:
            self.proxy.update_display(change)
    
    @observe('proxy.shape')
    def _update_topo(self, change):
        """ Update the cached topology references when the shape changes. s"""
        for k in ['shape_edges', 'shape_faces', 'shape_shells']:
            self.get_member(k).reset(self)


class Face(Shape):
    """ A Face turns it's first child Wire into a surface. 
    
    Examples
    --------
    
    Add a Wire as a child 
        Face:
            Wire:
                # etc.. 
    
    """

    #: Reference to the implementation control
    proxy = Typed(ProxyFace)


class Box(Shape):
    """ A primitive Box shape.  
    
    Attributes
    ----------
        dx: Float
            Size or width of the box along the x-axis
        dy: Float
            Size or height of the box along the y-axis
        dz: Float
            Size or depth of the box along the z-axis  
    
    Examples
    --------
    
        Box:
            dx = 3  
            dy = 10
            # dx, dy, and dz are all 1 by default if omitted
    
    """
    #: Proxy shape
    proxy = Typed(ProxyBox)
    
    #: x size
    dx = d_(Float(1, strict=False)).tag(view=True)
    
    #: y size
    dy = d_(Float(1, strict=False)).tag(view=True)
    
    #: z size
    dz = d_(Float(1, strict=False)).tag(view=True)
    
    # TODO: Handle other constructors
    
    @observe('dx', 'dy', 'dz')
    def _update_proxy(self, change):
        super(Box, self)._update_proxy(change)


class Cone(Shape):
    """ A primitive Cone shape.
    
    Attributes
    ----------
        height: Float
            Height of the cone
        radius: Float
            Radius of the base of the cone
        radius2: Float
            Second radius of the base of the cone (to make it oval)  
        angle: 
            The angle to revolve (in radians) the base profile
            
    Examples
    --------

        Cone:
            height = 10
            radius = 5
            angle = math.pi/2
        
    """
    #: Proxy shape
    proxy = Typed(ProxyCone)
    
    #: Radius
    radius = d_(Float(1, strict=False)).tag(view=True)
    
    #: Radius 2 size
    radius2 = d_(Float(0, strict=False)).tag(view=True)
    
    #: Height
    height = d_(Float(1, strict=False)).tag(view=True)
    
    #: Angle
    angle = d_(Float(0, strict=False)).tag(view=True)
    
    @observe('radius', 'radius2', 'height', 'angle')
    def _update_proxy(self, change):
        super(Cone, self)._update_proxy(change)


class Cylinder(Shape):
    """ A primitive Cylinder shape.

    Attributes
    ----------
        height: Float
            Height of the cylinder
        radius: Float
            Radius of the base of the cylinder
        angle: 
            The angle to revolve (in radians) the base profile.
            
    Examples
    --------
    
        Cone:
            height = 10
            radius = 5
        
    """
    #: Proxy shape
    proxy = Typed(ProxyCylinder)
    
    #: Radius
    radius = d_(Float(1, strict=False)).tag(view=True)
    
    #: Height
    height = d_(Float(1, strict=False)).tag(view=True)
    
    #: Angle
    angle = d_(Float(0, strict=False)).tag(view=True)
    
    @observe('radius', 'height', 'angle')
    def _update_proxy(self, change):
        super(Cylinder, self)._update_proxy(change)


class HalfSpace(Shape):
    """ An infinite solid limited by a surface.

    Attributes
    ----------
        surface: Face or Shell
            Surface to divide
            
    Notes
    -----
     A half-space is an infinite solid, limited by a surface. It is built from 
     a face or a shell, which bounds it, and with a reference point, which 
     specifies the side of the surface where the matter of the half-space is 
     located. A half-space is a tool commonly used in topological operations 
     to cut another shape
            
    Examples
    --------
    
    #: TODO: This does not work
    
        Box: box:
            pass
        
        HalfSpace:
            shape = box.shape_faces[0]
            position = (1, 1, 1)
        
    """
    #: Proxy shape
    proxy = Typed(ProxyHalfSpace)
    
    #: Surface that is either a face or a Shell
    surface = d_(Instance((TopoDS_Face, TopoDS_Shell)))
                 
    @observe('surface')
    def _update_proxy(self, change):
        super(HalfSpace, self)._update_proxy(change)

        
class Prism(Shape):
    """ A Prism extrudes a Face into a solid or a Wire into a surface along 
    the given vector. 
    
    Notes
    -----
    The first child node will be used as the shape if none is given.

    Attributes
    ----------
        shape: Shape to extrude or None
            Reference to the shape to extrude.
        vector: Tuple of (x, y, z)
            The extrusion vector.
        infinite: Bool
            Whether to extrude an infinte distance along the given vector.
        copy: Bool
            Copy the surface before extruding
        canonize: Bool
            Attempt to canonize in simple shapes
   
            
    Examples
    --------
    
    Prism:
        Wire:
            Polygon:
                Looper:
                    iterable = [(0,5,0), (2,6,0),  (5,4,0), (0,5,0)]
                    Point:
                        position = loop_item
    
    
    """

    #: Proxy shape
    proxy = Typed(ProxyPrism)
    
    #: Shape to build prism from
    shape = d_(Instance(Shape)).tag(view=True)
    
    #: Vector to build prism from, ignored if infinite is true
    vector = d_(Tuple((float, int), default=(0, 0, 1))).tag(view=True)
    
    #: Infinite
    infinite = d_(Bool(False)).tag(view=True)
    
    #: Copy the surface
    copy = d_(Bool(False)).tag(view=True)
    
    #: Attempt to canonize
    canonize = d_(Bool(True)).tag(view=True)
    
    @observe('shape', 'vector', 'infinite', 'copy', 'canonize')
    def _update_proxy(self, change):
        super(Prism, self)._update_proxy(change)


class Sphere(Shape):
    """ A primitive Sphere shape. 
    
    Attributes
    ----------
        radius: Float
            Radius of the sphere
        angle: Float
            The angle to revolve (in radians) along the base profile.
        angle2: Float
            See notes
        angle3: Float
            See notes
    
    
    Notes
    --------
    Make a sphere of radius R. For all algorithms The resulting shape is 
    composed of:
    
    - a lateral spherical face
    - Two planar faces parallel to the plane z = 0 if the sphere is truncated 
      in the v parametric direction, or only one planar face if angle1 is 
      equal to -p/2 or if angle2 is equal to p/2 (these faces are circles in 
      case of a complete truncated sphere),
    - and in case of a portion of sphere, two planar faces to shut the shape.
      (in the planes u = 0 and u = angle).

            
    Examples
    --------
    
    Sphere:
        radius = 3
    
    Sphere:
        angle = math.pi/2
        
    
    """
    #: Proxy shape
    proxy = Typed(ProxySphere)
    
    #: Radius of sphere
    radius = d_(Float(1, strict=False)).tag(view=True)
    
    #: angle 1
    angle = d_(Float(0, strict=False)).tag(view=True)
    
    #: angle 2
    angle2 = d_(Float(0, strict=False)).tag(view=True)
    
    #: angle 3
    angle3 = d_(Float(0, strict=False)).tag(view=True)
    
    @observe('radius', 'angle', 'angle2', 'angle3')
    def _update_proxy(self, change):
        super(Sphere, self)._update_proxy(change)


class Torus(Shape):
    #: Proxy shape
    proxy = Typed(ProxyTorus) 
    
    #: Radius of sphere
    radius = d_(Float(1, strict=False)).tag(view=True)
    
    #: Radius 2
    radius2 = d_(Float(0, strict=False)).tag(view=True)
    
    #: angle 1
    angle = d_(Float(0, strict=False)).tag(view=True)
    
    #: angle 2
    angle2 = d_(Float(0, strict=False)).tag(view=True)
    
    @observe('radius', 'radius2', 'angle1', 'angle2')
    def _update_proxy(self, change):
        super(Torus, self)._update_proxy(change)


class Wedge(Shape):
    #: Proxy shape
    proxy = Typed(ProxyWedge)
    
    #: x size
    dx = d_(Float(1, strict=False)).tag(view=True)
    
    #: y size
    dy = d_(Float(1, strict=False)).tag(view=True)
    
    #: z size
    dz = d_(Float(1, strict=False)).tag(view=True)
    
    #: z size
    itx = d_(Float(0, strict=False)).tag(view=True)
    
    # TODO: Handle other constructors
    
    @observe('dx', 'dy', 'dz', 'itx')
    def _update_proxy(self, change):
        super(Wedge, self)._update_proxy(change)


class Revol(Shape):
    #: Proxy shape
    proxy = Typed(ProxyRevol)
    
    #: Shape to build prism from
    shape = d_(Instance(Shape)).tag(view=True)
    
    #: Angle to revolve
    angle = d_(Float(0, strict=False)).tag(view=True)
    
    #: Copy the surface
    copy = d_(Bool(False)).tag(view=True)
    
    @observe('shape', 'angle', 'copy')
    def _update_proxy(self, change):
        super(Revol, self)._update_proxy(change)
