# Built-in imports.
from typing import List

# Third-party package imports.
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from coolname import generate_slug

# First-party package imports.
from frameworks.layer_interface import LayerInterface
from frameworks.Keras.designs.dense_layer_ui import Ui_DenseLayer


class DenseLayer(LayerInterface):
    LAYER_DISPLAY_NAME                 = 'Dense Layer'
    LAYER_DEFINITION                   = '    self.{} = tf.keras.layers.Dense(units={}, activation={}, use_bias={})'
    ROOT_LAYER_CONNECTION_TEMPLATE     = '    self.{}_output = {}(self.{})'
    NON_ROOT_LAYER_CONNECTION_TEMPLATE = '    self.{}_output = {}(self.{})'

    def __init__(self):
        self.object_name = generate_slug(2).replace('-', '_')
        self.units       = 32
        self.activation  = 'linear'
        self.use_bias    = False

    def layer_name(self) -> str:
        return DenseLayer.LAYER_DISPLAY_NAME

    def layer_image(self) -> QPolygonF:
        return DenseLayer.BASIC_LAYER_IMAGE

    def layer_definition(self) -> str:
        return DenseLayer.LAYER_DEFINITION.format(
            self.object_name,
            self.units,
            self.activation,
            self.use_bias,
        )

    def layer_connections(self, parents: List[LayerInterface], is_root: List[bool]) -> str:
        layer_connections = list()

        for p, r in zip(parents, is_root):
            if r:
                layer_connections.append(DenseLayer.ROOT_LAYER_CONNECTION_TEMPLATE.format(
                    self.object_name,
                    self.object_name,
                    p.object_name,
                ))
            else:
                layer_connections.append(DenseLayer.NON_ROOT_LAYER_CONNECTION_TEMPLATE.format(
                    self.object_name,
                    self.object_name,
                    p.object_name,
                ))

        return '\n'.join(layer_connections)

    def layer_config_dialog(self):
        self.dense_layer_dialog = DenseLayerDialog()
        ui = self.dense_layer_dialog.ui

        ui.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.layer_dialog_accept)

        ui.objectNameLineEdit.setText(self.object_name)

        ui.unitsSpinBox.setValue(self.units)

        index = ui.activationComboBox.findText(self.activation, Qt.MatchFixedString)
        ui.activationComboBox.setCurrentIndex(index)

        ui.useBiasCheckBox.setChecked(self.use_bias)

        self.dense_layer_dialog.exec_()

    def layer_dialog_accept(self):
        ui = self.dense_layer_dialog.ui

        self.object_name = ui.objectNameLineEdit.text()
        self.units = ui.unitsSpinBox.value()
        self.activation = ui.activationComboBox.currentText()
        self.use_bias = ui.useBiasCheckBox.isChecked()


class DenseLayerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DenseLayer()
        self.ui.setupUi(self)
