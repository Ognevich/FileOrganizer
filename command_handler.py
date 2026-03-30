import os
from pathlib import Path
import shutil
import extensions

def check_path(commands : dict) -> bool:
    if commands["--path"]:
        return True
    raise ValueError("Error: argument '--path' not found")

def check_help(commands : dict) -> bool:
    return commands.get('--help', False)

def check_specifiers(act_dict : dict):
    is_active = 0
    for key, value in act_dict.items():
        is_active = is_active + 1 if key != "--path" and value else is_active + 0 

    if not is_active:
        msg = "Error: A program must have at least one specifier.\n To see all specifiers type --help command"
        raise ValueError(msg)

def error_directories(directories: list) -> list:
    return [
        str(Path(dir).expanduser())
        for dir in directories
        if not Path(dir).expanduser().is_dir()
    ]

def execute_help():
    
    text = (
        "------------------------HELP-----------------------\n"
        "--path <folder list> -- adding directories to check\n"
        "--o                  -- sort files by directory\n"
        "--help               -- show help\n"
    )
            
    print(text)

def organize_files(dir_list : list):

    for dir in dir_list:
        path = Path(dir)

        for item in path.iterdir():
            if item.is_dir():
                continue
            elif item.is_file():
                category = get_category(item)
                target_folder = path/category
                target_folder.mkdir(exist_ok=True)

                shutil.move(str(item), str(target_folder / item.name))
                print(f"Moved {item.name} -> {category}")
                
def get_category(file_path : Path) -> str:
    ext = file_path.suffix.lower()
    for category, ext_turple in extensions.CATEGORIES.items():
        if ext in ext_turple:
            return category
    return "other"

# DEBUGGING 
def get_dir_info(path : Path):
    for item in path.iterdir():
        print(item)         
        print(item.name)     
        print(item.suffix)  
        print(item.is_file())
        print(item.is_dir())
        print("-----")