# Built-in imports.
import math

# Third-party package imports.
from PyQt5.QtCore import Qt, QLineF, QPointF, QRectF, QSizeF
from PyQt5.QtGui import QPen, QPolygonF
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsLineItem, QWidget

# First-party package imports.
from widgets.diagram_item import DiagramItem


class Arrow(QGraphicsLineItem):
    def __init__(
        self,
        start_item: DiagramItem,
        end_item: DiagramItem,
        parent: QGraphicsItem = None,
        scene: QGraphicsScene = None,
    ):
        super(Arrow, self).__init__()

        self.start_item = start_item
        self.end_item = end_item
        self.arrow_head = QPolygonF()

        # Could be used later to support coloring.
        self.color = Qt.black

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setPen(QPen(self.color, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

    def get_start_item(self) -> DiagramItem:
        return self.start_item

    def get_end_item(self) -> DiagramItem:
        return self.end_item

    def boundingRect(self) -> QRectF:
        extra = (self.pen().width() + 20) / 2.0
        p1 = self.line().p1()
        p2 = self.line().p2()
        return (
            QRectF(p1, QSizeF(p2.x() - p1.x(), p2.y() - p1.y()))
            .normalized()
            .adjusted(-extra, -extra, extra, extra)
        )

    def shape(self):
        path = super(Arrow, self).shape()
        path.addPolygon(self.arrow_head)
        return path

    def updatePosition(self):
        line = QLineF(self.mapFromItem(self.start_item, 0, 0), self.mapFromItem(self.end_item, 0, 0))
        self.setLine(line)

    def paint(self, painter, option, widget=None):
        if self.start_item.collidesWithItem(self.end_item):
            return

        start_item = self.start_item
        end_item = self.end_item
        color = self.color
        pen = self.pen()
        pen.setColor(color)
        arrow_size = 10.0
        painter.setPen(pen)
        painter.setBrush(color)

        center_line = QLineF(start_item.pos(), end_item.pos())
        end_polygon = end_item.polygon
        p1 = end_polygon.first() + end_item.pos()

        intersect_point = QPointF()
        for i in end_polygon:
            p2 = i + end_item.pos()
            poly_line = QLineF(p1, p2)
            intersect_type = poly_line.intersect(center_line, intersect_point)
            if intersect_type == QLineF.BoundedIntersection:
                break
            p1 = p2

        self.setLine(QLineF(intersect_point, start_item.pos()))
        line = self.line()

        angle = math.acos(line.dx() / max(1, line.length()))
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrow_p1 = (
            line.p1() +
            QPointF(
                math.sin(angle + math.pi / 3.0) * arrow_size,
                math.cos(angle + math.pi / 3.0) * arrow_size,
            )
        )

        arrow_p2 = (
            line.p1() +
            QPointF(
                math.sin(angle + math.pi - math.pi / 3.0) * arrow_size,
                math.cos(angle + math.pi - math.pi / 3.0) * arrow_size,
            )
        )

        self.arrow_head.clear()
        for point in [line.p1(), arrow_p1, arrow_p2]:
            self.arrow_head.append(point)

        painter.drawLine(line)
        painter.drawPolygon(self.arrow_head)

        if self.isSelected():
            painter.setPen(QPen(color, 1, Qt.DashLine))
            line = QLineF(line)
            line.translate(0, 4.0)
            painter.drawLine(line)
            line.translate(0,-8.0)
            painter.drawLine(line)
