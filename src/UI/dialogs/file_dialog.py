from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QFileDialog, QApplication, QWidget


class FileDialog(QFileDialog):
    def __init__(self, ui_texts: dict[str, str], mode: QFileDialog.FileMode, filters: str | None, parent: QWidget) -> None:
        super().__init__(parent)
        title_text = ui_texts.get("titleTextFolder", "Select folder")
        if mode == QFileDialog.FileMode.ExistingFiles:
            title_text = ui_texts.get("titleTextFile", "Select file(s)")
        self.setWindowTitle(title_text)
        self.setFileMode(mode)
        if filters:
            self.setNameFilter(filters)
        self.setLabelText(self.DialogLabel.Accept, ui_texts.get("labelTextAccept", "Select"))
        self.setLabelText(self.DialogLabel.Reject, ui_texts.get("labelTextReject", "Cancel"))

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if self.parentWidget() is None:
            screen = QApplication.primaryScreen().availableGeometry()
            geometry = self.frameGeometry()
            geometry.moveCenter(screen.center())
            self.move(geometry.topLeft())