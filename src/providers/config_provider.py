import pathlib
import shutil
import tomllib
import tomli_w

from typing import TYPE_CHECKING, Any

from src.utilities.error_handler import Errorhandler
from src.utilities.logging_provider import get_logger

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class ConfigProvider:

    @classmethod
    def basic_setup(cls, project_path: pathlib.Path) -> None:
        cls.project_path = project_path

    @staticmethod
    def get_config_data(class_name: str | None = None) -> dict[str, Any]:
        config_data = {}
        try:
            config_path = ConfigProvider.project_path.joinpath("config", "settings.toml")
            user_settings_path = ConfigProvider.project_path.joinpath("config", "user_settings.toml")
            if not user_settings_path.is_file():
                user_settings_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(config_path, user_settings_path)
            with config_path.open("rb") as default_file:
                default_config = tomllib.load(default_file)
            if user_settings_path.is_file():
                with user_settings_path.open("rb") as user_file:
                    user_config = tomllib.load(user_file)
            else:
                user_config = {}
            config_data = default_config.copy()
            config_data.update(user_config)
            if class_name is not None:
                config_data = config_data.get(class_name, {})
        except Exception as e:
            Errorhandler.handle_error(ConfigProvider.__name__, e)
        return config_data

    @staticmethod
    def save_config_data(main_window: "MainWindow") -> None:
        try:
            processing_map = {
                "inputPathEditPath": main_window.processing_widget.full_input_path,
                "outputPathEditPath": main_window.processing_widget.full_output_path
            }
            workflow_map = {
                "inputPathEditPath": main_window.processing_widget.full_input_path,
                "outputPathEditPath": main_window.processing_widget.full_output_path,
                "yearCheckboxState": main_window.workflow_settings.year_checkbox.isChecked(),
                "monthCheckboxState": main_window.workflow_settings.month_checkbox.isChecked(),
                "dayCheckboxState": main_window.workflow_settings.day_checkbox.isChecked(),
                "subfoldersTypeCheckboxState": main_window.workflow_settings.subfolders_type_checkbox.isChecked(),
                "hiddenFoldersCheckboxState": main_window.workflow_settings.hidden_folders_checkbox.isChecked(),
                "filterCheckboxState": main_window.workflow_settings.filter_checkbox.isChecked(),
                "documentsFilesCheckboxState": main_window.workflow_settings.documents_files_checkbox.isChecked(),
                "txtFilesCheckboxState": main_window.workflow_settings.txt_files_checkbox.isChecked(),
                "officeFilesCheckboxState": main_window.workflow_settings.office_files_checkbox.isChecked(),
                "imageFilesCheckboxState": main_window.workflow_settings.image_files_checkbox.isChecked(),
                "musicFilesCheckboxState": main_window.workflow_settings.music_files_checkbox.isChecked(),
                "archiveFilesCheckboxState": main_window.workflow_settings.archive_files_checkbox.isChecked(),
                "deleteFileCheckboxState": main_window.workflow_settings.delete_file_checkbox.isChecked(),
                "showFailedFilesCheckboxState": main_window.workflow_settings.show_failed_files.isChecked(),
            }
            user_settings_path = ConfigProvider.project_path.joinpath("config", "user_settings.toml")
            if not user_settings_path.is_file():
                raise IOError("User_settings file does not exist")
            with user_settings_path.open("rb") as user_settings_file:
                config_data = tomllib.load(user_settings_file)
            processing_section = config_data.setdefault("ProcessingWidget", {})
            workflow_section = config_data.setdefault("WorkflowSettings", {})
            for key, value in processing_map.items():
                if isinstance(value, pathlib.Path):
                    value = str(value)
                processing_section[key] = value
            for key, value in workflow_map.items():
                if isinstance(value, pathlib.Path):
                    value = str(value)
                workflow_section[key] = value
            with user_settings_path.open("wb") as user_settings_file:
                tomli_w.dump(config_data, user_settings_file)
        except Exception as e:
            logger = get_logger()
            logger.error(e)