import pathlib
import datetime
import shutil
import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

from src.utilities.logging_provider import get_logger


# noinspection PyBroadException
class ProcessObject(QObject):
    finished = pyqtSignal(list)
    failed = pyqtSignal(Exception)
    progress = pyqtSignal(int)

    def __init__(self, documents_texts: dict[str, str], output_path: pathlib.Path, selected_paths: list[str],
                 active_filter: dict[str, bool | str]) -> None:
        super().__init__()
        self.documents_texts = documents_texts
        self.output_path = output_path
        self.selected_paths = selected_paths
        self.active_filter = active_filter
        self.logger = get_logger()

    @pyqtSlot()
    def run_process(self) -> None:
        failed_list = []
        try:
            validated_list = self.check_dir_folders(self.selected_paths, self.active_filter, self.documents_texts)
            if not validated_list:
                raise ValueError("Validate folders failed")
            for index, path in enumerate(validated_list):
                output_path = self.get_output_path(index, path, self.output_path, self.active_filter, self.documents_texts)
                if not output_path:
                    failed_list.append((path, FileNotFoundError("Output path not created")))
                    self.logger.error(f"{self.__class__.__name__}: Output {path} not created", exc_info=True)
                    continue
                error = self.copy_file(path, output_path, self.active_filter.get("delete_file", False))
                if not error is None:
                    failed_list.append((path, error))
                    self.logger.error(f"{self.__class__.__name__}: {error}", exc_info=True)
                    continue
                self.progress.emit(index + 1)
            self.finished.emit(failed_list)
        except Exception as e:
            self.logger.error(f"{self.__class__.__name__}: {e}", exc_info=True)
            self.failed.emit(e)

    @classmethod
    def check_dir_folders(cls, paths_list: list[str], active_filters: dict[str, bool | str], documents_texts: dict[str, str]) -> list[pathlib.Path]:
        include_hidden = active_filters.get("hidden_folders", False)
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
                        if not skip_child and ProcessObject.is_file_type_included(child, active_filters, documents_texts):
                            validated_set.add(child)
            elif path.is_file() and ProcessObject.is_file_type_included(path, active_filters, documents_texts):
                validated_set.add(path)
        return list(validated_set)

    @classmethod
    def get_output_path(cls, index: int, path: pathlib.Path, output_path: pathlib.Path,
                        active_filters: dict[str, bool | str], documents_texts: dict[str, str | list[str]]) -> pathlib.Path | None:
        file_name = path.stem
        file_timestamp = None
        file_counter = -1
        file_suffix = path.suffix
        name_parts = []
        metadata = ProcessObject.get_file_metadata(path)
        if not metadata:
            return None
        file_created = metadata["created"]
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
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path

    @classmethod
    def copy_file(cls, path: pathlib.Path, output_path: pathlib.Path, delete_file: bool) -> Exception | None:
        try:
            if path.resolve() == output_path.resolve():
                return ValueError("Source and destination are the same")
            shutil.copy2(path, output_path)
            if delete_file:
                path.unlink()
            return None
        except (PermissionError, FileNotFoundError, IOError, OSError) as e:
            return e

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
    def is_file_type_included(file: pathlib.Path, active_filters: dict[str, bool | str], documents_texts: dict[str, str]) -> bool:
        suffix = file.suffix.lstrip(".")
        if active_filters.get("main_filter", False):
            for key, value in documents_texts.items():
                if key.endswith("Suffixes"):
                    if suffix in value:
                        filter_key = key.replace("Suffixes", "_filter")
                        return active_filters.get(filter_key, False)
        extensions = active_filters.get("custom_extensions", "")
        if extensions:
            for extension in extensions.split(";"):
                if suffix == extension.strip():
                    return True
        return False

    @staticmethod
    def get_creation_time(file_path: pathlib.Path) -> datetime.datetime:
        if sys.platform == "win32":
            timestamp = file_path.stat().st_ctime
        else:
            stat = file_path.stat()
            timestamp = getattr(stat, "st_birthtime", stat.st_mtime)
        return datetime.datetime.fromtimestamp(timestamp)