import datetime
import pathlib
import pytest

from pathlib import Path

from src.threads_objects.process_object import ProcessObject

@pytest.fixture
def base_folder(tmp_path) -> Path:
    folder = tmp_path.joinpath("folder")
    folder.mkdir()
    return folder

@pytest.fixture
def folder_with_files(base_folder) -> Path:
    file_1 = base_folder.joinpath("file_1.txt")
    file_1.write_text("file_1")
    file_2 = base_folder.joinpath("file_2.txt")
    file_2.write_text("file_2")
    hidden_file = base_folder.joinpath(".hidden_file.txt")
    hidden_file.write_text("hidden_file")
    return base_folder

@pytest.fixture
def documents_texts() -> dict[str, str | list[str]]:
    return {
        "documentsFiles": "Documents",
        "documentsSuffixes": ["pdf", "doc", "docx", "odt", "rtf", "tex"],
        "txtFiles": "Text_files",
        "txtSuffixes": ["txt", "log", "md", "cfg", "ini", "csv"],
        "officeFiles": "Office",
        "officeSuffixes": ["xls", "xlsx", "ppt", "pptx", "doc", "docx"],
        "imageFiles": "Images",
        "imageSuffixes": ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "svg", "webp", "heic"],
        "musicFiles": "Music",
        "musicSuffixes": ["mp3", "wav", "flac", "aac", "ogg", "m4a", "wma"],
        "archiveFiles": "Archive",
        "archiveSuffixes": ["zip", "rar", "7z", "tar", "gz", "bz2", "xz", "lzma"],
        "othersFiles": "Others"
    }

@pytest.fixture
def active_filters() -> dict[str, bool | str]:
    return {
        "year": True,
        "month": False,
        "day": False,
        "type_subfolder": False,
        "hidden_folders": False,
        "default_name": False,
        "custom_name": "custom name",
        "timestamp": False,
        "counter": False,
        "main_filter": True,
        "documents_filter":True,
        "txt_filter": True,
        "office_filter": True,
        "image_filter": True,
        "music_filter": True,
        "archive_filter": True,
        "custom_extensions": "pdf",
        "delete_file": True,
        "failed_files": True,
    }

@pytest.mark.parametrize("hidden_bool, files_count", [
    (True, 3),
    (False, 2),
], ids=["hidden_files", "without hidden_files"])

def test_check_dir_folders(folder_with_files, active_filters, documents_texts, hidden_bool, files_count) -> None:
    test_filters = active_filters.copy()
    test_filters["hidden_folders"] = hidden_bool
    expected_path = folder_with_files
    result = ProcessObject.check_dir_folders([str(expected_path)], test_filters, documents_texts)
    assert len(result) == files_count

@pytest.mark.parametrize("src, dest, delete_file, return_value", [
    ("test_folder1.txt", "test_folder2.txt", True, None),
    ("test_folder1.txt", "test_folder2.txt", False, None),
    ("test_folder1.txt", "test_folder1.txt", True, ValueError),
    ("test_folder1.txt", "test_folder2.txt", True, PermissionError),
], ids=["copy+delete", "copy_only", "same_path_error", "permission_error"])

def test_copy_file(base_folder, monkeypatch, src, dest, delete_file, return_value) -> None:
    path = base_folder.joinpath(src)
    path.touch()
    output_path = base_folder.joinpath(dest)

    def fake_copy(src_path, dest_path) -> None:
        pass

    def fake_copy_error(src_path, dest_path) -> None:
        raise PermissionError("Simulated permission error")

    def fake_unlink(path_to_remove) -> None:
        pass

    if return_value == PermissionError:
        monkeypatch.setattr("shutil.copy2", fake_copy_error)
    else:
        monkeypatch.setattr("shutil.copy2", fake_copy)
    monkeypatch.setattr(pathlib.Path, "unlink", fake_unlink)
    result = ProcessObject.copy_file(path, output_path, delete_file)
    if return_value is ValueError:
        assert isinstance(result, ValueError)
    elif return_value is PermissionError:
        assert isinstance(result, PermissionError)
    else:
        assert result is None

@pytest.mark.parametrize("month_checked, day_checked, timestamp, month, day", [
    (True, True, datetime.datetime(2021, 1, 1), "1", "1"),
    (True, False, datetime.datetime(2022, 2, 2), "2", None),
    (False, False, datetime.datetime(2023, 3, 3), None, None),
    (False, True, datetime.datetime(2024, 4, 4), None, "4"),
    (True, True, datetime.datetime(2025, 12, 24), "12", "24"),
], ids=["full_date", "month_date", "no_date", "wrong_setup", "double_date"])

def test_get_datetime_tree(base_folder, month_checked, day_checked, timestamp, month, day) -> None:
    expected_path = base_folder
    result = ProcessObject.get_datetime_tree(month_checked, day_checked, timestamp, base_folder)
    if month_checked:
        expected_path = expected_path.joinpath(month)
        if day_checked:
            expected_path = expected_path.joinpath(day)
    assert result == expected_path

@pytest.mark.parametrize("suffix, folder_name", [
        ("pdf", "Documents"),
        ("txt", "Text_files"),
        ("xls", "Office"),
        ("jpg", "Images"),
        ("mp3", "Music"),
        ("zip", "Archive"),
        ("xyz", "Others")
    ],
    ids=["documents_file", "txt_file", "office_file", "images_file", "music_file", "archive_file", "others_file"
    ]
)

def test_get_file_type(base_folder, documents_texts, suffix, folder_name) -> None:
    result = ProcessObject.get_file_type(documents_texts, suffix, base_folder)
    assert result == base_folder.joinpath(folder_name)

@pytest.mark.parametrize("file_name, custom_name, timestamp_checked, timestamp, counter_checked, counter, counter_result", [
    ("default", "new", True, None, True, 0, 1),
    ("default", "new", True, None, False, 1, 1),
    ("default", "new", False, None, True, 2, 3),
    ("default", "new", False, None, False, 3, 3),
], ids=["full_name", "timestamp_name", "counter_name", "default_name"])

def test_get_file_name(file_name, custom_name, timestamp_checked, timestamp, counter_checked, counter, counter_result) -> None:
    if timestamp_checked:
        timestamp = datetime.datetime.now()
    result_name, result_timestamp, result_counter = ProcessObject.get_file_name(
                                                    file_name, custom_name, timestamp_checked, counter_checked, counter)
    assert result_name == custom_name
    if timestamp_checked:
        assert abs((result_timestamp - timestamp).total_seconds()) < 0.1
    else:
        assert result_timestamp == timestamp
    assert result_counter == counter_result

@pytest.mark.parametrize("file_path, main_filter, documents_filter, txt_filter, office_filter, image_filter, music_filter,"
                         "archive_filter, extension, expected_bool", [
    (pathlib.Path("/fake/path/file1.pdf"), True, True, True, True, True, True, True, "", True),
    (pathlib.Path("/fake/path/file2.pdf"), True, False, True, True, True, True, True, "", False),
    (pathlib.Path("/fake/path/file1.txt"), True, True, True, True, True, True, True, "", True),
    (pathlib.Path("/fake/path/file2.txt"), True, True, False, True, True, True, True, "", False),
    (pathlib.Path("/fake/path/image1.jpg"), True, True, True, True, True, True, True, "", True),
    (pathlib.Path("/fake/path/image2.png"), True, True, True, True, False, True, True, "", False),
    (pathlib.Path("/fake/path/song1.mp3"), True, True, True, True, True, True, True, "", True),
    (pathlib.Path("/fake/path/song2.wav"), True, True, True, True, True, False, True, "", False),
    (pathlib.Path("/fake/path/archive1.zip"), True, True, True, True, True, True, True, "", True),
    (pathlib.Path("/fake/path/archive2.rar"), True, True, True, True, True, True, False, "", False),
    (pathlib.Path("/fake/path/file1.xyz"), True, True, True, True, True, True, True, "", False),
    (pathlib.Path("/fake/path/file2.xyz"), False, False, False, False, False, False, False, "", False),
    (pathlib.Path("/fake/path/extension1.xyz"), False, False, False, False, False, False, False, "xyz;zyx", True),
    (pathlib.Path("/fake/path/extension2.xyz"), True, False, False, False, False, False, False, "pdf;txt", False),
    (pathlib.Path("/fake/path/extension3.xyz"), False, False, False, False, False, False, False, " ", False),
    (pathlib.Path("/fake/path/extension4.xyz"), False, False, False, False, False, False, False, "abc;bca", False)
], ids=["document-True", "document-False", "txt-True", "txt-False", "image-True", "image-False", "music-True", "music-False",
        "archive-True", "archive-False", "others-False", "others-False", "extension-True", "extension-False",
        "empty extension-False", "wrong extension-False"])
def test_is_file_type_included(file_path, main_filter, documents_filter, txt_filter,
                               office_filter, image_filter, music_filter, archive_filter, extension, expected_bool,
                               active_filters, documents_texts) -> None:
    test_filters = active_filters.copy()
    test_filters.update({
        "main_filter": main_filter,
        "documents_filter": documents_filter,
        "txt_filter": txt_filter,
        "office_filter": office_filter,
        "image_filter": image_filter,
        "music_filter": music_filter,
        "archive_filter": archive_filter,
        "custom_extensions": extension,
    })

    result = ProcessObject.is_file_type_included(file_path, test_filters, documents_texts)
    assert result == expected_bool