import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox, QRadioButton, QLineEdit,
                             QPushButton, QGridLayout, QLabel, QSizePolicy)

from src.providers.config_provider import ConfigProvider
from src.providers.language_provider import LanguageProvider
from src.utilities.error_handler import Errorhandler
from src.utilities.setup_handler import handle_ui_texts, handle_ui_widgets
from src.utilities.ui_helpers import set_lineedit_text

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


# noinspection PyAttributeOutsideInit
class WorkflowSettings(QWidget):
    DEFAULT_SPACING = 10

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.setLayout(self.create_gui())
        self.set_ui_texts()
        self.set_config_data()
        self.set_validators()
        self.create_connection()

    def create_gui(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(self.DEFAULT_SPACING)
        main_layout.addLayout(self.create_paths_section())
        top_groups_layout = QHBoxLayout()
        top_groups_layout.addWidget(self.create_folder_group())
        top_groups_layout.addWidget(self.create_filter_group())
        top_groups_layout.setStretch(0, 1)
        top_groups_layout.setStretch(1, 1)
        main_layout.addLayout(top_groups_layout)
        bottom_groups_layout = QHBoxLayout()
        bottom_groups_layout.addWidget(self.create_name_group())
        bottom_groups_layout.addWidget(self.create_options_group())
        bottom_groups_layout.setStretch(0, 1)
        bottom_groups_layout.setStretch(1, 1)
        main_layout.addLayout(bottom_groups_layout)
        return main_layout

    def create_paths_section(self) -> QVBoxLayout:
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
        self.input_path_browse = QPushButton()
        self.input_path_browse.setObjectName("inputPathBrowse")
        self.input_path_browse.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        grid.addWidget(self.source_label, 0, 0)
        grid.addWidget(self.input_path_edit, 0, 1)
        grid.addWidget(self.input_path_browse, 0, 2)
        self.destination_label = QLabel()
        self.destination_label.setObjectName("destinationLabel")
        self.destination_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setObjectName("outputPathEdit")
        self.output_path_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.output_path_browse = QPushButton()
        self.output_path_browse.setObjectName("outputPathBrowse")
        self.output_path_browse.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        grid.addWidget(self.destination_label, 1, 0)
        grid.addWidget(self.output_path_edit, 1, 1)
        grid.addWidget(self.output_path_browse, 1, 2)
        grid.setColumnStretch(0, 0)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 0)
        paths_layout.addLayout(grid)
        return paths_layout

    def create_folder_group(self) -> QGroupBox:
        self.folder_group = QGroupBox()
        self.folder_group.setObjectName("folderGroup")
        self.folder_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout = QVBoxLayout()
        layout.setSpacing(self.DEFAULT_SPACING)
        self.year_checkbox = QCheckBox()
        self.year_checkbox.setObjectName("yearCheckbox")
        layout.addWidget(self.year_checkbox)
        month_layout = QHBoxLayout()
        month_layout.addSpacing(self.DEFAULT_SPACING)
        self.month_checkbox = QCheckBox()
        self.month_checkbox.setObjectName("monthCheckbox")
        month_layout.addWidget(self.month_checkbox)
        layout.addLayout(month_layout)
        day_layout = QHBoxLayout()
        day_layout.addSpacing(40)
        self.day_checkbox = QCheckBox()
        self.day_checkbox.setObjectName("dayCheckbox")
        day_layout.addWidget(self.day_checkbox)
        layout.addLayout(day_layout)
        self.subfolders_type_checkbox = QCheckBox()
        self.subfolders_type_checkbox.setObjectName("subfoldersTypeCheckbox")
        layout.addWidget(self.subfolders_type_checkbox)
        self.hidden_folders_checkbox = QCheckBox()
        self.hidden_folders_checkbox.setObjectName("hiddenFoldersCheckbox")
        layout.addWidget(self.hidden_folders_checkbox)
        layout.addStretch()
        self.folder_group.setLayout(layout)
        return self.folder_group

    def create_filter_group(self) -> QGroupBox:
        self.filter_group = QGroupBox()
        self.filter_group.setObjectName("filterGroup")
        self.filter_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout = QVBoxLayout()
        layout.setSpacing(self.DEFAULT_SPACING)
        self.filter_checkbox = QCheckBox()
        self.filter_checkbox.setObjectName("filterCheckbox")
        files_layout = QGridLayout()
        self.documents_files_checkbox = QCheckBox()
        self.documents_files_checkbox.setObjectName("documentsFilesCheckbox")
        self.txt_files_checkbox = QCheckBox()
        self.txt_files_checkbox.setObjectName("txtFilesCheckbox")
        self.office_files_checkbox = QCheckBox()
        self.office_files_checkbox.setObjectName("officeFilesCheckbox")
        self.image_files_checkbox = QCheckBox()
        self.image_files_checkbox.setObjectName("imageFilesCheckbox")
        self.music_files_checkbox = QCheckBox()
        self.music_files_checkbox.setObjectName("musicFilesCheckbox")
        self.archive_files_checkbox = QCheckBox()
        self.archive_files_checkbox.setObjectName("archiveFilesCheckbox")
        files_layout.addWidget(self.documents_files_checkbox, 0, 0)
        files_layout.addWidget(self.txt_files_checkbox, 0, 1)
        files_layout.addWidget(self.office_files_checkbox, 0, 2)
        files_layout.addWidget(self.image_files_checkbox, 1, 0)
        files_layout.addWidget(self.music_files_checkbox, 1, 1)
        files_layout.addWidget(self.archive_files_checkbox, 1, 2)
        self.custom_extensions_label = QLabel()
        self.custom_extensions_label.setObjectName("customExtensionsLabel")
        self.custom_extensions_edit = QLineEdit()
        self.custom_extensions_edit.setObjectName("customExtensionsEdit")
        layout.addWidget(self.filter_checkbox)
        layout.addLayout(files_layout)
        layout.addWidget(self.custom_extensions_label)
        layout.addWidget(self.custom_extensions_edit)
        layout.addStretch()
        self.filter_group.setLayout(layout)
        return self.filter_group

    def create_name_group(self) -> QGroupBox:
        self.name_group = QGroupBox()
        self.name_group.setObjectName("nameGroup")
        self.name_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout = QVBoxLayout()
        layout.setSpacing(self.DEFAULT_SPACING)
        radio_layout = QHBoxLayout()
        self.default_name_radiobutton = QRadioButton()
        self.default_name_radiobutton.setObjectName("defaultNameRadiobutton")
        self.user_name_radiobutton = QRadioButton()
        self.user_name_radiobutton.setObjectName("userNameRadiobutton")
        radio_layout.addWidget(self.default_name_radiobutton)
        radio_layout.addWidget(self.user_name_radiobutton)
        self.file_name_edit = QLineEdit()
        self.file_name_edit.setObjectName("fileNameEdit")
        self.use_timestamp_checkbox = QCheckBox()
        self.use_timestamp_checkbox.setObjectName("useTimestampCheckbox")
        self.use_counter_checkbox = QCheckBox()
        self.use_counter_checkbox.setObjectName("useCounterCheckbox")
        layout.addLayout(radio_layout)
        layout.addWidget(self.file_name_edit)
        layout.addWidget(self.use_timestamp_checkbox)
        layout.addWidget(self.use_counter_checkbox)
        layout.addStretch()
        self.name_group.setLayout(layout)
        return self.name_group

    def create_options_group(self) -> QGroupBox:
        self.options_group = QGroupBox()
        self.options_group.setObjectName("optionsGroup")
        self.options_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        layout = QVBoxLayout()
        layout.setSpacing(self.DEFAULT_SPACING)
        timestamp_layout = QHBoxLayout()
        self.modified_radiobutton = QRadioButton()
        self.modified_radiobutton.setObjectName("modifiedRadiobutton")
        self.created_radiobutton = QRadioButton()
        self.created_radiobutton.setObjectName("createdRadiobutton")
        timestamp_layout.addWidget(self.modified_radiobutton)
        timestamp_layout.addWidget(self.created_radiobutton)
        self.delete_file_checkbox = QCheckBox()
        self.delete_file_checkbox.setObjectName("deleteFileCheckbox")
        self.show_failed_files = QCheckBox()
        self.show_failed_files.setObjectName("showFailedFilesCheckbox")
        layout.addLayout(timestamp_layout)
        layout.addWidget(self.delete_file_checkbox)
        layout.addWidget(self.show_failed_files)
        layout.addStretch()
        self.options_group.setLayout(layout)
        return self.options_group

    def set_ui_texts(self) -> None:
        try:
            texts_data = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__,
                                                         LanguageProvider.language_code)
            if not texts_data:
                raise IOError("Texts data loading failed.")
            handle_ui_texts(self, texts_data, self.findChildren((QGroupBox, QCheckBox, QRadioButton, QLineEdit,
                                                                QPushButton, QGridLayout, QLabel)))
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def set_config_data(self) -> None:
        try:
            config_data = ConfigProvider.get_config_data(self.__class__.__name__)
            if not config_data:
                raise IOError("Config data loading failed.")
            handle_ui_widgets(config_data, self.findChildren((QLineEdit, QCheckBox, QRadioButton)))
            self.update_input_path(config_data.get(self.__class__.__name__, {}).get("inputPathEdit", ""))
            self.update_output_path(config_data.get(self.__class__.__name__, {}).get("outputPathEdit", ""))
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def set_validators(self) -> None:
        extension_regex = QRegularExpression(r"[A-Za-z0-9;]*")
        extension_validator = QRegularExpressionValidator(extension_regex)
        name_regex = QRegularExpression(r"[A-Za-z0-9_]*")
        name_validator = QRegularExpressionValidator(name_regex)
        self.custom_extensions_edit.setValidator(extension_validator)
        self.file_name_edit.setValidator(name_validator)

    def create_connection(self) -> None:
        self.filter_checkbox.toggled.connect(self.update_filter_options)
        self.year_checkbox.toggled.connect(self.update_folder_logic)
        self.month_checkbox.toggled.connect(self.update_folder_logic)
        self.default_name_radiobutton.toggled.connect(self.update_name_options)
        self.user_name_radiobutton.toggled.connect(self.update_name_options)
        self.use_timestamp_checkbox.toggled.connect(lambda _: self.validate_name_options(self.use_timestamp_checkbox))
        self.use_counter_checkbox.toggled.connect(lambda _: self.validate_name_options(self.use_counter_checkbox))
        self.delete_file_checkbox.toggled.connect(self.delete_toggled)
        self.show_failed_files.toggled.connect(self.move_toggled)

    def active_filter(self) -> dict[str, bool | str]:
        return {
            "year": self.year_checkbox.isChecked(),
            "month": self.month_checkbox.isChecked(),
            "day": self.day_checkbox.isChecked(),
            "type_subfolder": self.subfolders_type_checkbox.isChecked(),
            "hidden_folders": self.hidden_folders_checkbox.isChecked(),
            "default_name": self.default_name_radiobutton.isChecked(),
            "custom_name": self.file_name_edit.text().strip(),
            "timestamp": self.use_timestamp_checkbox.isChecked(),
            "counter": self.use_counter_checkbox.isChecked(),
            "main_filter": self.filter_checkbox.isChecked(),
            "documents_filter": self.documents_files_checkbox.isChecked(),
            "txt_filter": self.txt_files_checkbox.isChecked(),
            "office_filter": self.office_files_checkbox.isChecked(),
            "image_filter": self.image_files_checkbox.isChecked(),
            "music_filter": self.music_files_checkbox.isChecked(),
            "archive_filter": self.archive_files_checkbox.isChecked(),
            "custom_extensions": self.custom_extensions_edit.text().strip(),
            "file_modified": self.modified_radiobutton.isChecked(),
            "file_created": self.created_radiobutton.isChecked(),
            "delete_file": self.delete_file_checkbox.isChecked(),
            "failed_files": self.show_failed_files.isChecked()
        }

    def update_folder_logic(self) -> None:
        if not self.year_checkbox.isChecked():
            self.month_checkbox.setChecked(False)
            self.month_checkbox.setEnabled(False)
            self.day_checkbox.setChecked(False)
            self.day_checkbox.setEnabled(False)
        else:
            self.month_checkbox.setEnabled(True)
            if not self.month_checkbox.isChecked():
                self.day_checkbox.setChecked(False)
                self.day_checkbox.setEnabled(False)
            else:
                self.day_checkbox.setEnabled(True)

    def update_name_options(self) -> None:
        user_checked = self.user_name_radiobutton.isChecked()
        self.file_name_edit.setEnabled(user_checked)
        self.use_timestamp_checkbox.setEnabled(user_checked)
        self.use_counter_checkbox.setEnabled(user_checked)
        if not user_checked:
            self.use_counter_checkbox.setChecked(False)
            self.use_timestamp_checkbox.setChecked(False)
            self.use_counter_checkbox.setEnabled(False)
        else:
            self.file_name_edit.setFocus()
            self.file_name_edit.selectAll()
            self.use_timestamp_checkbox.setChecked(True)

    def validate_name_options(self, changed_checkbox: QCheckBox) -> None:
        if self.user_name_radiobutton.isChecked():
            if changed_checkbox == self.use_timestamp_checkbox:
                other_checkbox = self.use_counter_checkbox
            else:
                other_checkbox = self.use_timestamp_checkbox
            if not changed_checkbox.isChecked() and not other_checkbox.isChecked():
                changed_checkbox.setChecked(True)

    def update_filter_options(self) -> None:
        files_checkboxes = [self.documents_files_checkbox, self.txt_files_checkbox, self.office_files_checkbox,
                            self.image_files_checkbox, self.music_files_checkbox, self.archive_files_checkbox]
        if self.filter_checkbox.isChecked():
            for checkbox in files_checkboxes:
                checkbox.setChecked(True)
                checkbox.setEnabled(True)
        else:
            for checkbox in files_checkboxes:
                checkbox.setChecked(False)
                checkbox.setEnabled(False)
        self.custom_extensions_edit.setDisabled(self.filter_checkbox.isChecked())

    def delete_toggled(self) -> None:
        if self.delete_file_checkbox.isChecked():
            self.show_failed_files.setChecked(False)

    def move_toggled(self) -> None:
        if self.show_failed_files.isChecked():
            self.delete_file_checkbox.setChecked(False)

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