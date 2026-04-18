from PyQt6.QtWidgets import QMessageBox


def show_error_dialog(title: str, message: str, parent=None) -> None:
    error_dialog = QMessageBox(parent)
    error_dialog.setWindowTitle(title)
    error_dialog.setIcon(QMessageBox.Icon.Warning)
    error_dialog.setText(message)
    error_dialog.exec()

def show_question_dialog(title: str, message: str, parent=None) -> bool:
    result = QMessageBox.question(parent, title, message,
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                  QMessageBox.StandardButton.No)
    return result == QMessageBox.StandardButton.Yes