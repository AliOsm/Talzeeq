# Built-in imports.
import math

# Third-party package imports.
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

# First-party package imports.
from widgets.diagram_item import DiagramItem


class Arrow(QtWidgets.QGraphicsLineItem):
    def __init__(
        self,
        start_item: DiagramItem,
        end_item: DiagramItem,
        parent: QtWidgets.QWidget = None,
        scene: QtWidgets.QWidget = None,
    ):
        super(Arrow, self).__init__()

        self.start_item = start_item
        self.end_item = end_item
        self.arrow_head = QtGui.QPolygonF()

        # Could be used later to support coloring.
        self.color = Qt.black

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setPen(QtGui.QPen(
            self.color,
            2,
            Qt.SolidLine,
            Qt.RoundCap,
            Qt.RoundJoin,
        ))

    def get_start_item(self) -> DiagramItem:
        return self.start_item

    def get_end_item(self) -> DiagramItem:
        return self.end_item

    def boundingRect(self) -> QtCore.QRectF:
        extra = (self.pen().width() + 20) / 2.0
        p1 = self.line().p1()
        p2 = self.line().p2()
        return (
            QtCore.QRectF(p1, QtCore.QSizeF(p2.x() - p1.x(), p2.y() - p1.y()))
            .normalized()
            .adjusted(-extra, -extra, extra, extra)
        )

    def shape(self):
        path = super(Arrow, self).shape()
        path.addPolygon(self.arrow_head)
        return path

    def updatePosition(self):
        line = QtCore.QLineF(self.mapFromItem(self.start_item, 0, 0), self.mapFromItem(self.end_item, 0, 0))
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

        center_line = QtCore.QLineF(start_item.pos(), end_item.pos())
        end_polygon = end_item.polygon
        p1 = end_polygon.first() + end_item.pos()

        intersect_point = QtCore.QPointF()
        for i in end_polygon:
            p2 = i + end_item.pos()
            poly_line = QtCore.QLineF(p1, p2)
            intersect_type = poly_line.intersect(center_line, intersect_point)
            if intersect_type == QtCore.QLineF.BoundedIntersection:
                break
            p1 = p2

        self.setLine(QtCore.QLineF(intersect_point, start_item.pos()))
        line = self.line()

        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = (math.pi * 2.0) - angle

        arrow_p1 = (
            line.p1() +
            QtCore.QPointF(
                math.sin(angle + math.pi / 3.0) * arrow_size,
                math.cos(angle + math.pi / 3.0) * arrow_size,
            )
        )

        arrow_p2 = (
            line.p1() +
            QtCore.QPointF(
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
            painter.setPen(QtGui.QPen(color, 1, Qt.DashLine))
            line = QtCore.QLineF(line)
            line.translate(0, 4.0)
            painter.drawLine(line)
            line.translate(0,-8.0)
            painter.drawLine(line)
