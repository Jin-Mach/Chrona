from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QStackedWidget

from src.UI.widgets.processing_widget import ProcessingWidget
from src.UI.widgets.workflow_settings import WorkflowSettings
from src.UI.widgets.side_panel import SidePanel
from src.providers.language_provider import LanguageProvider
from src.utilities.error_handler import Errorhandler
from src.utilities.setup_handler import handle_ui_texts


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(1000, 600)
        self.centered = False
        self.setCentralWidget(self.create_gui())
        self.setup_stack()
        self.set_ui_texts()

    def create_gui(self) -> QWidget:
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setObjectName("stacked_widget")
        self.files_list_widget = ProcessingWidget(self)
        self.workflow_settings = WorkflowSettings(self)
        self.side_panel = SidePanel(self.stacked_widget, self)
        main_layout.addWidget(self.side_panel)
        main_layout.addWidget(self.stacked_widget)
        central_widget.setLayout(main_layout)
        return central_widget

    def setup_stack(self) -> None:
        widgets = [self.files_list_widget, self.workflow_settings]
        for widget in widgets:
            self.stacked_widget.addWidget(widget)

    def set_ui_texts(self) -> None:
        try:
            texts_data = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__,
                                                         LanguageProvider.language_code)
            if not texts_data:
                raise IOError("Texts data loading failed.")
            handle_ui_texts(self, texts_data)
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if self.centered:
            return
        screen = QApplication.primaryScreen().availableGeometry()
        geometry = self.frameGeometry()
        geometry.moveCenter(screen.center())
        self.move(geometry.topLeft())
        self.centered = True