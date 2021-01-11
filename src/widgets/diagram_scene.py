# Third-party package imports.
from PyQt5.QtCore import Qt, QLineF, pyqtSignal
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsScene,
    QGraphicsSceneMouseEvent,
    QGraphicsSimpleTextItem,
    QMenu,
    QWidget,
)

# First-party package imports.
from utils import frameworks_utils
from widgets.arrow import Arrow
from widgets.diagram_item import DiagramItem


class DiagramScene(QGraphicsScene):
    insert_item, insert_line, move_item = range(3)

    item_inserted = pyqtSignal(DiagramItem)

    def __init__(self, context_menu: QMenu, parent: QGraphicsItem = None):
        super(DiagramScene, self).__init__(parent)

        self.context_menu = context_menu
        self.framework_name = frameworks_utils.get_sorted_frameworks_list()[0]
        self.mode = self.move_item
        self.item_type = None
        self.line = None

        # Could be used later to support items & lines coloring.
        self.item_color = Qt.white
        self.line_color = Qt.black

    def set_framework_name(self, framework_name: str):
        self.framework_name = framework_name

    def set_mode(self, mode: int):
        self.mode = mode

    def set_item_type(self, item_type: int):
        self.item_type = item_type

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() != Qt.LeftButton:
            return

        if self.mode == self.insert_item:
            layers = frameworks_utils.get_framework_layers(self.framework_name)
            item = DiagramItem(layers[self.item_type](), self.context_menu)
            item.setBrush(self.item_color)
            item.setPos(event.scenePos())
            self.addItem(item)
            self.item_inserted.emit(item)
        elif self.mode == self.insert_line:
            self.line = QGraphicsLineItem(QLineF(event.scenePos(), event.scenePos()))
            self.line.setPen(QPen(self.line_color, 2))
            self.addItem(self.line)

        super(DiagramScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self.mode == self.insert_line and self.line:
            new_line = QLineF(self.line.line().p1(), event.scenePos())
            self.line.setLine(new_line)
        elif self.mode == self.move_item:
            super(DiagramScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if self.mode == self.insert_line and self.line:
            start_items = self.items(self.line.line().p1())
            if len(start_items) and start_items[0] == self.line:
                start_items.pop(0)

            end_items = self.items(self.line.line().p2())
            if len(end_items) and end_items[0] == self.line:
                end_items.pop(0)

            self.removeItem(self.line)
            self.line = None

            if len(start_items) and isinstance(start_items[0], QGraphicsSimpleTextItem):
                start_items[0] = start_items[0].parentItem()

            if len(end_items) and isinstance(end_items[0], QGraphicsSimpleTextItem):
                end_items[0] = end_items[0].parentItem()

            if (
                len(start_items) and
                len(end_items) and
                isinstance(start_items[0], DiagramItem) and
                isinstance(end_items[0], DiagramItem) and
                start_items[0] != end_items[0]
            ):
                start_item = start_items[0]
                end_item = end_items[0]
                arrow = Arrow(start_item, end_item)
                start_item.add_arrow(arrow)
                end_item.add_arrow(arrow)
                arrow.setZValue(-1000.0)
                self.addItem(arrow)
                arrow.updatePosition()

        self.line = None
        super(DiagramScene, self).mouseReleaseEvent(event)

    def isItemChange(self, type_: DiagramItem):
        for item in self.selectedItems():
            if isinstance(item, type_):
                return True

        return False
