from datetime import datetime
from pathlib import Path
import config
import json

def create_folder(dir_name : Path):
    dir_name.mkdir(exist_ok=True)

def generate_log_name():
    now = datetime.now()
    return now.strftime("run_%Y-%m-%d_%H-%M.json")

def save_log(operations : list):
    log_name = generate_log_name()
    target_place = config.LOG_DIR / log_name

    with open(target_place, "w") as file:
        json.dump(operations,file,indent=4)

