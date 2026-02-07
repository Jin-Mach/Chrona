from src.utilities.current_path_provider import check_base_dir


class ApplicationInit:

    @staticmethod
    def initialize_application() -> bool:
        try:
            default_dir = check_base_dir()
            if default_dir is None:
                raise FileNotFoundError("Default application directory not found")
        except Exception as e:
            print(e)
            return False
        return True