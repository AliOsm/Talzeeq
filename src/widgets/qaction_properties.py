# Built-in imports.
from typing import Callable

# Third-party package imports.
from PyQt5.QtGui import QIcon


class QActionProperties(object):
    def __init__(self, name: str, icon: QIcon, text: str, shortcut: str, status_tip: str, triggered: Callable):
        self.name = name
        self.icon = icon
        self.text = text
        self.shortcut = shortcut
        self.status_tip = status_tip
        self.triggered = triggered
