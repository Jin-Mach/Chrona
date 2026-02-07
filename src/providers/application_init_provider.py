from src.providers.language_provider import LanguageProvider
from src.utilities.current_path_provider import set_project_path
from src.utilities.error_handler import Errorhandler


class ApplicationInit:

    @staticmethod
    def initialize_application() -> bool:
        try:
            project_path = set_project_path()
            if project_path is None or not project_path.is_dir():
                raise FileNotFoundError("Default application directory not found")
            ApplicationInit.basic_setup()
        except Exception as e:
            Errorhandler.handle_error(ApplicationInit.__class__.__name__, e)
            return False
        return True

    @staticmethod
    def basic_setup() -> None:
        LanguageProvider.basic_setup()