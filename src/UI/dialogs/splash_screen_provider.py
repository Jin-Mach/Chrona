from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QSplashScreen

from src.utilities.current_path_provider import set_project_path
from src.UI.widgets.splash_screen import SplashScreen


def show_splash_screen() -> QSplashScreen | None:
    project_path = set_project_path()
    if not project_path.exists():
        return None
    img = project_path.joinpath("resources", "images", "splash_icon.jpg")
    if not img.exists():
        return None
    pixmap = QPixmap(str(img))
    if pixmap.isNull():
        return None
    pixmap = pixmap.scaled(800, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    splash_screen = SplashScreen(pixmap)
    return splash_screen