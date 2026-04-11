import json
import pathlib

from src.utilities.logging_provider import get_logger


class JsonValidator:
    logger = get_logger()

    @staticmethod
    def validate_ui_texts(file_path: pathlib.Path, structure: dict[str, set[str]]) -> bool:
        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict):
                return False
            for section, keys in structure.items():
                if section not in data:
                    return False
                if not isinstance(data[section], dict):
                    return False
                for key in keys:
                    if key not in data[section]:
                        return False
            return True
        except Exception as e:
            JsonValidator.logger.error(e)
            return False

    @staticmethod
    def validate_error_texts(file_path: pathlib.Path, keys: set[str]) -> bool:
        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict):
                return False
            for key in keys:
                if key not in data:
                    return False
            return True
        except Exception as e:
            JsonValidator.logger.error(e)
            return False