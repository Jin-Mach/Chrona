from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QDialog, QLayout, QVBoxLayout, QApplication, QLabel, QTextEdit, QDialogButtonBox, \
    QPushButton

from src.utilities.setup_handler import handle_ui_texts


# noinspection PyUnresolvedReferences,PyTypeChecker,PyBroadException
class ErrorDialog(QDialog):
    def __init__(self, exception: Exception, parent=None) -> None:
        super().__init__(parent)
        self.exception = exception
        self._detail_visible = False
        self.setLayout(self.create_gui())

    def create_gui(self) -> QLayout:
        main_layout = QVBoxLayout()
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
        self.error_label.setWordWrap(True)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detail_edit = QTextEdit()
        self.detail_edit.setObjectName("detailEdit")
        self.detail_edit.setReadOnly(True)
        self.detail_edit.setVisible(self._detail_visible)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.RestoreDefaults | QDialogButtonBox.StandardButton.Close)
        show_hide_button = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        show_hide_button.setObjectName("showHideButton")
        show_hide_button.clicked.connect(self.show_hide_detail)
        close_button = button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.reject)
        main_layout.addWidget(self.error_label)
        main_layout.addWidget(self.detail_edit)
        main_layout.addWidget(button_box)
        return main_layout

    def set_ui_texts(self) -> None:
        try:
            from src.providers.language_provider import LanguageProvider
            texts_data = LanguageProvider.get_texts_data("ui_texts", self.__class__.__name__,
                                                         LanguageProvider.language_code)
            if not texts_data:
                raise IOError("No ui_texts data loaded.")
            handle_ui_texts(self, texts_data, self.findChildren(QPushButton))
        except Exception:
            pass

    def set_error_texts(self) -> None:
        try:
            from src.providers.language_provider import LanguageProvider
            errors_data = LanguageProvider.get_error_text(LanguageProvider.language_code)
            key = type(self.exception).__name__
            if not key in errors_data.keys():
                key = "UnknownError"
            if not errors_data:
                raise IOError("No error_texts data loaded.")
            self.error_label.setText(errors_data.get(key, "Unknown error"))
            self.detail_edit.setPlainText(str(self.exception))
        except Exception:
            pass

    def show_hide_detail(self) -> None:
        self._detail_visible = not self._detail_visible
        self.detail_edit.setVisible(self._detail_visible)
        center = self.frameGeometry().center()
        self.adjustSize()
        geometry = self.frameGeometry()
        geometry.moveCenter(center)
        self.move(geometry.topLeft())

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if self.parentWidget() is None:
            screen = QApplication.primaryScreen().availableGeometry()
            geometry = self.frameGeometry()
            geometry.moveCenter(screen.center())
            self.move(geometry.topLeft())