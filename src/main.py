import sys

from PyQt6.QtWidgets import QApplication

from src.UI.main_window import MainWindow
from src.providers.application_init_provider import ApplicationInit


def create_application() -> None:
    application = QApplication(sys.argv)
    if not ApplicationInit.initialize_application():
        sys.exit(1)
    main_window = MainWindow()
    main_window.show()
    sys.exit(application.exec())