import pytest

from src.threading.process_object import ProcessObject

@pytest.mark.parametrize("include_hidden, files_count", [
    (True, 3),
    (False, 2),
], ids=["include_hidden", "without_hidden"])

def test_check_dir_folders(tmp_path, include_hidden, files_count) -> None:
    folder = tmp_path.joinpath("folder")
    folder.mkdir()
    file_1 = folder.joinpath("file_1.txt")
    file_1.write_text("file_1")
    file_2 = folder.joinpath("file_2.txt")
    file_2.write_text("file_2")
    hidden_file = folder.joinpath(".hidden_file.txt")
    hidden_file.write_text("hidden_file")
    result = ProcessObject.check_dir_folders([str(folder)], include_hidden=include_hidden)
    assert len(result) == files_count