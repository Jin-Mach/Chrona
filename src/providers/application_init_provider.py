import pathlib

from src.providers.config_provider import ConfigProvider
from src.providers.download_provider import DownloadProvider
from src.providers.file_provider import FileProvider
from src.providers.language_provider import LanguageProvider
from src.utilities.connection_handler import check_connection
from src.utilities.current_path_provider import set_project_path
from src.utilities.error_handler import Errorhandler


class ApplicationInitProvider:

    @staticmethod
    def initialize_application() -> bool:
        try:
            project_path = set_project_path()
            if project_path is None or not project_path.is_dir():
                raise FileNotFoundError("Default application directory not found")
            FileProvider.basic_setup(project_path)
            missing_files = FileProvider.check_missing_files()
            if any(missing_files.values()):
                if not check_connection():
                    raise ConnectionError("No internet connection to download missing files")
                if not DownloadProvider.download_files(missing_files):
                    raise ConnectionError(f"Download failed: {missing_files}")
            ApplicationInitProvider.basic_setup(project_path)
        except Exception as e:
            Errorhandler.handle_error(ApplicationInitProvider.__name__, e)
            return False
        return True

    @staticmethod
    def basic_setup(project_path: pathlib.Path) -> None:
        ConfigProvider.basic_setup(project_path)
        LanguageProvider.basic_setup(project_path)