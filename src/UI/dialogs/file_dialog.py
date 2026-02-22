from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QFileDialog, QApplication, QWidget


class FileDialog(QFileDialog):
    def __init__(self, mode: QFileDialog.FileMode, filters: str | None, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFileMode(mode)
        if filters:
            self.setNameFilter(filters)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if self.parentWidget() is None:
            screen = QApplication.primaryScreen().availableGeometry()
            geometry = self.frameGeometry()
            geometry.moveCenter(screen.center())
            self.move(geometry.topLeft())