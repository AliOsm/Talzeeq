# Third-party package imports.
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from coolname import generate_slug

# First-party package imports.
from frameworks.layer_interface import LayerInterface
from frameworks.Keras.dense_layer_ui import Ui_DenseLayer


class DenseLayer(LayerInterface):
    def __init__(self):
        self.object_name = generate_slug(2).replace('-', '_')
        self.units = 32
        self.activation = 'linear'
        self.use_bias = False

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

    def layer_definition(self) -> str:
        return ''.join([
            '    ',
            'self.{} = '.format(self.object_name),
            'tf.keras.layers.Dense(',
            'units={}, '.format(self.units),
            'activation={}, '.format(self.activation),
            'use_bias={}'.format(str(self.use_bias)),
            ')',
        ])

    def layer_connections(self, parents, is_root):
        layer_connections = list()

        for parent, is_root_ in zip(parents, is_root):
            if is_root_:
                layer_connections.append('    self.{}_output = {}(self.{})'.format(
                    self.object_name,
                    self.object_name,
                    parent.object_name,
                ))
            else:
                layer_connections.append('    self.{}_output = {}(self.{}_output)'.format(
                    self.object_name,
                    self.object_name,
                    parent.object_name,
                ))

        return '\n'.join(layer_connections)

    def layer_config_dialog(self):
        self.dense_layer_dialog = DenseLayerDialog()

        (
            self.dense_layer_dialog
                .ui
                .buttonBox
                .button(QtWidgets.QDialogButtonBox.Ok)
                .clicked
                .connect(self.layer_dialog_accept)
        )

        self.dense_layer_dialog.ui.objectNameLineEdit.setText(self.object_name)
        self.dense_layer_dialog.ui.unitsSpinBox.setValue(self.units)
        index = self.dense_layer_dialog.ui.activationComboBox.findText(self.activation, QtCore.Qt.MatchFixedString)
        self.dense_layer_dialog.ui.activationComboBox.setCurrentIndex(index)
        self.dense_layer_dialog.ui.useBiasCheckBox.setChecked(self.use_bias)

        self.dense_layer_dialog.exec_()

    def layer_dialog_accept(self):
        self.object_name = self.dense_layer_dialog.ui.objectNameLineEdit.text()
        self.units = self.dense_layer_dialog.ui.unitsSpinBox.value()
        self.activation = self.dense_layer_dialog.ui.activationComboBox.currentText()
        self.use_bias = self.dense_layer_dialog.ui.useBiasCheckBox.isChecked()


class DenseLayerDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DenseLayer()
        self.ui.setupUi(self)
