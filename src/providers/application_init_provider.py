import pathlib

from src.providers.config_provider import ConfigProvider
from src.providers.file_provider import FileProvider
from src.providers.language_provider import LanguageProvider
from src.utilities.current_path_provider import set_project_path
from src.utilities.error_handler import Errorhandler


class ApplicationInitProvider:

    @staticmethod
    def initialize_application() -> bool:
        try:
            project_path = set_project_path()
            if project_path is None or not project_path.is_dir():
                raise FileNotFoundError("Default application directory not found")
            ApplicationInitProvider.basic_setup(project_path)
        except Exception as e:
            Errorhandler.handle_error(ApplicationInitProvider.__name__, e)
            return False
        return True

    @staticmethod
    def basic_setup(project_path: pathlib.Path) -> None:
        FileProvider.basic_setup(project_path)
        ConfigProvider.basic_setup(project_path)
        LanguageProvider.basic_setup(project_path)