import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from src.UI.dialogs.splash_screen_provider import show_splash_screen
from src.UI.main_window import MainWindow
from src.providers.application_init_provider import ApplicationInitProvider


def run_application() -> None:
    application = QApplication(sys.argv)
    splash_screen = show_splash_screen()
    splash_state = splash_screen is not None
    if splash_state:
        splash_screen.show()
        application.processEvents()
    if not ApplicationInitProvider.initialize_application(application):
        sys.exit(1)
    main_window = MainWindow()
    if splash_state:
        QTimer.singleShot(1000, lambda: (splash_screen.finish(main_window), main_window.show()))
    else:
        main_window.show()
    sys.exit(application.exec())