from config import PATH, HELP, SORT

def parse_commands(argv : list) -> dict:
    commands = {PATH: [],
                HELP: False,
                SORT: False}
    
    i = 1
    list_len = len(argv)

    while i < list_len:
        
        arg = argv[i]
        
        if arg == PATH:
            i += 1
            if i >= list_len:
                raise ValueError("Error: missing <folder_name> argument after '--path' ")
            if  argv[i].startswith("--"):
                raise ValueError("Error: missing <folder_name> argument '--path' ")
            while i < list_len and not argv[i].startswith("--"):
                commands[PATH].append(argv[i])
                i += 1
            continue

        elif arg in (SORT, HELP):
            commands[arg] = True
        else:
            raise ValueError(f"Error: Unknown argument: {arg}")
        i += 1

    return commands