import pathlib
import requests

from src.utilities.error_handler import Errorhandler


class DownloadProvider:

    @classmethod
    def download_files(cls, missing_files: dict[str, dict[pathlib.Path, str]]) -> bool:
        try:
            for _, value in missing_files.items():
                for sub_key, sub_value in value.items():
                    cls.download_file(sub_key, sub_value)
            return True
        except Exception as e:
            Errorhandler.handle_error(cls.__name__, e)
            return False

    @classmethod
    def download_file(cls, path: pathlib.Path, url: str) -> bool:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(response.content)
            return True
        except Exception as e:
            Errorhandler.handle_error(cls.__name__, e)
            return False