# This Python file uses the following encoding: utf-8

# Built-in imports
import sys

# Third-party package imports
from PyQt5 import QtWidgets

# First-party package imports
from main_window import MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.showMaximized()

    sys.exit(app.exec_())
