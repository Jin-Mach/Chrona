from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("mainWindow")
        self.centered = False

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if self.centered:
            return
        screen = QApplication.primaryScreen().availableGeometry()
        geometry = self.frameGeometry()
        geometry.moveCenter(screen.center())
        self.move(geometry.topLeft())
        self.centered = True