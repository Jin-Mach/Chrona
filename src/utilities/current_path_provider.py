# Source - https://stackoverflow.com/a/13790741
# Posted by max, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-07, License - CC BY-SA 3.0

from pathlib import Path
import sys


# noinspection PyProtectedMember,PyUnresolvedReferences
def get_base_path() -> Path:
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent
    return base_path.resolve()
