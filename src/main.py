import sys

from PyQt6.QtWidgets import QApplication

from src.UI.main_window import MainWindow
from src.providers.application_init_provider import ApplicationInitProvider


def create_application() -> None:
    application = QApplication(sys.argv)
    if not ApplicationInitProvider.initialize_application():
        sys.exit(1)
    main_window = MainWindow()
    main_window.show()
    sys.exit(application.exec())