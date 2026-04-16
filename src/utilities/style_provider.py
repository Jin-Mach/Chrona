import pathlib

from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import QApplication


def set_application_style(application: QApplication, project_path: pathlib.Path) -> None:
    app_icon = project_path.joinpath("resources", "images", "application_icon.png")
    if app_icon.exists():
        application.setWindowIcon(QIcon(str(app_icon)))
    application.setStyle("Fusion")
    application.setStyleSheet(load_qss_file(project_path))

def load_qss_file(project_path: pathlib.Path) -> str:
    stylesheet = ""
    qss_file = project_path.joinpath("src", "UI", "styles", "application_style.qss")
    if qss_file.exists():
        with open(qss_file, "r", encoding="utf-8") as file:
            stylesheet = file.read()
    return stylesheet