import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtCore import QFileInfo, Qt
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QFileIconProvider, QListWidgetItem, QListWidget, QPushButton, \
    QWidget, QHBoxLayout, QLabel, QDialogButtonBox, QSizePolicy

from src.UI.dialogs.messagebox_dialogs import show_question_dialog
from src.providers.language_provider import LanguageProvider
from src.utilities.error_handler import Errorhandler
from src.utilities.path_helpers import show_selected_path
from src.utilities.setup_handler import handle_ui_texts

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class SelectedItemsDialog(QDialog):
    def __init__(self, main_window: "MainWindow"):
        super().__init__(main_window)
        self.setMinimumSize(600, 700)
        self.main_window = main_window
        self.selected_files = self.main_window.process_provider.selected_files
        self.setModal(True)
        self.setLayout(self.create_gui())
        self.set_ui_texts()
        self.create_connections()
        self.set_items_list()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.title_label = QLabel()
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.list_widget = QListWidget()
        button_layout = QHBoxLayout()
        self.show_path_button = QPushButton()
        self.show_path_button.setObjectName("showPathButton")
        self.clear_items_button = QPushButton()
        self.clear_items_button.setObjectName("clearItemsButton")
        button_layout.addWidget(self.show_path_button)
        button_layout.addWidget(self.clear_items_button)
        button_layout.addStretch()
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.list_widget, 1)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_texts(self) -> None:
        try:
            texts_data = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__,
                                                         LanguageProvider.language_code)
            if not texts_data:
                raise IOError("Texts data loading failed.")
            handle_ui_texts(self, texts_data, self.findChildren((QLabel, QPushButton)))
            self.item_button_text = texts_data.get("itemButtonText", "Remove item")
            self.clear_title = texts_data.get("questionTitleText", "Chrona")
            self.clear_items_text = texts_data.get("clearItemText", "Delete all selected items?")
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def create_connections(self) -> None:
        self.show_path_button.clicked.connect(self.show_path)
        self.clear_items_button.clicked.connect(self.show_clear_items_dialog)

    def set_items_list(self) -> None:
        provider = QFileIconProvider()
        for index, item_path in enumerate(self.selected_files):
            path = pathlib.Path(item_path)
            icon_type = QFileInfo(str(path))
            icon = provider.icon(icon_type)
            item = QListWidgetItem()
            item.setIcon(icon)
            item.setData(Qt.ItemDataRole.UserRole, path)
            item_widget = QWidget()
            item_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            item_layout = QHBoxLayout()
            item_layout.setContentsMargins(5, 5, 5, 5)
            item_layout.setSpacing(10)
            item_label = QLabel()
            item_label.setText(str(path.name))
            item_label.setToolTip(str(path))
            item_label.setToolTipDuration(5000)
            item_button = QPushButton()
            item_button.setText(self.item_button_text)
            item_button.clicked.connect(lambda _, it=item: self.delete_selected_item(it))
            item_layout.addWidget(item_label)
            item_layout.addStretch()
            item_layout.addWidget(item_button)
            item_widget.setLayout(item_layout)
            item_widget.adjustSize()
            item.setSizeHint(item_widget.sizeHint())
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, item_widget)

    def delete_selected_item(self, item: QListWidgetItem) -> None:
        item_path = item.data(Qt.ItemDataRole.UserRole)
        if str(item_path) in self.selected_files:
            self.selected_files.remove(str(item_path))
            if item_path.is_dir():
                self.main_window.processing_widget.update_count_labels(folders_count=-1)
            if item_path.is_file():
                self.main_window.processing_widget.update_count_labels(files_count=-1)
        self.list_widget.takeItem(self.list_widget.row(item))

    def show_path(self) -> None:
        item = self.list_widget.currentItem()
        if item is not None:
            path = item.data(Qt.ItemDataRole.UserRole)
            show_selected_path(path)

    def show_clear_items_dialog(self) -> None:
        result = show_question_dialog(self.clear_title, self.clear_items_text, self.main_window)
        if result:
            self.list_widget.clear()
            self.main_window.process_provider.selected_files.clear()
            self.main_window.processing_widget.reset_count_labels()
            self.accept()