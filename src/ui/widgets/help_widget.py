from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QTextEdit

from core.providers.config_provider import ConfigProvider
from core.providers.language_provider import LanguageProvider
from src.utils.error_handler import Errorhandler
from src.utils.setup_handler import handle_ui_widgets

if TYPE_CHECKING:
    from src.ui.main_window import MainWindow


class HelpWidget(QWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.setLayout(self.create_gui())
        self.set_ui_texts()
        self.set_config_data()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("textEdit")
        main_layout.addWidget(self.text_edit)
        return main_layout

    def set_ui_texts(self) -> None:
        try:
            text_data = LanguageProvider.get_help_texts(LanguageProvider.language_code)
            if not text_data:
                raise IOError("Texts data loading failed.")
            self.text_edit.setHtml(text_data)
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def set_config_data(self) -> None:
        try:
            config_data = ConfigProvider.get_config_data(self.__class__.__name__)
            if not config_data:
                raise IOError("Config data loading failed.")
            handle_ui_widgets(config_data, self.findChildren(QTextEdit))
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)