# Third-party package imports.
from PyQt5 import QtCore
from PyQt5 import QtGui

# First-party package imports.
from frameworks.layer_interface import LayerInterface


class DenseLayer(LayerInterface):
    def layer_name(self) -> str:
        return 'Dense Layer'

    def layer_image(self) -> QtGui.QPolygonF:
        return QtGui.QPolygonF([
            QtCore.QPointF(-20, -20),
            QtCore.QPointF(100, -20),
            QtCore.QPointF(100, 20),
            QtCore.QPointF(-100, 20),
            QtCore.QPointF(-100, -20),
        ])
