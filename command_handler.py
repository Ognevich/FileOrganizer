import os


def check_path(commands : dict):
    if commands["--path"]:
        return True
    raise ValueError("Error: argument '--path' not found")

def error_directories(directories : list) -> list:
    error_list = [dir for dir in directories if not os.path.isdir(dir)]
    return error_list
