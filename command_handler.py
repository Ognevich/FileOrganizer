import os
from pathlib import Path
import shutil
import extensions
from config import PATH, HELP, SORT

def handle_help(commands : dict) -> bool:
    if check_help(commands):
        execute_help()
        return True 
    return False  

def validate_commands(commands : dict):
    validate_path_argument(commands)
    res = validate_directories(commands[PATH])
    if res:
        raise ValueError(f"directories {','.join(res)} doesn't exists")

    check_specifiers(commands)

def run_actions(commands : dict):
    if commands[SORT]:
        organize_files(commands[PATH])

def validate_path_argument(commands : dict) -> bool:
    if commands[PATH]:
        return True
    raise ValueError(f"Error: argument {PATH} not found")

def check_help(commands : dict) -> bool:
    return commands.get(HELP, False)

def check_specifiers(commands : dict):
    active = any(
        key != PATH and value
        for key, value in commands.items()
    )

    if not active:
        msg = f"Error: A program must have at least one specifier.\n To see all specifiers type {HELP} command"
        raise ValueError(msg)

def validate_directories(directories: list) -> list:
    return [
        str(Path(dir).expanduser())
        for dir in directories
        if not Path(dir).expanduser().is_dir()
    ]

def execute_help():
    
    text = (
        "------------------------HELP-----------------------\n"
        f"{PATH} <folder list>  -- adding directories to check\n"
        f"{SORT}                -- sort files by directory\n"
        f"{HELP}                -- show help\n"
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

                target = target_folder / item.name

                if target.exists():
                    target = target_folder / f"{item.stem}_copy{item.suffix}"

                try:
                    shutil.move(str(item), str(target))
                    print(f"Moved {item.name} -> {category}")
                except Exception as e:
                    print(f"Error moving {item}: {e}")
                
def get_category(file_path : Path) -> str:
    ext = file_path.suffix.lower()
    for category, ext_tuple in extensions.CATEGORIES.items():
        if ext in ext_tuple:
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

    