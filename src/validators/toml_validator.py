import tomllib
import pathlib

from src.utilities.logging_provider import get_logger


class TomlValidator:
    logger = get_logger()

    @staticmethod
    def validate_config(file_path: pathlib.Path, structure: dict[str, set[str]]) -> bool:
        try:
            with file_path.open("rb") as file:
                data = tomllib.load(file)
            if not isinstance(data, dict):
                return False
            for section_name, required_keys in structure.items():
                if section_name not in data:
                    return False
                section = data[section_name]
                if not isinstance(section, dict):
                    return False
                if not required_keys.issubset(section.keys()):
                    return False
            return True
        except Exception as e:
            TomlValidator.logger.error(e)
            return False