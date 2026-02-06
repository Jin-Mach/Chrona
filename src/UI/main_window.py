from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout

from src.UI.widgets.settings_widget import SettingsWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.centered = False
        self.settings_widget = SettingsWidget(self)
        self.setCentralWidget(self.create_gui())

    def create_gui(self) -> QWidget:
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.settings_widget)
        central_widget.setLayout(main_layout)
        return central_widget

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if self.centered:
            return
        screen = QApplication.primaryScreen().availableGeometry()
        geometry = self.frameGeometry()
        geometry.moveCenter(screen.center())
        self.move(geometry.topLeft())
        self.centered = True