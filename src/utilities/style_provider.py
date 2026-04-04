import datetime

from qt_material import apply_stylesheet

from PyQt6.QtWidgets import QApplication

THEME = {
    "light": "light_blue.xml",
    "dark": "dark_blue.xml"
}

def set_application_style(application: QApplication) -> None:
    application.setStyle("Fusion")
    theme_key = get_theme_by_time()
    theme_file = THEME.get(theme_key)
    if theme_file:
        apply_stylesheet(application, theme_file)

def get_theme_by_time() -> str:
    now = datetime.datetime.now().time()
    if now >= datetime.time(20, 0) or now < datetime.time(7, 0):
        return "dark"
    return "light"