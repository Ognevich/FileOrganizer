import config

def parse_commands(argv : list) -> dict:
    commands = {config.PATH: [],
                "flags": {
                    config.HELP: False,
                    config.SORT: False,
                    config.DRY_RUN: False,
                    config.RECURSIVE: False
                }}
    
    flags = (config.SORT,config.HELP, config.DRY_RUN, config.RECURSIVE)

    i = 1
    list_len = len(argv)

    while i < list_len:
        
        arg = argv[i]
        
        if arg == config.PATH:
            i += 1
            if i >= list_len:
                raise ValueError("Error: missing <folder_name> argument after '--path' ")
            if  argv[i].startswith("--"):
                raise ValueError("Error: missing <folder_name> argument '--path' ")
            while i < list_len and not argv[i].startswith("--"):
                commands[config.PATH].append(argv[i])
                i += 1
            continue

        elif arg in flags:
            commands["flags"][arg] = True
        else:
            raise ValueError(f"Error: Unknown argument: {arg}")
        i += 1

    return commands