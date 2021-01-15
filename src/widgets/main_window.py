# Built-in imports.
from typing import List, Dict

# Third-party package imports.
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QAction,
    QButtonGroup,
    QComboBox,
    QFileDialog,
    QGraphicsView,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QToolBox,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

# First-party package imports.
import resources_rc

from utils import frameworks_utils
from utils import graph_utils
from constants import main_window_constants
from widgets.diagram_scene import DiagramScene
from widgets.diagram_item import DiagramItem
from widgets.arrow import Arrow
from widgets.qaction_properties import QActionProperties
from frameworks.layer_interface import LayerInterface


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.create_main_window_actions([
            QActionProperties(
                name=main_window_constants.EXPORT_ACTION_NAME,
                icon=QIcon(':/icons/export'),
                text='&Export',
                shortcut='Ctrl+E',
                status_tip='Export to Python code',
                triggered=self.export_diagram,
            ),
            QActionProperties(
                name=main_window_constants.DELETE_ACTON_NAME,
                icon=QIcon(':/icons/delete'),
                text='&Delete',
                shortcut='Delete',
                status_tip='Delete item from diagram',
                triggered=self.delete_item,
            ),
            QActionProperties(
                name=main_window_constants.TO_FRONT_ACTION_NAME,
                icon=QIcon(':/icons/bring_to_front'),
                text='Bring to &Front',
                shortcut='Ctrl+F',
                status_tip='Bring item to front',
                triggered=self.bring_to_front,
            ),
            QActionProperties(
                name=main_window_constants.TO_BACK_ACTION_NAME,
                icon=QIcon(':/icons/send_to_back'),
                text='Send to &Back',
                shortcut='Ctrl+B',
                status_tip='Send item to back',
                triggered=self.send_to_back,
            ),
        ])

        self.create_file_menu()
        self.create_edit_menu()
        self.create_frameworks_toolbar()
        self.create_edit_diagram_toolbar()
        self.create_pointer_toolbar()
        self.create_diagram_scene_and_view()
        self.create_framework_toolbox()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.framework_toolbox)
        self.layout.addWidget(self.view)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setWindowTitle(main_window_constants.MAIN_WINDOW_TITLE)
        self.setCentralWidget(self.widget)

    # Create methods.
    def create_main_window_actions(self, main_window_actions: List[QActionProperties]):
        self.main_window_actions = dict()
        for main_window_action in main_window_actions:
            self.main_window_actions[main_window_action.name] = QAction(
                main_window_action.icon,
                main_window_action.text,
                self,
                shortcut=main_window_action.shortcut,
                statusTip=main_window_action.status_tip,
                triggered=main_window_action.triggered,
            )

    def create_file_menu(self):
        self.file_menu = self.menuBar().addMenu(main_window_constants.FILE_MENU_NAME)
        self.file_menu.addAction(self.main_window_actions[main_window_constants.EXPORT_ACTION_NAME])

    def create_edit_menu(self):
        self.edit_menu = self.menuBar().addMenu(main_window_constants.EDIT_MENU_NAME)
        self.edit_menu.addAction(self.main_window_actions[main_window_constants.DELETE_ACTON_NAME])
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.main_window_actions[main_window_constants.TO_FRONT_ACTION_NAME])
        self.edit_menu.addAction(self.main_window_actions[main_window_constants.TO_BACK_ACTION_NAME])

    def create_frameworks_toolbar(self):
        self.frameworks_label = QLabel(main_window_constants.FRAMEWORKS_LABEL)

        self.frameworks_combobox = QComboBox()
        self.frameworks_combobox.setEditable(False)
        for framework in frameworks_utils.get_sorted_frameworks_list():
            self.frameworks_combobox.addItem(framework)

        self.frameworks_toolbar = self.addToolBar(main_window_constants.FRAMEWORKS_TOOLBAR_NAME)
        self.frameworks_toolbar.addWidget(self.frameworks_label)
        self.frameworks_toolbar.addWidget(self.frameworks_combobox)

    def create_edit_diagram_toolbar(self):
        self.edit_diagram_toolbar = self.addToolBar(main_window_constants.DIAGRAM_EDIT_TOOLBAR_NAME)
        self.edit_diagram_toolbar.addAction(self.main_window_actions[main_window_constants.DELETE_ACTON_NAME])
        self.edit_diagram_toolbar.addAction(self.main_window_actions[main_window_constants.TO_FRONT_ACTION_NAME])
        self.edit_diagram_toolbar.addAction(self.main_window_actions[main_window_constants.TO_BACK_ACTION_NAME])

    def create_pointer_toolbar(self):
        pointer_button = QToolButton()
        pointer_button.setCheckable(True)
        pointer_button.setChecked(True)
        pointer_button.setIcon(QIcon(':/icons/pointer'))

        line_pointer_button = QToolButton()
        line_pointer_button.setCheckable(True)
        line_pointer_button.setIcon(QIcon(':/icons/line_pointer'))

        self.pointer_type_group = QButtonGroup()
        self.pointer_type_group.addButton(pointer_button, DiagramScene.move_item)
        self.pointer_type_group.addButton(line_pointer_button, DiagramScene.insert_line)
        self.pointer_type_group.buttonClicked[int].connect(self.pointer_group_clicked)

        scene_scale_combo = QComboBox()
        scene_scale_combo.addItems(main_window_constants.DIAGRAM_SCENE_SCALES)
        scene_scale_combo.setCurrentIndex(
            main_window_constants.DIAGRAM_SCENE_SCALES.index(main_window_constants.DIAGRAM_SCENE_DEFAULT_SCALE)
        )
        scene_scale_combo.currentIndexChanged[str].connect(self.scene_scale_changed)

        self.pointer_toolbar = self.addToolBar(main_window_constants.POINTER_TYPE_TOOLBAR_NAME)
        self.pointer_toolbar.addWidget(pointer_button)
        self.pointer_toolbar.addWidget(line_pointer_button)
        self.pointer_toolbar.addWidget(scene_scale_combo)

    def create_diagram_scene_and_view(self):
        self.scene = DiagramScene(self.edit_menu)
        self.scene.setSceneRect(
            QRectF(0, 0, main_window_constants.DIAGRAM_SCENE_SIZE, main_window_constants.DIAGRAM_SCENE_SIZE)
        )
        self.scene.item_inserted.connect(self.item_inserted)
        self.view = QGraphicsView(self.scene)

    def create_framework_toolbox(self):
        framework_layers = frameworks_utils.get_framework_layers(self.get_selected_framework())

        self.framework_layers_button_group = QButtonGroup()
        self.framework_layers_button_group.setExclusive(False)
        self.framework_layers_button_group.buttonClicked[int].connect(self.framework_layers_button_group_clicked)

        layout = QGridLayout()
        for framework_layer in framework_layers:
            layout.addWidget(self.create_framework_layer_widget(framework_layer()))

        layout.setRowStretch(3, 10)
        layout.setColumnStretch(2, 10)

        item_widget = QWidget()
        item_widget.setLayout(layout)

        self.framework_toolbox = QToolBox()
        self.framework_toolbox.setSizePolicy(
            QSizePolicy(
                QSizePolicy.Maximum,
                QSizePolicy.Ignored,
            ),
        )
        self.framework_toolbox.setMinimumWidth(item_widget.sizeHint().width())
        self.framework_toolbox.addItem(item_widget, main_window_constants.LAYERS)

    # Callback methods.
    def export_diagram(self):
        nodes = self.get_nodes_from_scene()

        if len(nodes) == 0:
            return

        edges = self.get_edges_from_scene()
        nodes_mapping = self.create_nodes_mapping(nodes)
        uni_graph = graph_utils.create_graph_from_qt_elements(nodes, edges, nodes_mapping)
        bi_graph = graph_utils.create_graph_from_qt_elements(nodes, edges, nodes_mapping, is_bi_directional=True)
        
        is_one_connected_component = graph_utils.is_one_connected_component(bi_graph)
        graph_topological_sort = graph_utils.create_graph_topological_sort(uni_graph)

        if not is_one_connected_component:
            self.show_model_graph_eval_error_msg(main_window_constants.MODEL_GRAPH_MULTIPLE_COMPONENTS_ERROR_MSG)
        elif graph_topological_sort is None:
            self.show_model_graph_eval_error_msg(main_window_constants.MODEL_GRAPH_CYCLE_ERROR_MSG)
        else:
            layer_definitions = self.build_layer_definitions(nodes, graph_topological_sort)
            model_connections = self.build_model_connections(nodes, uni_graph, graph_topological_sort)
            framework_template = frameworks_utils.get_formatted_framework_template(
                self.get_selected_framework(),
                layer_definitions,
                model_connections,
            )

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                'Export Model As',
                'talzeeq.py',
                'Python Language (*.py);;'
                'All files (*.*)',
            )

            if file_path:
                with open(file_path, 'w') as fp:
                    fp.write(framework_template)

    def delete_item(self):
        for item in self.scene.selectedItems():
            if isinstance(item, DiagramItem):
                item.remove_arrows()
            self.scene.removeItem(item)

    def bring_to_front(self):
        for selected_item in self.scene.selectedItems():
            z_value = 0
            for item in selected_item.collidingItems():
                if item.zValue() >= z_value and isinstance(item, DiagramItem):
                    z_value = item.zValue() + 0.1
            selected_item.setZValue(z_value)

    def send_to_back(self):
        for selected_item in self.scene.selectedItems():
            z_value = 0
            for item in selected_item.collidingItems():
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
    def get_selected_framework(self) -> str:
        return str(self.frameworks_combobox.currentText())

    def get_nodes_from_scene(self) -> List[DiagramItem]:
        return list(filter(lambda item: isinstance(item, DiagramItem), self.scene.items()))

    def get_edges_from_scene(self) -> List[Arrow]:
        return list(filter(lambda item: isinstance(item, Arrow), self.scene.items()))

    def create_nodes_mapping(self, nodes: List[DiagramItem]) -> Dict[DiagramItem, int]:
        return { node:index for index, node in enumerate(nodes) }

    def show_model_graph_eval_error_msg(self, message: str):
        msg = QMessageBox().setIcon(QMessageBox.Critical)
        msg.setText(main_window_constants.MODEL_GRAPH_EVAL_ERROR_MSG_TEXT)
        msg.setInformativeText(message)
        msg.setWindowTitle(main_window_constants.MODEL_GRAPH_EVAL_ERROR_MSG_TEXT)
        msg.exec_()

    def build_layer_definitions(self, nodes: List[DiagramItem], graph_topological_sort: List[int]) -> str:
        return '\n'.join([nodes[element].get_framework_layer().layer_definition() for element in graph_topological_sort])

    def build_model_connections(
        self,
        nodes: List[DiagramItem],
        graph: List[List[int]],
        graph_topological_sort: List[int],
    ) -> str:
        model_connections = list()

        for element in graph_topological_sort:
            parents = list()
            is_root = list()
            for node in range(len(graph)):
                if element in graph[node]:
                    parents.append(nodes[node].get_framework_layer())
                    is_root.append(graph_utils.is_root_node(graph, node))

            layer_connections = nodes[element].get_framework_layer().layer_connections(parents, is_root)
            if layer_connections:
                model_connections.append(layer_connections)

        return '\n'.join(model_connections)

    def create_framework_layer_widget(self, framework_layer: LayerInterface) -> QWidget:
        button = QToolButton()
        button.setText(framework_layer.layer_name())
        button.setCheckable(True)
        self.framework_layers_button_group.addButton(
            button,
            frameworks_utils.get_framework_layer_index(
                self.get_selected_framework(),
                framework_layer.__class__,
            ),
        )

        layout = QVBoxLayout()
        layout.addWidget(button)

        widget = QWidget()
        widget.setLayout(layout)

        return widget
