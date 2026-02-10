import requests

from src.utilities.error_handler import Errorhandler


def check_connection() -> bool:
    try:
        url = "https://github.com/Jin-Mach/Chrona"
        response = requests.get(url, timeout=3)
        if not response.ok:
            raise requests.exceptions.RequestException(f"HTTP status {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        Errorhandler.handle_error("ConnectionHandler", e)
        return False