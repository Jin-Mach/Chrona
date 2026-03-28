import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLayout, QDialogButtonBox, QListWidget, QPushButton, \
    QListWidgetItem, QHBoxLayout, QApplication

from src.providers.language_provider import LanguageProvider
from src.utilities.error_handler import Errorhandler
from src.utilities.setup_handler import handle_ui_texts

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class FailedListDialog(QDialog):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.setLayout(self.create_gui())
        self.set_ui_texts()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.title_label = QLabel()
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("listWidget")
        count_layout = QHBoxLayout()
        self.count_label = QLabel()
        self.count_label.setObjectName("countLabel")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_layout.addStretch()
        count_layout.addWidget(self.count_label)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(count_layout)
        main_layout.addWidget(button_box)
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

    def set_list_widget(self, failed_list: list[tuple[pathlib.Path, Exception]]) -> None:
        count_text = self.count_label.text() + f" {len(failed_list)}"
        self.count_label.setText(count_text)
        self.list_widget.clear()
        for path, _ in failed_list:
            list_widget_item = QListWidgetItem()
            list_widget_item.setText(f"...{str(path.name)}")
            list_widget_item.setToolTip(str(path))
            self.list_widget.addItem(list_widget_item)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.adjustSize()
        self.setFixedSize(self.size())
        if self.parentWidget() is None:
            screen = QApplication.primaryScreen().availableGeometry()
            geometry = self.frameGeometry()
            geometry.moveCenter(screen.center())
            self.move(geometry.topLeft())