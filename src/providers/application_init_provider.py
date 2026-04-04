import pathlib

from PyQt6.QtWidgets import QApplication

from src.providers.config_provider import ConfigProvider
from src.providers.download_provider import DownloadProvider
from src.providers.file_provider import FileProvider
from src.providers.language_provider import LanguageProvider
from src.utilities.connection_handler import check_connection
from src.utilities.current_path_provider import set_project_path
from src.utilities.error_handler import Errorhandler
from src.utilities.style_provider import set_application_style


class ApplicationInitProvider:
    APP_NAME = "Chrona"
    APP_VERSION = "1.0.0"
    ORGANIZATION_NAME = "Jin-Mach"

    @classmethod
    def initialize_application(cls, application: QApplication) -> bool:
        try:
            application.setOrganizationName(cls.ORGANIZATION_NAME)
            application.setApplicationName(cls.APP_NAME)
            application.setApplicationVersion(cls.APP_VERSION)
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
            set_application_style(application)
        except Exception as e:
            Errorhandler.handle_error(ApplicationInitProvider.__name__, e)
            return False
        return True

    @staticmethod
    def basic_setup(project_path: pathlib.Path) -> None:
        ConfigProvider.basic_setup(project_path)
        LanguageProvider.basic_setup(project_path)