from PyQt6.QtCore import Qt, QLocale
from PyQt6.QtGui import QPixmap, QShowEvent
from PyQt6.QtWidgets import QSplashScreen, QApplication


class SplashScreen(QSplashScreen):
    def __init__(self, pixmap: QPixmap) -> None:
        super().__init__(pixmap)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("font-family: Tahoma; font-size: 15pt;")

    def show_message_text(self) -> None:
        message_dic = {
            "cs_CZ": "Načítám aplikaci...",
            "en_GB": "Loading application...",
        }
        language = QLocale.system().name()
        message = message_dic.get(language, "Loading application...")
        self.showMessage(message, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, Qt.GlobalColor.white)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.show_message_text()
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            splash_size = self.size()
            x = (screen_geometry.width() - splash_size.width()) // 2
            y = (screen_geometry.height() - splash_size.height()) // 2
            self.move(x, y)