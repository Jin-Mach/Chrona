import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent
from PyQt6.QtWidgets import QWidget, QSizePolicy

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class DragDropWidget(QWidget):
    NO_DRAG_STYLE = """
                    border: 2px dashed #666;
                    border-radius: 6px;
                    """

    DRAG_STYLE = """
                border: 2px dashed #3b82f6;
                background-color: rgba(59, 130, 246, 0.08);
                border-radius: 6px;
                """

    FAILED_DRAG_STYLE = """
                        border: 2px dashed #ef4444;
                        background-color: rgba(239, 68, 68, 0.08);
                        border-radius: 6px;
                        """

    def __init__(self, main_window: "MainWindow") -> None:
        QWidget.__init__(self, main_window)
        self.main_window = main_window
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAcceptDrops(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(self.NO_DRAG_STYLE)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            url_exists = False
            for url in event.mimeData().urls():
                path = url.toLocalFile()
                if path and pathlib.Path(path).exists():
                    url_exists = True
                    break
            if url_exists:
                self.setStyleSheet(self.DRAG_STYLE)
                event.acceptProposedAction()
            else:
                self.setStyleSheet(self.FAILED_DRAG_STYLE)
                event.ignore()
        else:
            self.setStyleSheet(self.FAILED_DRAG_STYLE)
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasUrls():
            paths = set()
            for url in event.mimeData().urls():
                local_file = url.toLocalFile()
                path = pathlib.Path(local_file)
                if local_file and path.exists():
                    if path.is_dir():
                        self.main_window.processing_widget.update_count_labels(folders_count=1)
                    else:
                        self.main_window.processing_widget.update_count_labels(files_count=1)
                    paths.add(path)
            self.main_window.process_provider.selected_files.update(paths)
            self.setStyleSheet(self.NO_DRAG_STYLE)
            event.acceptProposedAction()

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        self.setStyleSheet(self.NO_DRAG_STYLE)
        event.accept()