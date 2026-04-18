import os
import pathlib
import subprocess
import sys

from src.utils.error_handler import Errorhandler


def show_selected_path(path: pathlib.Path) -> None:
    try:
        if not path.exists():
            raise FileNotFoundError(f"{path} not found.")
        os_name = sys.platform
        if os_name == "win32":
            os.startfile(str(path))
        elif os_name == "darwin":
            subprocess.run(["open", "-R", str(path)], check=True)
        else:
            subprocess.run(["xdg-open", str(path)], check=True)
    except Exception as e:
        Errorhandler.handle_error("ShowSelectedPathHelper", e)