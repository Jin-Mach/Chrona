from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QMainWindow, QGroupBox, QCheckBox, QRadioButton

from src.utilities.error_handler import Errorhandler


def handle_ui_texts(top_widget: QWidget, texts_data: dict[str, str], widgets: list[QWidget] | None = None) -> None:
    try:
        title = texts_data.get("titleText")
        if title and isinstance(top_widget, QMainWindow):
            top_widget.setWindowTitle(title)
        if not widgets:
            return
        for widget in widgets:
            widget_name = widget.objectName()
            text = texts_data.get(widget_name + "Text")
            tooltip = texts_data.get(widget_name + "TooltipText")
            placeholder = texts_data.get(widget_name + "PlaceholderText")
            if isinstance(widget, (QLabel, QPushButton, QCheckBox, QRadioButton)):
                if text:
                    widget.setText(text)
            if isinstance(widget, QGroupBox):
                if text:
                    widget.setTitle(text)
            if isinstance(widget, QLineEdit):
                if placeholder:
                    widget.setPlaceholderText(placeholder)
            if tooltip:
                widget.setToolTip(tooltip)
                widget.setToolTipDuration(5000)
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