# declaracad

A declarative parametric 3D modeling program built using [OpenCascade](https://github.com/tpaviot/pythonocc-core)
and [enaml](https://github.com/nucleic/enaml/). 

[![Declaracad preview](https://img.youtube.com/vi/SeVcerBlpWE/0.jpg)](https://youtu.be/SeVcerBlpWE)

It's similar to [OpenSCAD](http://www.openscad.org/)
in that everything is intended to be defined programatically. However the 
language being used is enaml (a superset of python) instead of javascript.  
Python users/developers will find this very easy and intuitive.


See [the project site](https://www.codelv.com/projects/declaracad/) (coming soon).


## Features

Currently the following 3D features can be used:

1. Basic shapes (Box, Sphere, Cylinder, Wedge, Torus) see [shapes](declaracad/occ/shape.py)
2. Boolean operations (Cut, Fuse, Common) see [algo](declaracad/occ/algo.py)
3. Fillet and Chamfer edges see [algo](declaracad/occ/algo.py)
4. 2D Drawing of wires and faces see [draw](declaracad/occ/draw.py)
5. Pipes [algo](declaracad/occ/algo.py)
6. Extrude (Prism), LinearForm, RevolutionForm [algo](declaracad/occ/algo.py)
7. ThickSolid, ThroughSections [algo](declaracad/occ/algo.py)

See the [examples](examples) and the [occ](declaracad/occ/) package.

## Import / export


Currently there is no import support from other 3d types into editable code, 
but models can be loaded for display

![DeclaraCAD - loading models](https://user-images.githubusercontent.com/380158/34421112-4fcd664e-ebdb-11e7-8f75-ae7c2354dfa7.gif)

Importing 2D paths from SVG (ex Adobe Illustrator, Inkscape, etc..) is possible
 
![DeclaraCAD import from svg](https://user-images.githubusercontent.com/380158/34210286-5db22d4a-e563-11e7-9b86-6c2f5db73c96.gif)
    
Models can be exported to an stl file for imported into other programs (ex Simplify3D, FreeCAD, etc..)

![DeclaraCAD export to stl](https://user-images.githubusercontent.com/380158/34184975-d911c43c-e4f0-11e7-88ca-b52e6557ae83.gif)


## Example

This is generates a turners cube of a given number of levels.

```python

from enaml.core.api import Looper
from declaracad.occ.api import Box, Sphere, Cut, Part

enamldef TurnersCube(Part):
    name = "Turners Cube"

    attr levels: int = 3
    Looper:
        iterable << range(1,1+levels)
        Cut:
            Box:
                position = (-loop_item/2.0,-loop_item/2.0,-loop_item/2.0)
                dx = loop_item
                dy = loop_item
                dz = loop_item
            Sphere:
                radius = loop_item/1.5

```

## Docs

The goal is for the building blocks or components to be self documenting. 

It's partially there... suggestions are welcome!

![DeclaraCAD - Docs and Toolbox](https://user-images.githubusercontent.com/380158/34372327-d55d057a-eaa1-11e7-97dc-b95f97511f00.gif)

## Installing

There is currently no installer as it's in pre-alpha state. It runs on windows and linux 
(have not yet tested osx but it should also work). To use it:

```bash

#: Install conda or miniconda
#: See https://conda.io/miniconda.html

#: Create a conda env
conda create -n occ

#: Activate it
source activate occ

#: Install pythonocc
conda install -c conda-forge -c dlr-sc -c pythonocc -c oce pythonocc-core==0.18 python=3

#: Install enaml from repo (until some pending PR's are merged)
pip install git+https://github.com/frmdstryr/enaml.git@latest

#: Install enamlx
pip install git+https://github.com/frmdstryr/enamlx.git

#: Now install clone this repo
git clone https://github.com/codelv/declaracad.git

#: Go inside the cloned repo
cd declaracad

#: Install the dependencies
pip install .

#: Run 
python main.py

```


## License

The application is released under the GPL v3 (due to the use of PyQt5 and QScintilla). 
If you want to use this in your own application these can be replaced with alternatives if 
alternate licensing is needed. Please [contact](https://www.codelv.com/contact/) me for more 
details.

## Special thanks to

This project relies on the groundwork laid out by these projects: 

- [python-occ](https://github.com/tpaviot/pythonocc)
- [enaml](https://github.com/nucleic/enaml)

Please share your appreciation to them for all the hard work creating these projects!
