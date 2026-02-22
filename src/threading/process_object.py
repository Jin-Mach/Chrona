import pathlib

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class ProcessObject(QObject):
    finished = pyqtSignal()
    failed = pyqtSignal(Exception)
    progress = pyqtSignal(int)

    def __init__(self, selected_paths: list[str]) -> None:
        super().__init__()
        self.selected_paths = selected_paths

    @pyqtSlot()
    def run_process(self) -> None:
        try:
            validated_list = self.check_dir_folders(self.selected_paths)
            if not validated_list:
                raise ValueError("Validate folders failed")
            print(validated_list)
            self.finished.emit()
        except Exception as e:
            self.failed.emit(e)

    def check_dir_folders(self, paths_list: list[str]) -> list[pathlib.Path]:
        validated_list = []
        for path in paths_list:
            path = pathlib.Path(path)
            if path.is_dir():
                for child in path.rglob("*"):
                    if child.is_file():
                        validated_list.append(child)
            elif path.is_file():
                validated_list.append(path)
        return validated_list