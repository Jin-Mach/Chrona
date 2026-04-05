import json
import pathlib

from PyQt6.QtCore import QLocale

from src.providers.config_provider import ConfigProvider
from src.utilities.error_handler import Errorhandler


class LanguageProvider:

    @classmethod
    def basic_setup(cls, project_path: pathlib.Path) -> None:
        cls.project_path = project_path
        cls.config_data = ConfigProvider.get_config_data(class_name=cls.__name__)
        cls.supported_languages = cls.config_data.get("supported_languages", ["en_GB"])
        cls.default_code = cls.config_data.get("default_language", "en_GB")
        cls.language_code = cls.get_language_code()

    @classmethod
    def get_language_code(cls) -> str:
        try:
            current_code = QLocale().system().name()
            if current_code not in cls.supported_languages:
                return cls.default_code
            return current_code
        except Exception as e:
            Errorhandler.handle_error(cls.__name__, e)
            return cls.default_code

    @classmethod
    def get_widgets_texts(cls, widget_name: str, language_code: str | None = None) -> dict[str, str]:
        texts_data = {}
        try:
            if language_code is None:
                language_code = cls.language_code
            texts_path = cls.project_path.joinpath("resources", "texts", language_code, "ui_texts.json")
            if texts_path.exists() and texts_path.is_file():
                with texts_path.open("r", encoding="utf-8") as texts_file:
                    texts_data = json.load(texts_file).get(widget_name, {})
        except Exception as e:
            Errorhandler.handle_error(cls.__name__, e)
        return texts_data

    @classmethod
    def get_help_texts(cls, language_code: str | None = None) -> str:
        text = ""
        try:
            if language_code is None:
                language_code = cls.language_code
            help_text_path = cls.project_path.joinpath("resources", "texts", language_code, "help_text.html")
            if help_text_path.exists() and help_text_path.is_file():
                with help_text_path.open("r", encoding="utf-8") as help_text_file:
                    text = help_text_file.read()
        except Exception as e:
            Errorhandler.handle_error(cls.__name__, e)
        return text

    @classmethod
    def get_error_text(cls, language_code: str | None = None) -> dict[str, str]:
        errors_data = {}
        try:
            if language_code is None:
                language_code = cls.language_code
            errors_path = cls.project_path.joinpath("resources", "texts", language_code, "error_texts.json")
            if errors_path.exists() and errors_path.is_file():
                with errors_path.open("r", encoding="utf-8") as errors_file:
                    errors_data = json.load(errors_file)
        except Exception as e:
            Errorhandler.handle_error(cls.__name__, e)
        return errors_data