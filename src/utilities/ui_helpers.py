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
    existing_filters = set()
    filters_config = {
        "documentsFilesCheckboxText": "*.pdf *.doc *.docx *.odt",
        "txtFilesCheckboxText": "*.txt *.log *.md",
        "officeFilesCheckboxText": "*.xls *.xlsx *.ppt *.pptx *.csv",
        "imageFilesCheckboxText": "*.jpg *.jpeg *.png *.bmp *.gif *.tiff",
        "musicFilesCheckboxText": "*.mp3 *.wav *.flac *.aac *.ogg",
        "archiveFilesCheckboxText": "*.zip *.rar *.7z *.tar *.gz",
    }
    for widget in widgets:
        name = widget.objectName() + "Text"
        if isinstance(widget, QCheckBox):
            if widget.isChecked() and name in filters_config:
                filter_text = texts_data.get(name, "N/A")
                filters = filters_config.get(name)
                final_filters += f"{filter_text} ({filters});;"
                for exist_filter in filters.split(" "):
                    if exist_filter.strip():
                        existing_filters.add(exist_filter)
        if isinstance(widget, QLineEdit):
            if widget.objectName() == "customExtensionsEdit" and widget.text():
                extension_filter = ""
                for extension in widget.text().split(","):
                    if extension.strip():
                        filter_name = f"*.{extension.strip()}"
                        if filter_name not in existing_filters:
                            existing_filters.add(filter_name)
                            extension_filter += filter_name + " "
                if extension_filter:
                    filter_text = texts_data.get(name, "N/A")
                    final_filters += f"{filter_text} ({extension_filter});;"
    if final_filters.strip().endswith(";;"):
        final_filters = final_filters[:-2]
    return final_filters.strip()