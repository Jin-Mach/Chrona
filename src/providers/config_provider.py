import tomllib

from typing import Any

from src.utilities.current_path_provider import set_project_path
from src.utilities.error_handler import Errorhandler


class ConfigProvider:
    project_path = set_project_path()

    @staticmethod
    def get_config_data(class_name: str | None = None) -> dict[str, Any]:
        config_data = {}
        try:
            config_path = ConfigProvider.project_path.joinpath("config", "settings.toml")
            if not config_path.exists() or not config_path.is_file():
                raise FileNotFoundError(f"Config file {config_path} loading failed")
            with open(config_path, "rb") as config_file:
                config_data = tomllib.load(config_file)
            if class_name is not None:
                config_data = config_data.get(class_name, {})
        except Exception as e:
            Errorhandler.handle_error(ConfigProvider.__class__.__name__, e)
        return config_data