"""
Created on Dec 13, 2017

@author: jrm
"""
from enaml.qt.qt_factories import QT_FACTORIES


def occ_viewer_factory():
    from .qt_occ_viewer import QtOccViewer
    return QtOccViewer


QT_FACTORIES.update({
    'OccViewer': occ_viewer_factory,
})
