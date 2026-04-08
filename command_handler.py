import os
from pathlib import Path
import shutil
import extensions
import config
import utils
import file_operations

def validate_commands(commands : dict):
    validate_path_argument(commands)
    
    res_path = validate_path_directories(commands[config.PATH])

    if res_path:
        raise ValueError(f"directories {','.join(res_path)} doesn't exists")
    
    check_specifiers(commands)
    
def validate_mode(commands: dict) -> bool:
    modes = commands.get(config.MODE, [])

    if not modes:
        commands[config.MODE] = list(extensions.CATEGORIES.keys())
        return True

    normalized = [arg.upper() for arg in modes]

    if not all(arg in extensions.CATEGORIES for arg in normalized):
        return False

    commands[config.MODE] = normalized
    return True

def run_actions(commands : dict):
    
    if handle_help(commands):
        return 
    elif commands["flags"][config.UNDO]:
        execute_undo(commands)
        return
    elif commands["flags"][config.SORT]:

        validate_commands(commands)

        res = validate_mode(commands)
        
        if not res:
            raise ValueError(f"Error: unknown mode modifier. To see all modifiers type {config.HELP}")

        operations = organize_files(commands[config.PATH], 
                                    commands[config.MODE],
                       commands["flags"][config.DRY_RUN], 
                       commands["flags"][config.RECURSIVE])
        if not commands["flags"][config.DRY_RUN]:
            file_operations.save_log(operations)


def organize_files(dir_list: list,
                   mode_list: list, 
                   dry_mode: bool = False, 
                   recursive_mode: bool = False,
                   operations = None):

    if operations is None:
        operations = []

    for dir_path in dir_list:
        path = Path(dir_path)

        for item in path.iterdir():
            if item.is_file() and get_category(item) in mode_list:
                move_file(item, path, dry_mode, operations)
            if item.is_dir() and recursive_mode:
                organize_files([item],mode_list,dry_mode, recursive_mode, operations)
    
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

def check_single_flag_validation(commands : dict, flag : str) -> bool:
    status =  commands["flags"].get(flag, False)
    if not status:
        return False

    if utils.amount_active_flags(commands["flags"]) > 1:
        raise ValueError(f"Error: The {flag} flag cannot be combined with other flags") 

    return True 

def check_specifiers(commands : dict):
    active = any(
        key != config.PATH and value
        for key, value in commands["flags"].items()
    )

    if not active:
        msg = f"Error: A program must have at least one specifier.\n To see all specifiers type {config.HELP} command"
        raise ValueError(msg)

def validate_path_directories(directories: list) -> list:
    return [
        str(Path(dir).expanduser())
        for dir in directories
        if not Path(dir).expanduser().is_dir()
    ]

def validate_mode_arguments(args : list) -> bool:
    return any([arg for arg in args if arg not in config.modifiers])

def execute_help():
    
    text = (
        "\n====================== HELP ======================\n\n"
        
        "Usage:\n"
        f"  {config.PATH} <folder1> <folder2> ...\n"
        "      Add directories to process\n\n"
        
        "Main commands:\n"
        f"  {config.SORT}\n"
        "      Sort files in specified directories\n\n"
        
        f"  {config.HELP}\n"
        "      Show this help message\n\n"

        f"  {config.UNDO}\n"
        "      Revert last operation using saved logs\n"
        "      (works only if files were not modified or deleted manually)\n\n"
        "Optional flags:\n"

        f"  {config.RECURSIVE}\n"
        f"      Use with {config.SORT} to process subdirectories recursively\n\n"
        
        f"  {config.DRY_RUN}\n"
        "      Run in safe mode (no actual changes will be made)\n\n"
        
        "=================================================\n"
    )
            
    print(text)

def execute_undo(commands: dict):
    
    dry_run = commands["flags"].get(config.DRY_RUN, False)

    for name, value in commands["flags"].items():
        if value and name not in (config.DRY_RUN, config.UNDO):
            raise ValueError("Error: undo operation can only contain dry-run flag")
    
    filename = file_operations.find_last_log()
    
    if not filename:
        print("History is clear!")
        return

    full_path = config.LOG_DIR / filename
    data = file_operations.read_from_json(full_path)

    move_back(data, dry_run)

    if not dry_run:
        full_path.unlink()
    
def move_back(data: list, dry_run=False):
    for dct in data:
        src = Path(dct["to"])
        dst = Path(dct["from"])

        if dry_run:
            utils.print_dry_run_text(str(src), str(dst))
            continue

        try:
            shutil.move(src, dst)
            print(f"{src} -> {dst}")

            parent_dir = src.parent
            if parent_dir.exists() and not any(parent_dir.iterdir()):
                parent_dir.rmdir()

        except Exception as e:
            print(f"Error moving {src}: {e}")

# DEBUGGING 
def get_dir_info(path : Path):
    for item in path.iterdir():
        print(item)         
        print(item.name)     
        print(item.suffix)  
        print(item.is_file())
        print(item.is_dir())
        print("-----")

