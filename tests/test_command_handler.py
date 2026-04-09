import pytest
import command_handler
from config import HELP, PATH, SORT
import config

def  validate_path_directories(tmp_path):
    valid_dir = tmp_path
    invalid_dir = tmp_path / "not_exists"

    result = command_handler.validate_directories([valid_dir, invalid_dir])

    assert str(invalid_dir) in result
    assert str(valid_dir) not in result


def test_get_category_known_extension(tmp_path):
    file = tmp_path / "test.txt"
    file.touch()

    cat = command_handler.get_category(file)
    assert cat == "TXT"

def test_get_category_unknown_extension(tmp_path):
    file = tmp_path / "test.unknown"
    file.touch()

    cat = command_handler.get_category(file)
    assert cat == "other"

def test_specifiers_raises():
    commands = {PATH: ["folder1"],
                "flags": {HELP: False,
                            SORT: False}}
    
    with pytest.raises(ValueError):
        command_handler.check_specifiers(commands)

def test_specifiers_with_ok():
    commands = {PATH: ["folder1"],
                "flags": {HELP: True,
                            SORT: False}}
    
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

    command_handler.organize_files([tmp_path],['TXT'])

    target = tmp_path / "TXT" / "test.txt"

    assert target.exists()
    

def test_organize_dry_run_files(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello")

    command_handler.organize_files([tmp_path],["TXT"],True)

    target = tmp_path / "TXT" / "test.txt"
    assert file.exists()

def test_organize_recursive(tmp_path):
    file = tmp_path / "text.txt"
    file.write_text("hello")

    new_folder = tmp_path / "new_folder"
    new_folder.mkdir(exist_ok=True)

    new_file = new_folder / "anothertext.txt"
    new_file.write_text("text")

    command_handler.organize_files([tmp_path], ["TXT"],recursive_mode=True)

    target1 = tmp_path / "TXT" / "text.txt"
    target2 = tmp_path / "new_folder" / "TXT" / "anothertext.txt"

    assert not file.exists()
    assert not new_file.exists()

    assert target1.exists()
    assert target2.exists()

def test_mode_modifiers():
    commands = {
        PATH: ["folder1"],
        config.MODE: ["txt", "img"],
        "flags": {
            HELP: False,
            SORT: False
        }
    }

    result = command_handler.validate_mode(commands)

    assert result is True
    assert commands[config.MODE] == ["TXT", "IMG"]