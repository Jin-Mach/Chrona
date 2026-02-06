from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QStackedWidget

from src.UI.widgets.workflow_settings import WorkflowSettings
from src.UI.widgets.side_panel import SidePanel

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(1000, 600)
        self.centered = False
        self.settings_widget = WorkflowSettings(self)
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setObjectName("stacked_widget")
        self.side_panel = SidePanel(self.stacked_widget, self)
        self.setup_stack()
        self.setCentralWidget(self.create_gui())

    def create_gui(self) -> QWidget:
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.side_panel)
        main_layout.addWidget(self.stacked_widget)
        central_widget.setLayout(main_layout)
        return central_widget

    def setup_stack(self) -> None:
        widgets = [self.settings_widget]
        for widget in widgets:
            self.stacked_widget.addWidget(widget)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if self.centered:
            return
        screen = QApplication.primaryScreen().availableGeometry()
        geometry = self.frameGeometry()
        geometry.moveCenter(screen.center())
        self.move(geometry.topLeft())
        self.centered = True