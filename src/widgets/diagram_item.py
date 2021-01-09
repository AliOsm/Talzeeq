# Built-in imports.
from typing import List

# Third-party package imports.
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

# First-party package imports.
from frameworks.layer_interface import LayerInterface


class DiagramItem(QtWidgets.QGraphicsPolygonItem):
    def __init__(
        self,
        framework_layer: LayerInterface,
        context_menu: QtWidgets.QMenu,
        parent: QtWidgets.QWidget = None,
    ):
        super(DiagramItem, self).__init__(parent)

        self.arrows = list()
        self.framework_layer = framework_layer
        self.context_menu = context_menu
        self.polygon = self.framework_layer.layer_image()

        self.create_text_item()

        self.setPolygon(self.polygon)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)

    def create_text_item(self):
        self.textItem = QtWidgets.QGraphicsSimpleTextItem(self.framework_layer.layer_name(), self)
        rect = self.textItem.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.textItem.setPos(rect.topLeft())

    def get_arrows(self):
        return self.arrows

    def get_framework_layer(self):
        return self.framework_layer

    def add_arrow(self, arrow):
        self.arrows.append(arrow)

    def remove_arrow(self, arrow):
        try:
            self.arrows.remove(arrow)
        except ValueError:
            pass

    def remove_arrows(self):
        for arrow in self.arrows[:]:
            arrow.get_start_item().remove_arrow(arrow)
            arrow.get_end_item().remove_arrow(arrow)
            self.scene().removeItem(arrow)

    def mouseDoubleClickEvent(self, event):
        self.framework_layer.layer_config_dialog()

    def contextMenuEvent(self, event: QtWidgets.QGraphicsSceneContextMenuEvent):
        self.scene().clearSelection()
        self.setSelected(True)
        self.context_menu.exec_(event.screenPos())

    def itemChange(self, change: int, value: int) -> int:
        if change == QtWidgets.QGraphicsItem.ItemPositionChange:
            for arrow in self.arrows:
                arrow.updatePosition()

        return value
