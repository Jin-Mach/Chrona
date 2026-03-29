import pathlib

from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, QThread, QTimer

from src.UI.dialogs.failed_list_dialog import FailedListDialog
from src.UI.dialogs.progress_dialog import ProgressDialog
from src.UI.dialogs.messagebox_dialogs import show_question_dialog, show_error_dialog
from src.providers.language_provider import LanguageProvider
from src.threads_objects.process_object import ProcessObject
from src.utilities.error_handler import Errorhandler

if TYPE_CHECKING:
    from src.UI.main_window import MainWindow


class ProcessProvider(QObject):
    def __init__(self, main_window: "MainWindow"):
        super().__init__(main_window)
        self.main_window = main_window
        self.selected_files = []

    def start_process(self) -> None:
        try:
            ui_texts = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__,
                                                       LanguageProvider.language_code)
            if not ui_texts:
                raise IOError("Texts data loading failed.")
            if not self.selected_files:
                show_error_dialog(ui_texts.get("titleText", "Error"),
                                  ui_texts.get("messageText", "No file selected for transfer."),
                                  self.main_window)
                return
            self.question_title = ui_texts.get("questionTitleText", "Chrona")
            self.question_message = ui_texts.get("questionMessageText", "Do you really want to cancel the file transfer?")
            if not hasattr(self.main_window, "processing_widget") or not hasattr(self.main_window, "workflow_settings"):
                raise IOError("Processing widget or Workflow settings loading failed.")
            output_path = self.main_window.processing_widget.full_output_path
            active_filter = self.main_window.workflow_settings.active_filter()
            self.progress_thread = QThread()
            self.progress_object = ProcessObject(ui_texts, output_path, self.selected_files, active_filter)
            self.progress_dialog = ProgressDialog(self.main_window)
            self.progress_dialog.cancel_progress_button.clicked.connect(self.cancel_thread)
            self.progress_object.moveToThread(self.progress_thread)
            self.progress_thread.started.connect(self.progress_object.run_process)
            self.progress_object.files_count.connect(self.progress_dialog.set_progress_bar_range)
            self.progress_object.progress.connect(self.progress_dialog.update_progress_value_label)
            self.progress_object.finished.connect(self.stop_thread)
            self.progress_object.failed.connect(self.show_dialog)
            self.progress_dialog.show()
            QTimer.singleShot(0, self.progress_thread.start)
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def stop_thread(self, failed_list: list[tuple[pathlib.Path, Exception]]) -> None:
        self.progress_thread.quit()
        self.progress_thread.wait()
        self.progress_object.deleteLater()
        self.progress_thread.deleteLater()
        self.selected_files.clear()
        if failed_list:
            self.progress_dialog.set_failed_list_text()
            failed_dialog = FailedListDialog(self.main_window)
            failed_dialog.set_list_widget(failed_list)
            QTimer.singleShot(300, failed_dialog.open)
        QTimer.singleShot(50, self.progress_dialog.reject)

    def cancel_thread(self) -> None:
        self.progress_object.pause_thread()
        result = show_question_dialog(self.question_title, self.question_message, self.main_window)
        if result:
            self.progress_object.cancel_thread()
            QTimer.singleShot(50, self.progress_dialog.reject)
        else:
            self.progress_object.resume_thread()

    def show_dialog(self, exception: Exception) -> None:
        QTimer.singleShot(50, self.progress_dialog.reject)
        Errorhandler.handle_error(self.__class__.__name__, exception)