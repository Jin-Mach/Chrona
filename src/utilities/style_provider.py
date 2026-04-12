import pathlib

from PyQt6.QtGui import QIcon
from qt_material import apply_stylesheet

from PyQt6.QtWidgets import QApplication


def set_application_style(application: QApplication, project_path: pathlib.Path) -> None:
    app_icon = project_path.joinpath("resources", "images", "application_icon.png")
    if app_icon.exists():
        application.setWindowIcon(QIcon(str(app_icon)))
    application.setStyle("Fusion")
    apply_stylesheet(application, "dark_blue.xml")