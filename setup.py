#!/usr/bin/env python
"""
Copyright (c) 2017, Jairus Martin.
Distributed under the terms of the GPL v3 License.
The full license is in the file COPYING.txt, distributed with this software.
Created on Dec 13, 2017
"""
from setuptools import setup, find_packages

setup(
    name='declaracad',
    version='0.1.',
    description='Parametric 3D modeling with enaml and OpenCascade',
    long_description=open('README.md').read(),
    author='CodeLV',
    author_email='frmdstryr@gmail.com',
    license=open('LICENSE').read(),
    url='https://github.com/codelv/declaracad',
    packages=find_packages(),
    install_requires=['enaml', 'jsonpickle', 'qtconsole', 'pyflakes',
                      'QScintilla', 'numpydoc', 'markdown'],
)