import json
import pathlib
import tomllib

from src.utilities.error_handler import Errorhandler


class FileProvider:

    @classmethod
    def basic_setup(cls, project_path: pathlib.Path):
        cls.project_path = project_path
        cls.config_path = project_path.joinpath("config")
        cls.resources_path = project_path.joinpath("resources")
        cls.required_files = {
            "config": {
                cls.config_path.joinpath("settings.toml"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/refs/heads/main/config/settings.toml"
            },
            "resources": {
                cls.resources_path.joinpath("texts", "cs_CZ", "ui_texts.json"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/refs/heads/main/resources/texts/cs_CZ/ui_texts.json",
                cls.resources_path.joinpath("texts", "en_GB", "ui_texts.json"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/refs/heads/main/resources/texts/en_GB/ui_texts.json",
                cls.resources_path.joinpath("texts", "cs_CZ", "error_texts.json"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/refs/heads/main/resources/texts/cs_CZ/error_texts.json",
                cls.resources_path.joinpath("texts", "en_GB", "error_texts.json"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/refs/heads/main/resources/texts/en_GB/error_texts.json"
            }
        }

    SETTINGS_KEYS = [
        "LanguageProvider",
        "default_language", "supported_languages",
        "ProcessingWidget",
        "inputPathEditPath", "outputPathEditPath",
        "WorkflowSettings",
        "inputPathEditPath", "outputPathEditPath",
        "yearCheckboxState", "monthCheckboxState", "dayCheckboxState", "createSubfoldersDateCheckboxState",
        "createSubfoldersTypeCheckboxState", "includeHiddenFoldersCheckboxState", "filterCheckboxState",
        "documentsFilesCheckboxState", "txtFilesCheckboxState", "officeFilesCheckboxState", "imageFilesCheckboxState",
        "musicFilesCheckboxState", "archiveFilesCheckboxState", "useTimestampCheckboxState", "useCounterCheckboxState",
        "deleteFileCheckboxState", "moveInsteadCopyCheckboxState", "overwriteCheckboxState", "defaultNameRadiobuttonState",
        "userNameRadiobuttonState"
    ]

    TEXTS_KEYS = [
        "MainWindow",
        "titleText", "titleTextFolder",
        "SidePanel",
        "processingButtonText", "processingButtonTooltipText", "workflowSettingsButtonText", "workflowSettingsButtonTooltipText",
        "ProcessingWidget",
        "startButtonText", "startButtonTooltipText", "dragGroupText", "dragLabelText", "pathGroupText",
        "sourceLabelText", "inputPathSelectText", "inputPathSelectTooltipText", "inputPathAddText",
        "inputPathAddTooltipText", "destinationLabelText", "outputPathSelectText",
        "outputPathSelectTooltipText", "detailsGroupText", "filesCountLabelText", "filesSizeLabelText",
        "filesTypeLabelText", "showFilesButtonText", "showFilesButtonTooltipText", "clearButtonText",
        "clearButtonTooltipText",
        "WorkflowSettings",
        "sourceLabelText", "inputPathBrowseText",
        "inputPathBrowseTooltipText", "destinationLabelText", "outputPathBrowseText",
        "outputPathBrowseTooltipText", "folderGroupText", "yearCheckboxText", "monthCheckboxText",
        "dayCheckboxText", "createSubfoldersDateCheckboxText", "createSubfoldersTypeCheckboxText",
        "includeHiddenFoldersCheckboxText", "filterGroupText", "filterCheckboxText",
        "documentsFilesCheckboxText", "txtFilesCheckboxText", "officeFilesCheckboxText",
        "imageFilesCheckboxText", "musicFilesCheckboxText", "archiveFilesCheckboxText",
        "customExtensionsLabelText", "customExtensionsEditPlaceholderText", "customExtensionsEditText", "nameGroupText",
        "defaultNameRadiobuttonText", "userNameRadiobuttonText", "fileNameEditText",
        "useTimestampCheckboxText", "useCounterCheckboxText", "actionsGroupText", "deleteFileCheckboxText",
        "moveInsteadCopyCheckboxText", "overwriteCheckboxText",
        "ErrorDialog",
        "titleText", "showHideButtonText", "closeButtonText"
        "FileDialog",
        "documentsFilesCheckboxText", "txtFilesCheckboxText", "officeFilesCheckboxText", "imageFilesCheckboxText",
        "musicFilesCheckboxText", "archiveFilesCheckboxText", "customExtensionsEditText",
        "ProcessProvider",
        "titleText", "messageText", "documentsFiles", "documentsSuffixes", "txtFiles", "txtSuffixes",
        "officeFiles", "officeSuffixes", "imageFiles", "imageSuffixes", "musicFiles", "musicSuffixes",
        "archiveFiles", "archiveSuffixes", "othersFiles"
    ]

    @classmethod
    def check_missing_files(cls) -> dict[str, dict[pathlib.Path, str]]:
        missing_files = {}
        try:
            for path in (cls.config_path, cls.resources_path):
                path.mkdir(parents=True, exist_ok=True)
            for category in cls.required_files:
                missing_files[category] = {}
                for file, url in cls.required_files[category].items():
                    if not file.exists() or file.stat().st_size == 0:
                        missing_files[category][file] = url
                    suffix = file.suffix.lower()
                    if suffix == ".toml":
                        if not cls.check_keys(file, cls.SETTINGS_KEYS, file_type="toml"):
                            missing_files[category][file] = url
                    if suffix == ".json":
                        if not cls.check_keys(file, cls.TEXTS_KEYS, file_type="json"):
                            missing_files[category][file] = url
            return missing_files
        except Exception as e:
            Errorhandler.handle_error(cls.__name__, e)
            return cls.required_files

    @classmethod
    def check_keys(cls, file_path: pathlib.Path, keys: list[str], file_type: str) -> bool:
        try:
            if file_type == "toml":
                with file_path.open("rb") as f:
                    data = tomllib.load(f)
            elif file_type == "json":
                with file_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            for key, value in data.items():
                if key not in keys or value in ["", {}, [], None]:
                    return False
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if sub_key not in keys or sub_value == "":
                            return False
            return True
        except Exception as e:
            Errorhandler.handle_error(cls.__name__, e)
            return False