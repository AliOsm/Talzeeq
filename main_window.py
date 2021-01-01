# This Python file uses the following encoding: utf-8

# Third-party package imports
from PyQt5 import QtWidgets

# First-party package imports
from utils import frameworks_utils
from constants import main_window_constants


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle(main_window_constants.MAIN_WINDOW_TITLE)

        self.createFrameworksToolbar()

    def createFrameworksToolbar(self):
        self.frameworksLabel = QtWidgets.QLabel(main_window_constants.FRAMEWORKS_LABEL)

        self.frameworksCombo = QtWidgets.QComboBox()
        self.frameworksCombo.setEditable(False)
        for framework in frameworks_utils.get_sorted_frameworks_list():
            self.frameworksCombo.addItem(framework)

        self.frameworksToolbar = self.addToolBar(main_window_constants.FRAMEWORKS_TOOL_BAR_NAME)
        self.frameworksToolbar.addWidget(self.frameworksLabel)
        self.frameworksToolbar.addWidget(self.frameworksCombo)
