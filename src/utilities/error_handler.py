from PyQt6.QtWidgets import QApplication, QMainWindow

from src.UI.dialogs.error_dialog import ErrorDialog
from src.utilities.logging_provider import get_logger


# noinspection PyBroadException
class Errorhandler:
    logger = get_logger()
    _show_dialog = True

    @staticmethod
    def handle_error(class_name: str, exception: Exception) -> None:
        if Errorhandler.logger is None:
            return
        try:
            Errorhandler.logger.error(f"{class_name}: {exception}", exc_info=True)
            if Errorhandler._show_dialog:
                main_window = QApplication.activeWindow()
                parent = None
                if isinstance(main_window, QMainWindow):
                    parent = main_window
                from src.providers.language_provider import LanguageProvider
                dialog = ErrorDialog(exception, parent)
                try:
                    dialog.set_ui_texts()
                    dialog.set_error_texts()
                except Exception as e:
                    if Errorhandler.logger:
                        Errorhandler.logger.error(f"ErrorDialog load_ui_texts: {e}", exc_info=True)
                dialog.exec()
            Errorhandler._show_dialog = False
        except Exception:
            Errorhandler.logger.error(f"{class_name}: {exception}", exc_info=True)
            pass