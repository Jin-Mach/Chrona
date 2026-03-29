from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QLabel

from src.providers.language_provider import LanguageProvider
from src.utilities.setup_handler import handle_ui_texts

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class NotificationDialog(QDialog):
    def __init__(self, main_window: "MainWindow"):
        super().__init__(main_window)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.main_window = main_window
        self.setLayout(self.create_gui())
        self.set_ui_texts()
        QTimer.singleShot(3000, self.reject)

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.info_label = QLabel()
        self.info_label.setObjectName("infoLabel")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.count_label = QLabel()
        self.count_label.setObjectName("countLabel")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label = QLabel()
        self.loading_label.setObjectName("loadingLabel")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setVisible(False)
        main_layout.addWidget(self.info_label)
        main_layout.addWidget(self.count_label)
        main_layout.addWidget(self.loading_label)
        return main_layout

    def set_ui_texts(self) -> None:
        text_data = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__,
                                                    LanguageProvider.language_code)
        if not text_data:
            raise IOError("texts data loading failed.")
        self.processed_text = text_data.get("processedText", "Processed files:")
        self.failed_text = text_data.get("failedText", "Unprocessed files:")
        handle_ui_texts(self, text_data, self.findChildren(QLabel))

    def update_label_text(self, processed_count: int, failed_count: int) -> None:
        self.count_label.setText(f"{self.processed_text} {processed_count}\n{self.failed_text} {failed_count}")
        if failed_count > 0:
            self.loading_label.setVisible(True)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.adjustSize()
        self.setFixedSize(self.size())
        geometry = self.main_window.frameGeometry()
        x_pos = (geometry.x() + geometry.width()) - (self.size().width() + 10)
        y_pos = (geometry.y() + geometry.height()) - (self.size().height() + 10)
        self.move(x_pos, y_pos)