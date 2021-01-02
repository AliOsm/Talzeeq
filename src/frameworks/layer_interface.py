# Built-in imports.
import abc

# Third-party package imports.
from PyQt5 import QtGui


class LayerInterface(object, metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'layer_name') and
            callable(subclass.layer_name) and
            hasattr(subclass, 'layer_image') and
            callable(subclass.layer_image) or
            NotImplemented
        )

    @abc.abstractmethod
    def layer_name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def layer_image(self) -> QtGui.QPolygonF:
        raise NotImplementedError
