import pathlib

from src.validators.json_validator import JsonValidator
from src.validators.toml_validator import TomlValidator


class FileProvider:

    @classmethod
    def basic_setup(cls, project_path: pathlib.Path):
        cls.project_path = project_path
        cls.config_path = project_path.joinpath("config")
        cls.resources_path = project_path.joinpath("resources")

        cls.required_files = {
            "config": {
                cls.config_path.joinpath("settings.toml"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/main/config/settings.toml"
            },
            "resources": {
                cls.resources_path.joinpath("texts", "cs_CZ", "ui_texts.json"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/main/resources/texts/cs_CZ/ui_texts.json",
                cls.resources_path.joinpath("texts", "en_GB", "ui_texts.json"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/main/resources/texts/en_GB/ui_texts.json",
                cls.resources_path.joinpath("texts", "cs_CZ", "error_texts.json"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/main/resources/texts/cs_CZ/error_texts.json",
                cls.resources_path.joinpath("texts", "en_GB", "error_texts.json"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/main/resources/texts/en_GB/error_texts.json",
                cls.resources_path.joinpath("texts", "cs_CZ", "help_text.html"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/main/resources/texts/cs_CZ/help_text.html",
                cls.resources_path.joinpath("texts", "en_GB", "help_text.html"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/main/resources/texts/en_GB/help_text.html",
                cls.resources_path.joinpath("images", "splash_pixmap.jpg"):
                    "https://raw.githubusercontent.com/Jin-Mach/Chrona/main/resources/images/splash_pixmap.jpg"
            }
        }

    SETTINGS_SECTIONS = {
        "LanguageProvider",
        "ProcessingWidget",
        "WorkflowSettings",
        "HelpWidget"
    }

    TEXTS_STRUCTURE = {
        "MainWindow": {
            "titleText"
        },

        "SidePanel": {
            "processingButtonText",
            "processingButtonTooltipText",
            "workflowSettingsButtonText",
            "workflowSettingsButtonTooltipText",
            "helpButtonText",
            "helpButtonTooltipText",
            "aboutButtonText",
            "aboutButtonTooltipText"
        },

        "ProcessingWidget": {
            "startButtonText",
            "startButtonTooltipText",
            "dragGroupText",
            "dragLabelText",
            "pathGroupText",
            "sourceLabelText",
            "inputPathSelectText",
            "inputPathSelectTooltipText",
            "inputPathAddText",
            "inputPathAddTooltipText",
            "destinationLabelText",
            "outputPathSelectText",
            "outputPathSelectTooltipText",
            "detailsGroupText",
            "totalCountLabelText",
            "foldersCountLabelText",
            "filesCountLabelText",
            "showItemsButtonText",
            "showItemsButtonTooltipText",
            "clearItemsButtonText",
            "clearItemsButtonTooltipText",
            "titleText",
            "messageText",
            "questionTitleText",
            "clearItemText"
        },

        "WorkflowSettings": {
            "sourceLabelText",
            "inputPathBrowseText",
            "inputPathBrowseTooltipText",
            "destinationLabelText",
            "outputPathBrowseText",
            "outputPathBrowseTooltipText",
            "folderGroupText",
            "yearCheckboxText",
            "monthCheckboxText",
            "dayCheckboxText",
            "subfoldersTypeCheckboxText",
            "hiddenFoldersCheckboxText",
            "filterGroupText",
            "filterCheckboxText",
            "documentsFilesCheckboxText",
            "txtFilesCheckboxText",
            "officeFilesCheckboxText",
            "imageFilesCheckboxText",
            "musicFilesCheckboxText",
            "archiveFilesCheckboxText",
            "customExtensionsLabelText",
            "customExtensionsEditPlaceholderText",
            "customExtensionsEditText",
            "nameGroupText",
            "defaultNameRadiobuttonText",
            "userNameRadiobuttonText",
            "fileNameEditText",
            "useTimestampCheckboxText",
            "useCounterCheckboxText",
            "optionsGroupText",
            "deleteFileCheckboxText",
            "overwriteFileCheckboxText",
            "showFailedFilesCheckboxText"
        },

        "ErrorDialog": {
            "titleText",
            "showHideButtonText",
            "closeButtonText"
        },

        "FileDialog": {
            "documentsFilesCheckboxText",
            "txtFilesCheckboxText",
            "officeFilesCheckboxText",
            "imageFilesCheckboxText",
            "musicFilesCheckboxText",
            "archiveFilesCheckboxText",
            "customExtensionsEditText"
        },

        "ProcessProvider": {
            "titleText",
            "messageText",
            "questionTitleText",
            "questionMessageText",
            "documentsFiles",
            "documentsSuffixes",
            "txtFiles",
            "txtSuffixes",
            "officeFiles",
            "officeSuffixes",
            "imageFiles",
            "imageSuffixes",
            "musicFiles",
            "musicSuffixes",
            "archiveFiles",
            "archiveSuffixes",
            "othersFiles"
        },

        "ProgressDialog": {
            "titleLabelText",
            "progressText",
            "cancelProgressButtonText",
            "cancelProgressButtonTooltipText"
        },

        "NotificationDialog": {
            "infoLabelText",
            "processedText",
            "failedText",
            "loadingLabelText"
        },

        "FailedListDialog": {
            "titleLabelText",
            "countLabelText",
            "showPathButtonText",
            "closeButtonText"
        },

        "SelectedItemsDialog": {
            "titleLabelText",
            "showPathButtonText",
            "clearItemsButtonText",
            "clearItemsButtonTooltipText",
            "closeButtonText",
            "itemButtonText",
            "questionTitleText",
            "clearItemText"
        },

        "AboutDialog": {
            "titleLabelText",
            "textLabelText",
            "closeButtonText"
        }
    }

    ERROR_TEXTS_KEYS = {
        "IOError",
        "PermissionError",
        "OSError",
        "FileNotFoundError",
        "ConnectionError",
        "ValueError",
        "TypeError",
        "KeyError",
        "IndexError",
        "AttributeError",
        "ZeroDivisionError",
        "RuntimeError",
        "ImportError",
        "ModuleNotFoundError",
        "NameError",
        "StopIteration",
        "MemoryError",
        "AssertionError",
        "RecursionError",
        "FloatingPointError",
        "TimeoutError",
        "UnknownError"
    }

    @classmethod
    def check_missing_files(cls) -> dict[str, dict[pathlib.Path, str]]:
        missing_files = {}
        for path in (cls.config_path, cls.resources_path):
            path.mkdir(parents=True, exist_ok=True)
        for category, files in cls.required_files.items():
            missing_files[category] = {}
            for file, url in files.items():
                if not file.exists() or file.stat().st_size == 0:
                    missing_files[category][file] = url
                    continue
                if file.suffix == ".toml":
                    if not TomlValidator.validate_config(file, cls.SETTINGS_SECTIONS):
                        missing_files[category][file] = url
                    continue
                if "error_texts" in file.name:
                    if not JsonValidator.validate_error_texts(file, cls.ERROR_TEXTS_KEYS):
                        missing_files[category][file] = url
                    continue
                if "ui_texts" in file.name:
                    if not JsonValidator.validate_ui_texts(file, cls.TEXTS_STRUCTURE):
                        missing_files[category][file] = url
                    continue
        return missing_files