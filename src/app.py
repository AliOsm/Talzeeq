# Built-in imports.
import sys

# Third-party package imports.
from PyQt5.QtWidgets import QApplication

# First-party package imports.
from widgets.main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.showMaximized()

    sys.exit(app.exec_())
