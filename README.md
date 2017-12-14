# declaracad

A declarative parametric 3D modeling program built using [OpenCascade](https://github.com/tpaviot/pythonocc-core)
and [enaml](https://github.com/nucleic/enaml/). 

[![Declaracad preview](https://img.youtube.com/vi/SeVcerBlpWE/0.jpg)](https://youtu.be/SeVcerBlpWE)

It's similar to [OpenSCAD](http://www.openscad.org/)
in that everything is intended to be defined programatically. However the 
language being used is enaml (a superset of python) instead of javascript.  Python users/developers will find this very easy and intuitive.



See [the project site](https://www.codelv.com/projects/declaracad/) (coming soon).


## Features

Currently the following 3D features can be used:

1. Basic shapes (Box, Sphere, Cylinder, Wedge, Torus) see [shapes](declaracad/occ/shape.py)
2. Boolean operations (Cut, Fuse, Common) see [algo](declaracad/occ/algo.py)
3. Fillet and chamfer edges see [algo](declaracad/occ/algo.py)
4. Drawing of wires and faces see [draw](declaracad/occ/draw.py)
4. Pipes [algo](declaracad/occ/algo.py)
5. LinearForm, RevolutionForm [algo](declaracad/occ/algo.py)
5. ThickSolid, ThroughSections [algo](declaracad/occ/algo.py)

See the [examples](examples) and the [occ](declaracad/occ/) package.


## Example

This is generates a turners cube of a given number of levels.

```python

from enaml.core.api import Looper
from declaracad.occ.shape import Box, Sphere
from declaracad.occ.algo import Cut
from declaracad.occ.part import Part

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

#: Run 
python main.py

```
