import pytest
import command_handler
from config import HELP, PATH, SORT

def test_validate_directories(tmp_path):
    valid_dir = tmp_path
    invalid_dir = tmp_path / "not_exists"

    result = command_handler.validate_directories([valid_dir, invalid_dir])

    assert str(invalid_dir) in result
    assert str(valid_dir) not in result


def test_get_category_known_extension(tmp_path):
    file = tmp_path / "test.txt"
    file.touch()

    cat = command_handler.get_category(file)
    assert cat == "text"

def test_get_category_unknown_extension(tmp_path):
    file = tmp_path / "test.unknown"
    file.touch()

    cat = command_handler.get_category(file)
    assert cat == "other"

def test_specifiers_raises():
    commands = {PATH: ["folder1"],
                HELP: False,
                SORT: False}
    
    with pytest.raises(ValueError):
        command_handler.check_specifiers(commands)

def test_specifiers_with_ok():
    commands = {PATH: ["folder1"],
                HELP: True,
                SORT: False}
    
    command_handler.check_specifiers(commands)


def test_validate_path_argument_ok():
    commands = {"--path": ["dir"]}
    assert command_handler.validate_path_argument(commands)

def test_validate_path_argument_fail():
    commands = {"--path": []}

    with pytest.raises(ValueError):
        command_handler.validate_path_argument(commands)

def test_organize_files(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")

    command_handler.organize_files([tmp_path])

    target = tmp_path / "text" / "test.txt"
    assert target.exists()

def test_organize_dry_run_files(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")

    command_handler.organize_files([tmp_path],True)

    target = tmp_path / "text" / "test.txt"
    assert file.exists()