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
from widgets.arrow import Arrow
from frameworks.layer_interface import LayerInterface


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.create_edit_diagram_actions()
        self.create_file_menu()
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

    def create_file_menu(self):
        self.export_action = QtWidgets.QAction(
            QtGui.QIcon(':/icons/export'),
            '&Export',
            self,
            shortcut='Ctrl+E',
            statusTip='Export to Python code',
            triggered=self.export_diagram,
        )

        self.file_menu = self.menuBar().addMenu(main_window_constants.FILE_MENU_NAME)
        self.file_menu.addAction(self.export_action)

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
    def export_diagram(self):
        nodes = self.get_nodes_from_scene()

        if len(nodes) == 0:
            return

        edges = self.get_edges_from_scene()
        nodes_mapping = self.create_nodes_mapping(nodes)
        uni_graph, bi_graph = self.create_model_graph(nodes, edges, nodes_mapping)

        if not self.is_one_connected_component(bi_graph):
            self.show_model_graph_eval_error_msg(main_window_constants.MODEL_GRAPH_MULTIPLE_COMPONENTS_ERROR_MSG)
        else:
            topological_sort = self.create_graph_topological_sort(uni_graph)
            if topological_sort is None:
                self.show_model_graph_eval_error_msg(main_window_constants.MODEL_GRAPH_CYCLE_ERROR_MSG)
            else:
                framework_template = frameworks_utils.get_framework_template(self.get_selected_framework())
                layers_definition = self.build_layers_definition(nodes, topological_sort)
                model_connections = self.build_model_connections(nodes, uni_graph, topological_sort)
                framework_template = framework_template.format(layers_definition, model_connections)

                file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
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

    def is_root_node(self, uni_graph, elem) -> bool:
        for node in range(len(uni_graph)):
            if elem in uni_graph[node]:
                return False

        return True

    def get_selected_framework(self) -> str:
        return str(self.frameworks_combobox.currentText())

    def get_nodes_from_scene(self) -> List[DiagramItem]:
        items = self.scene.items()
        nodes = list(filter(lambda item: isinstance(item, DiagramItem), items))

        return nodes

    def get_edges_from_scene(self) -> List[Arrow]:
        items = self.scene.items()
        edges = list(filter(lambda item: isinstance(item, Arrow), items))

        return edges

    def create_nodes_mapping(self, nodes):
        nodes_mapping = dict()

        for index, node in enumerate(nodes):
            nodes_mapping[node] = index

        return nodes_mapping

    def show_model_graph_eval_error_msg(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText(main_window_constants.MODEL_GRAPH_EVAL_ERROR_MSG_TEXT)
        msg.setInformativeText(message)
        msg.setWindowTitle(main_window_constants.MODEL_GRAPH_EVAL_ERROR_MSG_TEXT)
        msg.exec_()

    def create_model_graph(self, nodes, edges, nodes_mapping) -> List[List[int]]:
        uni_graph = [list() for _ in range(len(nodes))]
        bi_graph = [list() for _ in range(len(nodes))]

        for edge in edges:
            start_item = edge.get_start_item()
            end_item = edge.get_end_item()

            uni_graph[nodes_mapping[start_item]].append(nodes_mapping[end_item])

            bi_graph[nodes_mapping[start_item]].append(nodes_mapping[end_item])
            bi_graph[nodes_mapping[end_item]].append(nodes_mapping[start_item])

        return uni_graph, bi_graph

    def build_layers_definition(self, nodes, topological_sort) -> str:
        layers_code = list()

        for elem in topological_sort:
            layers_code.append(nodes[elem].get_framework_layer().layer_definition())

        return '\n'.join(layers_code)

    def build_model_connections(self, nodes, uni_graph, topological_sort) -> str:
        model_connections = list()

        for elem in topological_sort:
            parents = list()
            is_root = list()
            for node in range(len(uni_graph)):
                if elem in uni_graph[node]:
                    parents.append(nodes[node].get_framework_layer())
                    is_root.append(self.is_root_node(uni_graph, node))

            layer_connections = nodes[elem].get_framework_layer().layer_connections(parents, is_root)
            if layer_connections:
                model_connections.append(layer_connections)

        return '\n'.join(model_connections)

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

    def is_one_connected_component(self, graph) -> bool:
        queue = [0]
        visited = [False for _ in range(len(graph))]

        while len(queue):
            current_node = queue[0]
            queue.pop(0)

            if visited[current_node]:
                continue
            visited[current_node] = True

            for child in graph[current_node]:
                queue.append(child)

        if sum(visited) != len(visited):
            return False
        return True

    def create_graph_topological_sort(self, graph) -> List[int]:
        nodes_in = [0] * len(graph)
        for node in range(len(graph)):
            for child in graph[node]:
                nodes_in[child] += 1

        queue = list()
        for index, node_in in enumerate(nodes_in):
            if node_in == 0:
                queue.append(index)

        topological_sort = list()
        while len(queue):
            current_node = queue[0]
            queue.pop(0)
            topological_sort.append(current_node)

            for child in graph[current_node]:
                nodes_in[child] -= 1
                if nodes_in[child] == 0:
                    queue.append(child)

        if len(topological_sort) != len(graph):
            return None

        return topological_sort
