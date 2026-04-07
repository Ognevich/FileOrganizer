from colorama import Fore, Style, init
from pathlib import Path
init()

def print_sort_info(category : str, item : Path, target_folder : str, dry_mode = False):
    dry_text = "[DRY RUN]" if dry_mode else ""
    
    print(f"{Fore.GREEN}{dry_text}{Style.RESET_ALL} "
    f"{Fore.BLUE}[{category}]{Style.RESET_ALL} "
    f"{item} -> {target_folder}")

def add_operation(operations : list, item : Path, target : Path):
    operations.append(
        {
            "from": str(item),
            "to": str(target)
        }
    )

def amount_active_flags(flags : dict) -> int:
    return sum(flags.values())