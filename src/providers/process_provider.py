from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, QThread
from PyQt6.QtWidgets import QMessageBox

from src.UI.dialogs.progress_dialog import ProgressDialog
from src.providers.language_provider import LanguageProvider
from src.threads_objects.process_object import ProcessObject
from src.utilities.error_handler import Errorhandler

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class ProcessProvider(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_files = []

    def start_process(self, main_window: "MainWindow") -> None:
        try:
            ui_texts = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__,
                                                       LanguageProvider.language_code)
            if not self.selected_files:
                if not ui_texts:
                    raise IOError("Texts data loading failed.")
                message = QMessageBox(main_window)
                message.setWindowTitle(ui_texts.get("titleText", "Error"))
                message.setIcon(QMessageBox.Icon.Warning)
                message.setText(ui_texts.get("messageText", "No file selected for transfer."))
                message.exec()
                return
            if not hasattr(main_window, "processing_widget") or not hasattr(main_window, "workflow_settings"):
                raise IOError("Processing widget or Workflow settings loading failed.")
            output_path = main_window.processing_widget.full_output_path
            active_filter = main_window.workflow_settings.active_filter()
            self.thread = QThread()
            self.object = ProcessObject(ui_texts, output_path, self.selected_files, active_filter)
            self.dialog = ProgressDialog(main_window)
            self.dialog.cancel_progress_button.clicked.connect(self.object.cancel_thread)
            self.object.moveToThread(self.thread)
            self.thread.started.connect(self.object.run_process)
            self.object.files_count.connect(self.dialog.set_progress_bar_range)
            self.object.progress.connect(self.dialog.update_progress_value_label)
            self.object.finished.connect(self.stop_thread)
            self.object.failed.connect(self.show_dialog)
            self.thread.start()
            self.dialog.exec()
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def stop_thread(self) -> None:
        self.thread.quit()
        self.object.deleteLater()
        self.thread.deleteLater()
        self.selected_files.clear()
        self.dialog.close()

    def show_dialog(self, exception: Exception) -> None:
        self.dialog.close()
        Errorhandler.handle_error(self.__class__.__name__, exception)