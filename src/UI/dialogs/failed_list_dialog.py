import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLayout, QDialogButtonBox, QListWidget, QPushButton, \
    QListWidgetItem, QHBoxLayout, QApplication, QAbstractItemView

from src.providers.language_provider import LanguageProvider
from src.utilities.error_handler import Errorhandler
from src.utilities.path_helpers import show_selected_path
from src.utilities.setup_handler import handle_ui_texts

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class FailedListDialog(QDialog):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.setModal(True)
        self.setLayout(self.create_gui())
        self.set_ui_texts()
        self.create_connection()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.title_label = QLabel()
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("listWidget")
        self.list_widget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        count_layout = QHBoxLayout()
        self.count_label = QLabel()
        self.count_label.setObjectName("countLabel")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_layout.addStretch()
        count_layout.addWidget(self.count_label)
        button_layout = QHBoxLayout()
        self.show_path_button = QPushButton()
        self.show_path_button.setObjectName("showPathButton")
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        button_box.rejected.connect(self.reject)
        button_layout.addWidget(self.show_path_button)
        button_layout.addStretch()
        button_layout.addWidget(button_box)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.list_widget)
        main_layout.addLayout(count_layout)
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
        self.show_path_button.clicked.connect(self.show_path)

    def set_list_widget(self, failed_list: list[tuple[pathlib.Path, Exception]]) -> None:
        count_text = self.count_label.text() + f" {len(failed_list)}"
        self.count_label.setText(count_text)
        self.list_widget.clear()
        for path, _ in failed_list:
            list_widget_item = QListWidgetItem()
            list_widget_item.setText(str(path.name))
            list_widget_item.setToolTip(str(path))
            list_widget_item.setData(Qt.ItemDataRole.UserRole, path)
            self.list_widget.addItem(list_widget_item)
        self.list_widget.setSortingEnabled(True)
        self.list_widget.sortItems(Qt.SortOrder.AscendingOrder)
        self.list_widget.setCurrentRow(0)

    def show_path(self) -> None:
        item = self.list_widget.currentItem()
        if item is not None:
            path = item.data(Qt.ItemDataRole.UserRole)
            show_selected_path(path)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.adjustSize()
        self.setFixedSize(self.size())
        if self.parentWidget() is None:
            screen = QApplication.primaryScreen().availableGeometry()
            geometry = self.frameGeometry()
            geometry.moveCenter(screen.center())
            self.move(geometry.topLeft())