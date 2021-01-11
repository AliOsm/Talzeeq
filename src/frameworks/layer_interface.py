# Built-in imports.
import abc

from typing import List

# Third-party package imports.
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF


class LayerInterface(object, metaclass=abc.ABCMeta):
    BASIC_LAYER_IMAGE = QPolygonF([
        QPointF(-20, -20),
        QPointF(100, -20),
        QPointF(100, 20),
        QPointF(-100, 20),
        QPointF(-100, -20),
    ])

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'layer_name') and
            callable(subclass.layer_name) and
            hasattr(subclass, 'layer_image') and
            callable(subclass.layer_image) and
            hasattr(subclass, 'layer_definition') and
            callable(subclass.layer_definition) and
            hasattr(subclass, 'layer_connections') and
            callable(subclass.layer_connections) and
            hasattr(subclass, 'layer_config_dialog') and
            callable(subclass.layer_config_dialog) and
            hasattr(subclass, 'layer_dialog_accept') and
            callable(subclass.layer_dialog_accept) or
            NotImplemented
        )

    @abc.abstractmethod
    def layer_name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def layer_image(self) -> QPolygonF:
        raise NotImplementedError

    @abc.abstractmethod
    def layer_definition(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def layer_connections(self, parents: List['LayerInterface'], is_root: List[bool]) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def layer_config_dialog(self):
        raise NotImplementedError

    @abc.abstractmethod
    def layer_dialog_accept(self):
        raise NotImplementedError
