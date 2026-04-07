import os
from pathlib import Path
import shutil
import extensions
import config
import utils
import file_operations

def validate_commands(commands : dict):
    validate_path_argument(commands)
    res = validate_directories(commands[config.PATH])
    if res:
        raise ValueError(f"directories {','.join(res)} doesn't exists")

    check_specifiers(commands)


def run_actions(commands : dict):
    if commands["flags"][config.SORT]:
        operations = organize_files(commands[config.PATH], 
                       commands["flags"][config.DRY_RUN], 
                       commands["flags"][config.RECURSIVE])
        if not commands["flags"][config.DRY_RUN]:
            file_operations.save_log(operations)


def organize_files(dir_list: list, 
                   dry_mode: bool = False, 
                   recursive_mode: bool = False,
                   operations = None):

    if operations is None:
        operations = []

    for dir_path in dir_list:
        path = Path(dir_path)

        for item in path.iterdir():
            if item.is_file():
                move_file(item, path, dry_mode, operations)
            if item.is_dir() and recursive_mode:
                organize_files([item],dry_mode, recursive_mode, operations)
    
    return operations


def move_file(item: Path, base_path: Path, dry_mode: bool, operations : list):
    category = get_category(item)
    target_folder = base_path / category
    target = target_folder / item.name

    if target.exists():
        target = target_folder / f"{item.stem}_copy{item.suffix}"

    if dry_mode:
        utils.print_sort_info(category,item,target_folder,dry_mode=True)
        return

    target_folder.mkdir(exist_ok=True)

    try:
        shutil.move(str(item), str(target))
        
        utils.add_operation(operations, item, target)

        utils.print_sort_info(category, item, target_folder)
    except Exception as e:
        print(f"Error moving {item}: {e}")

          
def get_category(file_path : Path) -> str:
    ext = file_path.suffix.lower()
    for category, ext_tuple in extensions.CATEGORIES.items():
        if ext in ext_tuple:
            return category
    return "other"

def validate_path_argument(commands : dict) -> bool:
    if commands[config.PATH]:
        return True
    raise ValueError(f"Error: argument {config.PATH} not found")

def handle_help(commands : dict) -> bool:
    if check_single_flag_validation(commands, config.HELP):
        execute_help()
        return True 
    return False  

def handle_undo(commands : dict) -> bool:
    
    if check_single_flag_validation(commands, config.UNDO):
        execute_undo()
        return True
    return False

def check_single_flag_validation(commands : dict, flag : str) -> bool:
    status =  commands["flags"].get(flag, False)

    if utils.amount_active_flags(commands["flags"]) > 1:
        raise ValueError(f"Error: The {flag} flag cannot be combined with other flags") 

    return status 

def check_specifiers(commands : dict):
    active = any(
        key != config.PATH and value
        for key, value in commands["flags"].items()
    )

    if not active:
        msg = f"Error: A program must have at least one specifier.\n To see all specifiers type {config.HELP} command"
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
        f"{config.PATH} <folder list>  -- adding directories to check\n"
        f"{config.SORT}                -- sort files in directory\n"
        f"{config.HELP}                -- show help\n"
        f"{config.RECURSIVE}           -- an additional flag used with {config.SORT} to sort in this directory as well as all subdirectories\n"
        f"{config.DRY_RUN}             -- an additional flag used to execute commands in safe mode. Changes will not be applied\n"               
    )
            
    print(text)

def execute_undo():

    filename = file_operations.find_last_log()
    if not filename:
        print("History is clear!")
        return

    full_path = config.LOG_FOLDER + "\\" + filename

    data = file_operations.read_from_json(full_path)

    for dct in data:

        src = dct["to"]   
        dst = dct["from"] 

        try:
            shutil.move(src, dst)


            parent_dir = Path(src).parent

            if parent_dir.exists() and not any(parent_dir.iterdir()):
                parent_dir.rmdir()  

        except Exception as e:
            print(f"Error moving {src}: {e}")

    path = Path(full_path)
    path.unlink()
    

# DEBUGGING 
def get_dir_info(path : Path):
    for item in path.iterdir():
        print(item)         
        print(item.name)     
        print(item.suffix)  
        print(item.is_file())
        print(item.is_dir())
        print("-----")

