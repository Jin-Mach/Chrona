import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QLabel, QSizePolicy, QLineEdit, \
    QGridLayout

from src.UI.widgets.drag_drop_widget import DragDropWidget
from src.providers.config_provider import ConfigProvider
from src.providers.language_provider import LanguageProvider
from src.utilities.error_handler import Errorhandler
from src.utilities.setup_handler import handle_ui_texts
from src.utilities.ui_helpers import set_lineedit_text

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


# noinspection PyAttributeOutsideInit
class ProcessingWidget(QWidget):
    DEFAULT_SPACING = 30

    def __init__(self, main_window: "MainWindow"):
        super().__init__(main_window)
        self.main_window = main_window
        self.setLayout(self.create_gui())
        self.set_ui_texts()
        self.set_config_data()

    def create_gui(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(self.DEFAULT_SPACING)
        main_layout.setContentsMargins(0, 0, 0, 0)
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_button = QPushButton()
        self.start_button.setObjectName("startButton")
        button_layout.addWidget(self.start_button)
        main_layout.addWidget(self.create_drag_group(), 2)
        main_layout.addWidget(self.create_path_group(), 1)
        main_layout.addWidget(self.create_details_group(), 1)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        return main_layout

    def create_drag_group(self) -> QGroupBox:
        drag_group = QGroupBox()
        drag_group.setObjectName("dragGroup")
        drag_layout = QVBoxLayout()
        drag_layout.setSpacing(self.DEFAULT_SPACING)
        drag_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drag_widget_layout = QHBoxLayout()
        self.drag_widget = DragDropWidget(self.main_window)
        drag_widget_layout.addStretch()
        drag_widget_layout.addWidget(self.drag_widget)
        drag_widget_layout.addStretch()
        self.drag_label = QLabel()
        self.drag_label.setObjectName("dragLabel")
        self.drag_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drag_layout.addLayout(drag_widget_layout)
        drag_layout.addWidget(self.drag_label)
        drag_group.setLayout(drag_layout)
        return drag_group

    def create_path_group(self) -> QGroupBox:
        path_group = QGroupBox()
        path_group.setObjectName("pathGroup")
        paths_layout = QVBoxLayout()
        paths_layout.setSpacing(self.DEFAULT_SPACING)
        grid = QGridLayout()
        grid.setHorizontalSpacing(self.DEFAULT_SPACING)
        grid.setVerticalSpacing(self.DEFAULT_SPACING)
        self.source_label = QLabel()
        self.source_label.setObjectName("sourceLabel")
        self.source_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setObjectName("inputPathEdit")
        self.input_path_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.input_path_select = QPushButton()
        self.input_path_select.setObjectName("inputPathSelect")
        self.input_path_select.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.input_path_add = QPushButton()
        self.input_path_add.setObjectName("inputPathAdd")
        self.input_path_add.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        grid.addWidget(self.source_label, 0, 0)
        grid.addWidget(self.input_path_edit, 0, 1)
        grid.addWidget(self.input_path_select, 0, 2)
        grid.addWidget(self.input_path_add, 0, 3)
        self.destination_label = QLabel()
        self.destination_label.setObjectName("destinationLabel")
        self.destination_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setObjectName("outputPathEdit")
        self.output_path_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.output_path_select = QPushButton()
        self.output_path_select.setObjectName("outputPathSelect")
        self.output_path_select.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        grid.addWidget(self.destination_label, 1, 0)
        grid.addWidget(self.output_path_edit, 1, 1)
        grid.addWidget(self.output_path_select, 1, 2)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)
        paths_layout.addLayout(grid)
        path_group.setLayout(paths_layout)
        return path_group

    def create_details_group(self) -> QGroupBox:
        details_group = QGroupBox()
        details_group.setObjectName("detailsGroup")
        details_layout = QVBoxLayout()
        details_layout.setSpacing(self.DEFAULT_SPACING)
        self.total_count_label = QLabel()
        self.total_count_label.setObjectName("totalCountLabel")
        self.folders_count_label = QLabel()
        self.folders_count_label.setObjectName("foldersCountLabel")
        self.files_count_label = QLabel()
        self.files_count_label.setObjectName("filesCountLabel")
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(self.DEFAULT_SPACING)
        self.show_items_button = QPushButton()
        self.show_items_button.setObjectName("showItemsButton")
        self.show_items_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.clear_items_button = QPushButton()
        self.clear_items_button.setObjectName("clearItemsButton")
        self.clear_items_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        buttons_layout.addWidget(self.show_items_button)
        buttons_layout.addWidget(self.clear_items_button)
        buttons_layout.addStretch()
        details_layout.addWidget(self.total_count_label)
        details_layout.addWidget(self.folders_count_label)
        details_layout.addWidget(self.files_count_label)
        details_layout.addLayout(buttons_layout)
        details_group.setLayout(details_layout)
        return details_group

    def set_ui_texts(self) -> None:
        try:
            texts_data = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__,
                                                         LanguageProvider.language_code)
            if not texts_data:
                raise IOError("texts data loading failed.")
            handle_ui_texts(self, texts_data, self.findChildren((QPushButton, QGroupBox, QLabel)))
            self.total_count_text = texts_data.get(self.total_count_label.objectName() + "Text", "Total:")
            self.total_count_value = 0
            self.folders_count_text = texts_data.get(self.folders_count_label.objectName() + "Text", "Folders:")
            self.folders_count_value = 0
            self.files_count_text = texts_data.get(self.files_count_label.objectName() + "Text", "Files:")
            self.files_count_value = 0
            self.total_count_label.setText(f"{self.total_count_text} {self.total_count_value}")
            self.folders_count_label.setText(f"{self.folders_count_text} {self.folders_count_value}")
            self.files_count_label.setText(f"{self.files_count_text} {self.files_count_value}")
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def set_config_data(self) -> None:
        try:
            config_data = ConfigProvider.get_config_data(self.__class__.__name__)
            if not config_data:
                raise IOError("config data loading failed.")
            self.input_path_edit.setReadOnly(True)
            self.output_path_edit.setReadOnly(True)
            self.update_input_path(config_data.get(self.__class__.__name__, {}).get("inputPathEdit", ""))
            self.update_output_path(config_data.get(self.__class__.__name__, {}).get("outputPathEdit", ""))
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def update_input_path(self, path: str) -> None:
        if path == "":
            path = pathlib.Path.home()
        self.full_input_path = pathlib.Path(path)
        set_lineedit_text(self.full_input_path, self.input_path_edit)

    def update_output_path(self, path: str) -> None:
        if path == "":
            path = pathlib.Path.home()
        self.full_output_path = pathlib.Path(path)
        set_lineedit_text(self.full_output_path, self.output_path_edit)

    def update_count_labels(self, folders_count: int = 0, files_count: int = 0) -> None:
        total_increment = folders_count + files_count
        self.total_count_value += total_increment
        self.folders_count_value += folders_count
        self.files_count_value += files_count
        self.total_count_label.setText(f"{self.total_count_text} {self.total_count_value}")
        self.folders_count_label.setText(f"{self.folders_count_text} {self.folders_count_value}")
        self.files_count_label.setText(f"{self.files_count_text} {self.files_count_value}")