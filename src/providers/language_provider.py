from typing import Any

from PyQt6.QtCore import QLocale

from src.providers.config_provider import ConfigProvider
from src.utilities.error_handler import Errorhandler


class LanguageProvider:
    name = ""
    language_code: str = ""
    supported_languages: list[str] = []
    config_data: dict[str, Any] = {}

    @classmethod
    def basic_setup(cls) -> None:
        cls.name = cls.__name__
        cls.config_data = ConfigProvider.get_config_data(class_name=cls.name)
        cls.language_code = cls.config_data.get("default_language", "en_GB")
        cls.supported_languages = cls.config_data.get("supported_languages", ["en_GB"])

    @classmethod
    def get_language_code(cls) -> str:
        try:
            current_code = QLocale().system().name()
            if current_code in cls.supported_languages:
                cls.language_code = current_code
        except Exception as e:
            Errorhandler.handle_error(cls.name, e)
        return cls.language_code