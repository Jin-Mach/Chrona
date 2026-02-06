from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QLayout, QVBoxLayout, QGroupBox, QCheckBox, QHBoxLayout, QLabel, QLineEdit, \
    QGridLayout, QRadioButton

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class SettingsWidget(QWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.setLayout(self.create_gui())
        self.basic_setup()
        self.create_connection()

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        folder_group = QGroupBox("Folder")
        folder_group.setObjectName("folderGroup")
        folder_layout = QVBoxLayout()
        self.year_checkbox = QCheckBox("Year")
        self.year_checkbox.setObjectName("yearCheckbox")
        month_layout = QHBoxLayout()
        self.month_checkbox = QCheckBox("Month")
        self.month_checkbox.setObjectName("monthCheckbox")
        month_layout.addSpacing(20)
        month_layout.addWidget(self.month_checkbox)
        folder_layout.addWidget(self.year_checkbox)
        folder_layout.addLayout(month_layout)
        folder_group.setLayout(folder_layout)
        filter_group = QGroupBox("Filter")
        filter_group.setObjectName("filterGroup")
        filter_layout = QVBoxLayout()
        self.filter_checkbox = QCheckBox("Filter")
        self.filter_checkbox.setObjectName("filterCheckbox")
        filter_files_layout = QVBoxLayout()
        files_label = QLabel("File types...")
        files_label.setObjectName("filesLabel")
        files_layout = QGridLayout()
        files_layout.setSpacing(20)
        files_layout.setContentsMargins(20, 0, 0, 0)
        self.documents_files_checkbox = QCheckBox("Documents")
        self.documents_files_checkbox.setObjectName("documentsCheckbox")
        self.txt_files_checkbox = QCheckBox("Texts")
        self.txt_files_checkbox.setObjectName("textsCheckbox")
        self.office_files_checkbox = QCheckBox("Office")
        self.office_files_checkbox.setObjectName("officeCheckbox")
        self.image_files_checkbox = QCheckBox("Images")
        self.image_files_checkbox.setObjectName("imagesCheckbox")
        self.music_files_checkbox = QCheckBox("Music")
        self.music_files_checkbox.setObjectName("musicCheckbox")
        self.archive_files_checkbox = QCheckBox("Archives")
        self.archive_files_checkbox.setObjectName("archiveCheckbox")
        files_layout.addWidget(self.documents_files_checkbox, 0, 0)
        files_layout.addWidget(self.txt_files_checkbox, 0, 1)
        files_layout.addWidget(self.office_files_checkbox, 0, 2)
        files_layout.addWidget(self.image_files_checkbox, 1, 0)
        files_layout.addWidget(self.music_files_checkbox, 1, 1)
        files_layout.addWidget(self.archive_files_checkbox, 1, 2)
        filter_files_layout.addWidget(files_label)
        filter_files_layout.addLayout(files_layout)
        filter_files_layout.addStretch()
        filter_layout.addWidget(self.filter_checkbox)
        filter_layout.addLayout(filter_files_layout)
        filter_group.setLayout(filter_layout)
        name_group = QGroupBox("Name")
        name_group.setObjectName("nameGroup")
        name_layout = QVBoxLayout()
        radio_layout = QHBoxLayout()
        self.default_name_radiobutton = QRadioButton("Default")
        self.default_name_radiobutton.setObjectName("defaultRadioButton")
        self.user_name_radiobutton = QRadioButton("User")
        self.user_name_radiobutton.setObjectName("userNameRadioButton")
        self.file_name_edit = QLineEdit()
        self.file_name_edit.setObjectName("fileNameEdit")
        radio_layout.addWidget(self.default_name_radiobutton)
        radio_layout.addWidget(self.user_name_radiobutton)
        name_layout.addLayout(radio_layout)
        name_layout.addWidget(self.file_name_edit)
        name_group.setLayout(name_layout)
        self.delete_file_checkbox = QCheckBox("Delete")
        self.delete_file_checkbox.setObjectName("deleteFileCheckbox")
        main_layout.addWidget(folder_group)
        main_layout.addWidget(filter_group)
        main_layout.addWidget(name_group)
        main_layout.addWidget(self.delete_file_checkbox)
        return main_layout

    def basic_setup(self) -> None:
        widget_names_true = ["yearCheckbox", "filterCheckbox", "documentsCheckbox", "textsCheckbox", "officeCheckbox",
                             "imagesCheckbox", "musicCheckbox","archiveCheckbox", "defaultRadioButton", "deleteFileCheckbox"]
        widgets_names_false = ["monthCheckbox", "userNameRadioButton", "fileNameEdit"]
        for widget in self.findChildren((QCheckBox, QRadioButton, QLineEdit)):
            if widget.objectName() in widget_names_true:
                if isinstance(widget, (QCheckBox, QRadioButton)):
                    widget.setChecked(True)
            elif widget.objectName() in widgets_names_false:
                if isinstance(widget, (QCheckBox, QRadioButton)):
                    widget.setChecked(False)
                elif isinstance(widget, QLineEdit):
                    widget.setEnabled(False)
            else:
                if isinstance(widget, (QCheckBox, QRadioButton)):
                    widget.setChecked(False)
                elif isinstance(widget, QLineEdit):
                    widget.setEnabled(False)

    def create_connection(self) -> None:
        files_checkboxes = [self.documents_files_checkbox, self.txt_files_checkbox, self.office_files_checkbox,
                            self.image_files_checkbox, self.music_files_checkbox, self.archive_files_checkbox]
        for checkbox in files_checkboxes:
            self.filter_checkbox.toggled.connect(checkbox.setEnabled)
        self.year_checkbox.toggled.connect(self.month_checkbox.setEnabled)
        self.user_name_radiobutton.toggled.connect(self.file_name_edit.setEnabled)