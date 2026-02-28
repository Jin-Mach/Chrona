from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QStackedWidget, QFileDialog, QCheckBox, \
    QLineEdit

from src.UI.dialogs.file_dialog import FileDialog
from src.UI.widgets.processing_widget import ProcessingWidget
from src.UI.widgets.workflow_settings import WorkflowSettings
from src.UI.widgets.side_panel import SidePanel
from src.providers.language_provider import LanguageProvider
from src.providers.process_provider import ProcessProvider
from src.utilities.error_handler import Errorhandler
from src.utilities.setup_handler import handle_ui_texts
from src.utilities.ui_helpers import get_current_filter


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(1200, 700)
        self.centered = False
        self.setCentralWidget(self.create_gui())
        self.process_provider = ProcessProvider(self)
        self.setup_stack()
        self.set_ui_texts()
        self.create_connection()

    def create_gui(self) -> QWidget:
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setObjectName("stacked_widget")
        self.processing_widget = ProcessingWidget(self)
        self.workflow_settings = WorkflowSettings(self)
        self.side_panel = SidePanel(self.stacked_widget, self)
        main_layout.addWidget(self.side_panel)
        main_layout.addWidget(self.stacked_widget)
        central_widget.setLayout(main_layout)
        return central_widget

    def setup_stack(self) -> None:
        widgets = [self.processing_widget, self.workflow_settings]
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

    def create_connection(self) -> None:
        self.processing_widget.input_path_select.clicked.connect(lambda: self.show_dialog(
            QFileDialog.FileMode.Directory, self, "input_folder_processing_widget"
        ))
        self.processing_widget.input_path_add.clicked.connect(lambda: self.show_dialog(
            QFileDialog.FileMode.ExistingFiles, self, "add_files_processing_widget", filters=True
        ))
        self.processing_widget.output_path_select.clicked.connect(lambda: self.show_dialog(
            QFileDialog.FileMode.Directory, self, "output_folder_processing_widget"
        ))
        self.workflow_settings.input_path_browse.clicked.connect(lambda: self.show_dialog(
            QFileDialog.FileMode.Directory, self, "input_folder_workflow_settings"
        ))
        self.workflow_settings.output_path_browse.clicked.connect(lambda: self.show_dialog(
            QFileDialog.FileMode.Directory, self, "output_folder_workflow_settings"
        ))
        self.processing_widget.start_button.clicked.connect(lambda: self.process_provider.start_process(
            self
        ))

    def show_dialog(self, mode: QFileDialog.FileMode, parent: QWidget, action: str, filters: bool = False) -> None:
        try:
            texts_data = LanguageProvider.get_texts_data("ui_texts", FileDialog.__name__,
                                                         LanguageProvider.language_code)
            if not texts_data:
                raise IOError("Texts data loading failed.")
            current_filter = None
            if filters:
                current_filter = get_current_filter(self.workflow_settings.findChildren((QCheckBox, QLineEdit)), texts_data)
            dialog = FileDialog(mode, current_filter, parent)
            if dialog.exec():
                selected = dialog.selectedFiles()
                if selected:
                    if mode == QFileDialog.FileMode.Directory:
                        self.handle_dialog_result(selected[0], action)
                    else:
                        self.handle_dialog_result(selected, action)
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def handle_dialog_result(self, path: list[str] | str, action: str) -> None:
        if action in ["input_folder_processing_widget", "add_files_processing_widget"]:
            if isinstance(path, list):
                self.process_provider.selected_files = list(set(self.process_provider.selected_files + path))
            elif isinstance(path, str) and path not in self.process_provider.selected_files:
                self.process_provider.selected_files.append(path)
        elif action == "output_folder_processing_widget":
            self.processing_widget.update_output_path(path)
        elif action == "input_folder_workflow_settings":
            self.workflow_settings.update_input_path(path)
            self.processing_widget.update_input_path(path)
        elif action == "output_folder_workflow_settings":
            self.workflow_settings.update_output_path(path)
            self.processing_widget.update_output_path(path)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if self.centered:
            return
        screen = QApplication.primaryScreen().availableGeometry()
        geometry = self.frameGeometry()
        geometry.moveCenter(screen.center())
        self.move(geometry.topLeft())
        self.centered = True