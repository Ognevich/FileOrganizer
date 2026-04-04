import pytest
from config import PATH, SORT, HELP
import config
from parser import parse_commands

def test_single_path():
    argv = ["main.py", PATH , "folder1"] 

    result = parse_commands(argv)

    assert result[PATH] == ["folder1"]
    assert result[HELP] is False
    assert result[SORT] is False

def test_multiple_path():
    argv = ["main.py", PATH, "folder1", "folder2", "folder3"]

    result = parse_commands(argv)

    assert result[PATH] == ["folder1", "folder2", "folder3"]

def test_help():
    argv = ["main.py", HELP]

    result = parse_commands(argv)

    assert result[HELP] == True

def test_sort_flag():
    argv = ["main.py", SORT]
    result = parse_commands(argv)

    assert result[SORT] is True

def test_dry_run_flag():
    argv = ["main.py", config.DRY_RUN]
        
    result = parse_commands(argv)

    assert result[config.DRY_RUN] == True

def test_combined_args():
    argv = ["main.py", PATH, "folder1", SORT]
    result = parse_commands(argv)

    assert result[PATH] == ["folder1"]
    assert result[SORT] is True

def test_missing_path_value():
    argv = ["main.py", PATH]

    with pytest.raises(ValueError):
        parse_commands(argv)

def test_path_before_flag():
    argv = ["script.py", PATH, HELP]

    with pytest.raises(ValueError):
        parse_commands(argv)


def test_unknown_argument():
    argv = ["script.py", "--unknown"]

    with pytest.raises(ValueError):
        parse_commands(argv)

def test_empty_result():
    argv = ["script.py"]

    res = parse_commands(argv)

    assert res[PATH] == []

def test_argument_order():
    argv = ["main.py", PATH, "folder1", SORT]
    result = parse_commands(argv)

    assert result[SORT] == True
    assert result[PATH] == ["folder1"]

