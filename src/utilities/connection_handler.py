import requests


def check_connection() -> bool:
    try:
        url = "https://github.com/Jin-Mach/Chrona"
        response = requests.get(url, timeout=3)
        if not response.ok:
            raise
        return True
    except requests.exceptions.RequestException:
        return False