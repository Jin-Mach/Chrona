from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget

from src.providers.language_provider import LanguageProvider
from src.utilities.error_handler import Errorhandler
from src.utilities.setup_handler import handle_ui_texts

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class SidePanel(QWidget):
    def __init__(self, stacked_widget: QStackedWidget, main_window: "MainWindow"):
        super().__init__(main_window)
        self.stacked_widget = stacked_widget
        self.main_window = main_window
        self.setLayout(self.create_gui())
        self.create_connection()
        self.set_ui_texts()

    def create_gui(self) -> QVBoxLayout:
            main_layout = QVBoxLayout()
            main_layout.setSpacing(10)
            self.processing_button = QPushButton()
            self.processing_button.setObjectName("processingButton")
            self.workflow_settings_button = QPushButton()
            self.workflow_settings_button.setObjectName("workflowSettingsButton")
            main_layout.addWidget(self.processing_button)
            main_layout.addWidget(self.workflow_settings_button)
            main_layout.addStretch()
            return main_layout

    def create_connection(self) -> None:
        self.processing_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.workflow_settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

    def set_ui_texts(self) -> None:
        try:
            texts_data = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__,
                                                         LanguageProvider.language_code)
            if not texts_data:
                raise IOError("Texts data loading failed.")
            handle_ui_texts(self, texts_data, self.findChildren(QPushButton))
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)