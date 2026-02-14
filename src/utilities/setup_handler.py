from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMainWindow, QGroupBox, QCheckBox, QRadioButton

from src.utilities.error_handler import Errorhandler


def handle_ui_texts(top_widget: QWidget, texts_data: dict[str, str], widgets: list[QWidget] | None  = None) -> None:
    try:
        if "titleText" in texts_data:
            if isinstance(top_widget, QMainWindow):
                top_widget.setWindowTitle(texts_data["titleText"])
        if not widgets:
            return
        for widget in widgets:
            key_name = widget.objectName() + "Text"
            if key_name in texts_data:
                text = texts_data[key_name]
                if isinstance(widget, (QLabel, QPushButton, QCheckBox, QRadioButton)):
                    widget.setText(text)
                elif isinstance(widget, QLineEdit):
                    widget.setPlaceholderText(text)
                elif isinstance(widget, QGroupBox):
                    widget.setTitle(text)
    except Exception as e:
        Errorhandler.handle_error("UITextsHandler", e)

def handle_ui_widgets(config_data: dict[str, bool], widgets: list[QWidget]) -> None:
    try:
        if not widgets:
            return
        for widget in widgets:
            key_name = widget.objectName() + "State"
            if key_name in config_data:
                if isinstance(widget, (QCheckBox, QRadioButton)):
                    widget.setChecked(config_data[key_name])
    except Exception as e: Errorhandler.handle_error("UIWidgetsHandler", e)