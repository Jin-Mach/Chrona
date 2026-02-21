import pathlib
import os

from PyQt6.QtWidgets import QCheckBox, QLineEdit, QWidget


def set_lineedit_text(path: pathlib.Path, line_edit: QLineEdit, tooltip_duration: int = 5000) -> None:
    parts = path.parts
    display_text = str(path)
    if len(parts) > 2:
        display_text = f"{parts[0]}{parts[1]}...{parts[-2]}{os.sep}{parts[-1]}"
    line_edit.setText(display_text)
    line_edit.setToolTip(str(path))
    line_edit.setToolTipDuration(tooltip_duration)

def get_current_filter(widgets: list[QWidget], texts_data: dict[str, str]) -> str:
    final_filters = ""
    filters_config = {
        "documentsFilesCheckboxText": "*.pdf *.doc *.docx *.odt",
        "txtFilesCheckboxText": "*.txt *.log *.md",
        "officeFilesCheckboxText": "*.xls *.xlsx *.ppt *.pptx *.csv",
        "imageFilesCheckboxText": "*.jpg *.jpeg *.png *.bmp *.gif *.tiff",
        "musicFilesCheckboxText": "*.mp3 *.wav *.flac *.aac *.ogg",
        "archiveFilesCheckboxText": "*.zip *.rar *.7z *.tar *.gz",
    }
    for widget in widgets:
        if isinstance(widget, QCheckBox):
            if widget.isChecked() and widget.objectName() in filters_config:
                filter_text = texts_data.get(widget.objectName() + "Text", "N/A")
                final_filters += f"{filter_text} {filters_config.get(widget.objectName())};;"
        if isinstance(widget, QLineEdit):
            if widget.objectName() == "customExtensionsEdit" and widget.text():
                extension_filter = ""
                for extension in widget.text().split(","):
                    if extension.strip():
                        extension_filter += f"*.{extension.strip()} "
                if extension_filter:
                    filter_text = texts_data.get(widget.objectName() + "Text", "N/A")
                    final_filters += f"{filter_text} {extension_filter};;"
    if final_filters.strip().endswith(";;"):
        final_filters = final_filters[:-2]
    return final_filters.strip()