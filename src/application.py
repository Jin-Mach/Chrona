import sys

from PyQt6.QtWidgets import QApplication

from src.UI.main_window import MainWindow


def create_application() -> None:
    application = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(application.exec())