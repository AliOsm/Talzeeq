# Built-in imports.
from typing import List

# Third-party package imports.
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from coolname import generate_slug

# First-party package imports.
from frameworks.layer_interface import LayerInterface
from frameworks.Keras.designs.input_layer_ui import Ui_InputLayer


class InputLayer(LayerInterface):
    IS_INPUT_LAYER = True

    LAYER_DISPLAY_NAME = 'Input Layer'

    def __init__(self):
        self.object_name = generate_slug(2).replace('-', '_')

    def layer_name(self) -> str:
        return self.LAYER_DISPLAY_NAME

    def layer_image(self) -> QPolygonF:
        return self.BASIC_LAYER_IMAGE

    def layer_definition(self) -> str:
        return self.object_name

    def layer_connections(self, parents: List[LayerInterface], is_root: List[bool]) -> str:
        pass

    def layer_config_dialog(self):
        self.dense_layer_dialog = InputLayerDialog()
        ui = self.dense_layer_dialog.ui

        ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.layer_dialog_accept)

        ui.objectNameLineEdit.setText(self.object_name)

        self.dense_layer_dialog.exec_()

    def layer_dialog_accept(self):
        ui = self.dense_layer_dialog.ui

        self.object_name = ui.objectNameLineEdit.text()


class InputLayerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_InputLayer()
        self.ui.setupUi(self)
