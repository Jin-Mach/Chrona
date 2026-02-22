from PyQt6.QtCore import QObject, QThread
from PyQt6.QtWidgets import QMessageBox

from src.providers.language_provider import LanguageProvider
from src.threading.process_object import ProcessObject
from src.utilities.error_handler import Errorhandler


class ProcessProvider(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.selected_files = []

    def start_process(self) -> None:
        try:
            if not self.selected_files:
                ui_texts = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__, LanguageProvider.language_code)
                if not ui_texts:
                    raise IOError("Texts data loading failed.")
                message = QMessageBox(self.parent)
                message.setWindowTitle(ui_texts.get("titleText", "Error"))
                message.setIcon(QMessageBox.Icon.Warning)
                message.setText(ui_texts.get("messageText", "No file selected for transfer."))
                message.exec()
                return
            self.thread = QThread()
            self.object = ProcessObject(self.selected_files)
            self.object.moveToThread(self.thread)
            self.thread.started.connect(self.object.run_process)
            self.object.finished.connect(self.thread.quit)
            self.object.finished.connect(self.object.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.object.finished.connect(lambda: self.selected_files.clear())
            self.object.failed.connect(self.show_dialog)
            self.thread.start()
        except Exception as e:
            Errorhandler.handle_error(self.__class__.__name__, e)

    def show_dialog(self, exception: Exception) -> None:
        Errorhandler.handle_error(self.__class__.__name__, exception)