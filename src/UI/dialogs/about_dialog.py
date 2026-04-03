from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

from src.providers.language_provider import LanguageProvider
from src.utilities.error_handler import Errorhandler
from src.utilities.setup_handler import handle_ui_texts

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class AboutDialog(QDialog):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.setLayout(self.create_gui())
        self.set_ui_texts()
        self.create_connection()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        title_label = QLabel()
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font: bold;")
        text_label = QLabel()
        text_label.setObjectName("textLabel")
        text_label.setTextFormat(Qt.TextFormat.RichText)
        text_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        text_label.setOpenExternalLinks(True)
        button_layout = QHBoxLayout()
        self.close_button = QPushButton()
        self.close_button.setObjectName("closeButton")
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        button_layout.addStretch()
        main_layout.addWidget(title_label)
        main_layout.addWidget(text_label)
        main_layout.addLayout(button_layout)
        return main_layout

    def set_ui_texts(self) -> None:
        try:
            texts_data = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__,
                                                         LanguageProvider.language_code)
            if not texts_data:
                raise IOError("Texts data loading failed.")
            handle_ui_texts(self, texts_data, self.findChildren((QLabel, QPushButton)))
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def create_connection(self) -> None:
        self.close_button.clicked.connect(self.reject)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.adjustSize()
        self.setFixedSize(self.size())