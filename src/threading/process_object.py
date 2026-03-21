import pathlib
import datetime
import sys

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
        print("active_filter:", self.active_filter)

    @pyqtSlot()
    def run_process(self) -> None:
        try:
            validated_list = self.check_dir_folders(self.selected_paths, self.active_filter.get("hidden_folders", False))
            if not validated_list:
                raise ValueError("Validate folders failed")
            for index, path in enumerate(validated_list):
                self.move_file_to_path(index, self.output_path, path, self.active_filter, self.documents_texts)
            self.finished.emit()
        except Exception as e:
            self.failed.emit(e)

    @classmethod
    def check_dir_folders(cls, paths_list: list[str], include_hidden: bool) -> list[pathlib.Path]:
        validated_set = set()
        for path_str in paths_list:
            path = pathlib.Path(path_str)
            skip_path = False
            if not include_hidden:
                for part in path.parts:
                    if part.startswith("."):
                        skip_path = True
                        break
            if skip_path:
                continue
            if path.is_dir():
                for child in path.rglob("*"):
                    if child.is_file():
                        skip_child = False
                        if not include_hidden:
                            for part in child.parts:
                                if part.startswith("."):
                                    skip_child = True
                                    break
                        if not skip_child:
                            validated_set.add(child)
            elif path.is_file():
                validated_set.add(path)
        return list(validated_set)

    @classmethod
    def move_file_to_path(cls, index: int, output_path: pathlib.Path, path: pathlib.Path,
                          active_filters: dict[str, bool | str], documents_texts: dict[str, str | list[str]]) -> bool:
        file_name = path.stem
        file_timestamp = None
        file_counter = -1
        file_suffix = path.suffix
        name_parts = []
        metadata = ProcessObject.get_file_metadata(path)
        if not metadata:
            return False
        file_created = metadata["created"]
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if active_filters.get("year", True):
            output_path = output_path.joinpath(f"{file_created.year}")
            output_path = ProcessObject.get_datetime_tree(
                active_filters.get("month", False),
                active_filters.get("day", False),
                file_created,
                output_path
            )
        if active_filters.get("type_subfolder", False):
            output_path = ProcessObject.get_file_type(documents_texts, metadata["type"], output_path)
        if not active_filters.get("default_name", True):
            new_name, file_timestamp, counter = ProcessObject.get_file_name(
                file_name,
                active_filters.get("custom_name", ""),
                active_filters.get("timestamp", False),
                active_filters.get("counter", False),
                index
            )
            file_name = new_name
            file_counter = counter
        name_parts.append(file_name)
        if file_timestamp:
            name_parts.append(file_timestamp.strftime("%Y-%m-%d_%H-%M-%S_%f"))
        if file_counter > 0:
            name_parts.append(str(file_counter))
        output_path = output_path.joinpath("_".join(name_parts)).with_suffix(file_suffix)
        return True

    @staticmethod
    def get_file_metadata(file_path: pathlib.Path) -> dict[str, str | datetime.datetime]:
        return {
                "created": ProcessObject.get_creation_time(file_path),
                "type": file_path.suffix.lstrip(".").lower(),
                "hidden": file_path.name.startswith(".")
        }

    @staticmethod
    def get_datetime_tree(month_checked: bool, day_checked: bool, timestamp: datetime.datetime,
                          output_path: pathlib.Path) -> pathlib.Path:
        if month_checked:
            output_path = output_path.joinpath(f"{timestamp.month}")
            if day_checked:
                output_path = output_path.joinpath(f"{timestamp.day}")
        return output_path

    @staticmethod
    def get_file_type(documents_texts: dict[str, str | list[str]], file_suffix: str, output_path: pathlib.Path) -> pathlib.Path:
        type_filter = {
            documents_texts["documentsFiles"]: documents_texts["documentsSuffixes"],
            documents_texts["txtFiles"]: documents_texts["txtSuffixes"],
            documents_texts["officeFiles"]: documents_texts["officeSuffixes"],
            documents_texts["imageFiles"]: documents_texts["imageSuffixes"],
            documents_texts["musicFiles"]: documents_texts["musicSuffixes"],
            documents_texts["archiveFiles"]: documents_texts["archiveSuffixes"],
        }
        folder_name = documents_texts["othersFiles"]
        for key, value in type_filter.items():
            if file_suffix in value:
                folder_name = key
                break
        output_path = output_path.joinpath(folder_name)
        return output_path

    @staticmethod
    def get_file_name(file_name: str, custom_name: str, timestamp_checked: bool, counter_checked: bool,
                      counter: int) -> tuple[str, datetime.datetime | None, int]:
        timestamp = None
        if custom_name:
            file_name = custom_name
            if timestamp_checked:
                timestamp = datetime.datetime.now()
            if counter_checked:
                counter = counter + 1
        return file_name, timestamp, counter

    @staticmethod
    def get_creation_time(file_path: pathlib.Path) -> datetime.datetime:
        if sys.platform == "win32":
            timestamp = file_path.stat().st_ctime
        else:
            stat = file_path.stat()
            timestamp = getattr(stat, "st_birthtime", stat.st_mtime)
        return datetime.datetime.fromtimestamp(timestamp)