from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QPushButton

from src.providers.language_provider import LanguageProvider
from src.utilities.setup_handler import handle_ui_texts

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class ProgressDialog(QDialog):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setModal(True)
        self.main_window = main_window
        self.setLayout(self.create_gui())
        self.set_ui_texts()
        self._file_count = 0

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.title_label = QLabel()
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setTextVisible(False)
        self.progress_value_label = QLabel()
        self.progress_value_label.setObjectName("progressValueLabel")
        self.progress_value_label.setVisible(False)
        button_layout = QHBoxLayout()
        self.cancel_progress_button = QPushButton()
        self.cancel_progress_button.setObjectName("cancelProgressButton")
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_progress_button)
        button_layout.addStretch()
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_value_label)
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(progress_layout)
        main_layout.addLayout(button_layout)
        return main_layout

    def set_ui_texts(self) -> None:
        text_data = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__,
                                                   LanguageProvider.language_code)
        if not text_data:
            raise IOError("texts data loading failed.")
        self.progress_text = text_data.get("progressText", "Processing...")
        handle_ui_texts(self, text_data, self.findChildren((QLabel, QPushButton)))

    def set_progress_bar_range(self, value: int) -> None:
        self._file_count = value
        self.progress_bar.setRange(0, self._file_count)
        if self.progress_text:
            self.title_label.setText(self.progress_text)

    def update_progress_value_label(self, value: int) -> None:
        self.progress_bar.setValue(value)
        if not self.progress_value_label.isVisible():
            self.progress_value_label.setVisible(True)
        self.progress_value_label.setText(f"{value}/{self._file_count}")

    def set_failed_list_text(self) -> None:
        self.title_label.setText("Loading failed list...")