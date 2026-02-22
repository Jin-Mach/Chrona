from PyQt6.QtWidgets import QMessageBox

from src.providers.language_provider import LanguageProvider
from src.utilities.error_handler import Errorhandler


class ProcessProvider:
    selected_files = []

    @classmethod
    def start_process(cls) -> None:
        try:
            if not cls.selected_files:
                ui_texts = LanguageProvider.get_texts_data("ui_texts", cls.__name__, LanguageProvider.language_code)
                if not ui_texts:
                    raise IOError("Texts data loading failed.")
                message = QMessageBox()
                message.setWindowTitle(ui_texts.get("titleText", "Error"))
                message.setIcon(QMessageBox.Icon.Warning)
                message.setText(ui_texts.get("messageText", "No file selected for transfer."))
                message.exec()
                return
            print(cls.selected_files)
        except Exception as e:
            Errorhandler.handle_error(cls.__name__, e)