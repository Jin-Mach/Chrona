import pathlib
import os


def set_lineedit_text(path: pathlib.Path, line_edit, tooltip_duration: int = 5000) -> None:
    parts = path.parts
    display_text = str(path)
    if len(parts) > 2:
        display_text = f"{parts[0]}{parts[1]}...{parts[-2]}{os.sep}{parts[-1]}"
    line_edit.setText(display_text)
    line_edit.setToolTip(str(path))
    line_edit.setToolTipDuration(tooltip_duration)