import tomllib
import pathlib

from src.utilities.logging_provider import get_logger


class TomlValidator:
    logger = get_logger()

    @staticmethod
    def validate_config(file_path: pathlib.Path, required_sections: set[str]) -> bool:
        try:
            with file_path.open("rb") as file:
                data = tomllib.load(file)
            if not isinstance(data, dict):
                return False
            for section in required_sections:
                if section not in data:
                    return False
            return True
        except Exception as e:
            TomlValidator.logger.error(e)
            return False