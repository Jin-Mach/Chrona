from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QLabel, QSizePolicy, QLineEdit, \
    QGridLayout

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class ProcessingWidget(QWidget):
    DEFAULT_SPACING = 20

    def __init__(self, main_window: "MainWindow"):
        super().__init__(main_window)
        self.main_window = main_window
        self.setLayout(self.create_gui())

    def create_gui(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(self.DEFAULT_SPACING)
        main_layout.setContentsMargins(0, 0, 0, 0)
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        button_layout.addWidget(self.start_button)
        main_layout.addWidget(self.create_drag_group())
        main_layout.addWidget(self.create_path_group())
        main_layout.addWidget(self.create_details_group())
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        return main_layout

    def create_drag_group(self) -> QGroupBox:
        drag_group = QGroupBox("Drag")
        drag_layout = QVBoxLayout()
        drag_layout.setSpacing(self.DEFAULT_SPACING)
        drag_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drag_widget_layout = QHBoxLayout()
        self.drag_widget = QWidget()
        self.drag_widget.setObjectName("dragWidget")
        self.drag_widget.setMinimumSize(QSize(150, 150))
        self.drag_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.drag_widget.setStyleSheet("""
        QWidget#dragWidget {
            border: 2px dashed #666;
            border-radius: 6px;
        }
        """)
        drag_widget_layout.addStretch()
        drag_widget_layout.addWidget(self.drag_widget)
        drag_widget_layout.addStretch()
        self.drag_label = QLabel("some drag text")
        self.drag_label.setObjectName("dragLabel")
        self.drag_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drag_layout.addLayout(drag_widget_layout)
        drag_layout.addWidget(self.drag_label)
        drag_group.setLayout(drag_layout)
        return drag_group

    def create_path_group(self) -> QGroupBox:
        path_group = QGroupBox("Path")
        paths_layout = QVBoxLayout()
        paths_layout.setSpacing(self.DEFAULT_SPACING)
        grid = QGridLayout()
        grid.setHorizontalSpacing(self.DEFAULT_SPACING)
        grid.setVerticalSpacing(self.DEFAULT_SPACING)
        self.source_label = QLabel("Source folder:")
        self.source_label.setObjectName("sourceLabel")
        self.source_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.input_path_edit = QLineEdit()
        self.input_path_edit.setObjectName("inputPathEdit")
        self.input_path_edit.setReadOnly(True)
        self.input_path_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.input_path_select = QPushButton("Select")
        self.input_path_select.setObjectName("inputPathSelect")
        self.input_path_select.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.input_path_add = QPushButton("Add")
        self.input_path_add.setObjectName("inputPathAdd")
        self.input_path_add.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        grid.addWidget(self.source_label, 0, 0)
        grid.addWidget(self.input_path_edit, 0, 1)
        grid.addWidget(self.input_path_select, 0, 2)
        grid.addWidget(self.input_path_add, 0, 3)
        self.destination_label = QLabel("Destination folder:")
        self.destination_label.setObjectName("destinationLabel")
        self.destination_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setObjectName("outputPathEdit")
        self.output_path_edit.setReadOnly(True)
        self.output_path_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.output_path_select = QPushButton("Select")
        self.output_path_select.setObjectName("outputPathSelect")
        self.output_path_select.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.output_path_add = QPushButton("Add")
        self.output_path_add.setObjectName("outputPathAdd")
        self.output_path_add.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        grid.addWidget(self.destination_label, 1, 0)
        grid.addWidget(self.output_path_edit, 1, 1)
        grid.addWidget(self.output_path_select, 1, 2)
        grid.addWidget(self.output_path_add, 1, 3)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)
        paths_layout.addLayout(grid)
        path_group.setLayout(paths_layout)
        return path_group

    def create_details_group(self) -> QGroupBox:
        details_group = QGroupBox("Details")
        details_layout = QVBoxLayout()
        details_layout.setSpacing(self.DEFAULT_SPACING)
        grid = QGridLayout()
        grid.setHorizontalSpacing(self.DEFAULT_SPACING)
        grid.setVerticalSpacing(self.DEFAULT_SPACING)
        self.files_count_label = QLabel("Files count:")
        self.files_count_label.setObjectName("filesCountLabel")
        self.files_count_value = QLabel("200")
        self.files_count_value.setObjectName("filesCountValue")
        self.files_size_label = QLabel("Size:")
        self.files_size_label.setObjectName("filesSizeLabel")
        self.files_size_value = QLabel("2,1 GB")
        self.files_size_value.setObjectName("filesSizeValue")
        self.files_type_label = QLabel("Included file types:")
        self.files_type_label.setObjectName("filesTypeLabel")
        self.files_type_value = QLabel("pdf, txt, docx, xlsx, jpg, png, img, csv, mp3, mp4 ..., abc,def, ghi, jkl")
        self.files_type_value.setObjectName("filesTypeValue")
        self.files_type_value.setWordWrap(True)
        self.files_type_value.setMinimumWidth(500)
        grid.addWidget(self.files_count_label, 0, 0)
        grid.addWidget(self.files_count_value, 0, 1)
        grid.addWidget(self.files_size_label, 1, 0)
        grid.addWidget(self.files_size_value, 1, 1)
        grid.addWidget(self.files_type_label, 2, 0, Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.files_type_value, 2, 1)
        buttons_layout = QVBoxLayout()
        buttons_layout.addStretch()
        self.show_files_button = QPushButton("Show Files")
        self.show_files_button.setObjectName("showFilesButton")
        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("clearButton")
        buttons_layout.addWidget(self.show_files_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addStretch()
        grid.addLayout(buttons_layout, 0, 2, 3, 1, alignment=Qt.AlignmentFlag.AlignRight)
        details_group.setLayout(grid)
        return details_group