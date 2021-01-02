# Built-in imports.
from typing import List

# Third-party package imports.
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

# First-party package imports.
import resources_rc

from utils import frameworks_utils
from constants import main_window_constants
from widgets.diagram_scene import DiagramScene
from widgets.diagram_item import DiagramItem
from frameworks.layer_interface import LayerInterface


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.create_edit_diagram_actions()
        self.create_edit_menu()
        self.create_frameworks_toolbar()
        self.create_edit_diagram_toolbar()
        self.create_pointer_toolbar()
        self.create_diagram_scene_and_view()
        self.create_framework_toolbox()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.framework_toolbox)
        self.layout.addWidget(self.view)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)

        self.setWindowTitle(main_window_constants.MAIN_WINDOW_TITLE)
        self.setCentralWidget(self.widget)

    # Create methods.
    def create_edit_diagram_actions(self):
        self.delete_action = QtWidgets.QAction(
            QtGui.QIcon(':/icons/delete'),
            '&Delete',
            self,
            shortcut='Delete',
            statusTip='Delete item from diagram',
            triggered=self.delete_item,
        )

        self.to_front_action = QtWidgets.QAction(
            QtGui.QIcon(':/icons/bring_to_front'),
            'Bring to &Front',
            self,
            shortcut='Ctrl+F',
            statusTip='Bring item to front',
            triggered=self.bring_to_front,
        )

        self.send_back_action = QtWidgets.QAction(
            QtGui.QIcon(':/icons/send_to_back'),
            'Send to &Back',
            self,
            shortcut='Ctrl+B',
            statusTip='Send item to back',
            triggered=self.send_to_back,
        )

    def create_edit_menu(self):
        self.edit_menu = self.menuBar().addMenu(main_window_constants.EDIT_MENU_NAME)
        self.edit_menu.addAction(self.delete_action)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.to_front_action)
        self.edit_menu.addAction(self.send_back_action)

    def create_frameworks_toolbar(self):
        self.frameworks_label = QtWidgets.QLabel(main_window_constants.FRAMEWORKS_LABEL)

        self.frameworks_combobox = QtWidgets.QComboBox()
        self.frameworks_combobox.setEditable(False)
        for framework in frameworks_utils.get_sorted_frameworks_list():
            self.frameworks_combobox.addItem(framework)

        self.frameworks_toolbar = self.addToolBar(main_window_constants.FRAMEWORKS_TOOLBAR_NAME)
        self.frameworks_toolbar.addWidget(self.frameworks_label)
        self.frameworks_toolbar.addWidget(self.frameworks_combobox)

    def create_edit_diagram_toolbar(self):
        self.edit_diagram_toolbar = self.addToolBar(main_window_constants.DIAGRAM_EDIT_TOOLBAR_NAME)
        self.edit_diagram_toolbar.addAction(self.delete_action)
        self.edit_diagram_toolbar.addAction(self.to_front_action)
        self.edit_diagram_toolbar.addAction(self.send_back_action)

    def create_pointer_toolbar(self):
        pointer_button = QtWidgets.QToolButton()
        pointer_button.setCheckable(True)
        pointer_button.setChecked(True)
        pointer_button.setIcon(QtGui.QIcon(':/icons/pointer'))

        line_pointer_button = QtWidgets.QToolButton()
        line_pointer_button.setCheckable(True)
        line_pointer_button.setIcon(QtGui.QIcon(':/icons/line_pointer'))

        self.pointer_type_group = QtWidgets.QButtonGroup()
        self.pointer_type_group.addButton(pointer_button, DiagramScene.move_item)
        self.pointer_type_group.addButton(line_pointer_button, DiagramScene.insert_line)
        self.pointer_type_group.buttonClicked[int].connect(self.pointer_group_clicked)

        self.scene_scale_combo = QtWidgets.QComboBox()
        self.scene_scale_combo.addItems(main_window_constants.DIAGRAM_SCENE_SCALES)
        self.scene_scale_combo.setCurrentIndex(
            main_window_constants.DIAGRAM_SCENE_SCALES.index(
                main_window_constants.DIAGRAM_SCENE_DEFAULT_SCALE
            )
        )
        self.scene_scale_combo.currentIndexChanged[str].connect(self.scene_scale_changed)

        self.pointer_toolbar = self.addToolBar(main_window_constants.POINTER_TYPE_TOOLBAR_NAME)
        self.pointer_toolbar.addWidget(pointer_button)
        self.pointer_toolbar.addWidget(line_pointer_button)
        self.pointer_toolbar.addWidget(self.scene_scale_combo)

    def create_diagram_scene_and_view(self):
        self.scene = DiagramScene(self.edit_menu)
        self.scene.setSceneRect(QtCore.QRectF(
            0,
            0,
            main_window_constants.DIAGRAM_SCENE_SIZE,
            main_window_constants.DIAGRAM_SCENE_SIZE,
        ))

        self.scene.item_inserted.connect(self.item_inserted)

        self.view = QtWidgets.QGraphicsView(self.scene)

    def create_framework_toolbox(self):
        framework_layers = frameworks_utils.get_framework_layers(self.get_selected_framework())

        self.framework_layers_button_group = QtWidgets.QButtonGroup()
        self.framework_layers_button_group.setExclusive(False)
        self.framework_layers_button_group.buttonClicked[int].connect(self.framework_layers_button_group_clicked)

        layout = QtWidgets.QGridLayout()
        for framework_layer in framework_layers:
            layout.addWidget(self.create_framework_layer_widget(framework_layer()))

        layout.setRowStretch(3, 10)
        layout.setColumnStretch(2, 10)

        item_widget = QtWidgets.QWidget()
        item_widget.setLayout(layout)

        self.framework_toolbox = QtWidgets.QToolBox()
        self.framework_toolbox.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Maximum,
                QtWidgets.QSizePolicy.Ignored,
            )
        )
        self.framework_toolbox.setMinimumWidth(item_widget.sizeHint().width())
        self.framework_toolbox.addItem(item_widget, main_window_constants.LAYERS)

    # Callback methods.
    def delete_item(self):
        for item in self.scene.selectedItems():
            if isinstance(item, DiagramItem):
                item.remove_arrows()
            self.scene.removeItem(item)

    def bring_to_front(self):
        if self.are_scene_items_selected():
            for selected_item in self.scene.selectedItems():
                overlap_items = selected_item.collidingItems()

                z_value = 0
                for item in overlap_items:
                    if item.zValue() >= z_value and isinstance(item, DiagramItem):
                        z_value = item.zValue() + 0.1
                selected_item.setZValue(z_value)

    def send_to_back(self):
        if self.are_scene_items_selected():
            for selected_item in self.scene.selectedItems():
                overlap_items = selected_item.collidingItems()

                z_value = 0
                for item in overlap_items:
                    if item.zValue() <= z_value and isinstance(item, DiagramItem):
                        z_value = item.zValue() - 0.1
                selected_item.setZValue(z_value)

    def pointer_group_clicked(self, index: int):
        self.scene.set_mode(self.pointer_type_group.checkedId())

    def scene_scale_changed(self, scale: str):
        new_scale = int(scale[:scale.index(main_window_constants.DIAGRAM_SCENE_SCALE_PERCENT)]) / 100.0
        old_transform = self.view.transform()
        self.view.resetTransform()
        self.view.translate(old_transform.dx(), old_transform.dy())
        self.view.scale(new_scale, new_scale)

    def item_inserted(self, item: DiagramItem):
        self.pointer_type_group.button(DiagramScene.move_item).setChecked(True)
        self.scene.set_mode(self.pointer_type_group.checkedId())
        layer_index = frameworks_utils.get_framework_layer_index(
            self.get_selected_framework(),
            item.framework_layer.__class__,
        )
        self.framework_layers_button_group.button(layer_index).setChecked(False)

    def framework_layers_button_group_clicked(self, id: int):
        buttons = self.framework_layers_button_group.buttons()
        for button in buttons:
            if self.framework_layers_button_group.button(id) != button:
                button.setChecked(False)

        if self.framework_layers_button_group.button(id).isChecked():
            self.scene.set_item_type(id)
            self.scene.set_framework_name(self.get_selected_framework())
            self.scene.set_mode(DiagramScene.insert_item)
        else:
            self.scene.set_mode(DiagramScene.move_item)

    # Helper methods.
    def are_scene_items_selected(self) -> bool:
        return bool(self.scene.selectedItems())

    def get_selected_framework(self) -> str:
        return str(self.frameworks_combobox.currentText())

    def create_framework_layer_widget(self, framework_layer: LayerInterface) -> QtWidgets.QWidget:
        button = QtWidgets.QToolButton()
        button.setText(framework_layer.layer_name())
        button.setCheckable(True)
        layer_index = frameworks_utils.get_framework_layer_index(
            self.get_selected_framework(),
            framework_layer.__class__,
        )
        self.framework_layers_button_group.addButton(button, layer_index)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(button)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        return widget