import datetime
import pytest

from pathlib import Path

from src.threading.process_object import ProcessObject

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

@pytest.mark.parametrize("include_hidden, files_count", [
    (True, 3),
    (False, 2),
], ids=["include_hidden", "without_hidden"])

def test_check_dir_folders(folder_with_files, include_hidden, files_count) -> None:
    expected_path = folder_with_files
    result = ProcessObject.check_dir_folders([str(expected_path)], include_hidden=include_hidden)
    assert len(result) == files_count

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

def test_get_file_type(base_folder, suffix, folder_name) -> None:
    documents_texts = {
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