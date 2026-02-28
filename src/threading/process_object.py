import pathlib
import datetime

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


# noinspection PyBroadException
class ProcessObject(QObject):
    finished = pyqtSignal()
    failed = pyqtSignal(Exception)
    progress = pyqtSignal(int)

    def __init__(self, documents_texts: dict[str, str], output_path: pathlib.Path, selected_paths: list[str],
                 active_filter: dict[str, bool | str]) -> None:
        super().__init__()
        self.documents_texts = documents_texts
        self.output_path = output_path
        self.selected_paths = selected_paths
        self.active_filter = active_filter

    @pyqtSlot()
    def run_process(self) -> None:
        try:
            validated_list = self.check_dir_folders(self.selected_paths)
            if not validated_list:
                raise ValueError("Validate folders failed")
            for path in validated_list:
                self.move_file_to_path(self.output_path, path, self.active_filter, self.documents_texts)
            self.finished.emit()
        except Exception as e:
            self.failed.emit(e)

    @classmethod
    def check_dir_folders(cls, paths_list: list[str]) -> list[pathlib.Path]:
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

    @classmethod
    def move_file_to_path(cls, output_path: pathlib.Path, path: pathlib.Path, active_filters: dict[str, bool | str],
                          documents_texts: dict[str, str]) -> bool:
        output_path = output_path
        metadata = ProcessObject.get_file_metadata(path)
        if not metadata:
            return False
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path = ProcessObject.get_datetime_tree(active_filters.get("year", True),
                                            active_filters.get("month", False),
                                            active_filters.get("day", False),
                                            metadata["created"], output_path)
        output_path = ProcessObject.get_file_type(active_filters.get("type", False), documents_texts,
                                        metadata["type"], output_path)
        print(output_path)
        return True

    @staticmethod
    def get_file_metadata(file_path: pathlib.Path) -> dict[str, str | datetime.datetime]:
        return {
                "created": datetime.datetime.fromtimestamp(file_path.stat().st_mtime),
                "type": file_path.suffix.lstrip(".").lower(),
                "hidden": file_path.name.startswith(".")
        }

    @staticmethod
    def get_datetime_tree(year_checked: bool, month_checked: bool, day_checked: bool, timestamp: datetime.datetime,
                          output_path: pathlib.Path) -> pathlib.Path:
        if year_checked:
            output_path = output_path.joinpath(f"{timestamp.year}")
            if month_checked:
                output_path = output_path.joinpath(f"{timestamp.month}")
                if day_checked:
                    output_path = output_path.joinpath(f"{timestamp.day}")
        return output_path

    @staticmethod
    def get_file_type(type_checked: bool, documents_texts: dict[str, str], file_suffix: str,
                      output_path: pathlib.Path) -> pathlib.Path:
        if type_checked:
            type_filter = {
                documents_texts["documentsFiles"]: documents_texts["documentsSuffixes"],
                documents_texts["txtFiles"]: documents_texts["txtSuffixes"],
                documents_texts["officeFiles"]: documents_texts["officeSuffixes"],
                documents_texts["imageFiles"]: documents_texts["imageSuffixes"],
                documents_texts["musicFiles"]: documents_texts["musicSuffixes"],
                documents_texts["archiveFiles"]: documents_texts["archiveSuffixes"],
            }
            folder_name = documents_texts["otherFiles"]
            for key, value in type_filter.items():
                if file_suffix in value:
                    folder_name = key
                    break
            output_path = output_path.joinpath(folder_name)
        return output_path