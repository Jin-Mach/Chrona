from functools import partial
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class SidePanel(QWidget):
    def __init__(self, stacked_widget: QStackedWidget, main_window: "MainWindow"):
        super().__init__(main_window)
        self.stacked_widget = stacked_widget
        self.main_window = main_window
        self.setLayout(self.create_gui())
        self.create_connection()

    @staticmethod
    def create_gui() -> QVBoxLayout:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        files_list_button = QPushButton("Files list")
        files_list_button.setObjectName("filesListButton")
        workflow_settings_button = QPushButton("Workflow")
        workflow_settings_button.setObjectName("workflowSettingsButton")
        main_layout.addWidget(files_list_button)
        main_layout.addWidget(workflow_settings_button)
        main_layout.addStretch()
        return main_layout

    def create_connection(self) -> None:
        buttons = self.findChildren(QPushButton)
        for index, button in enumerate(buttons):
            if isinstance(button, QPushButton):
                button.clicked.connect(partial(self.stacked_widget.setCurrentIndex, index))