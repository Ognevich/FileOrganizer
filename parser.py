import config

def parse_commands(argv : list) -> dict:
    commands = {config.PATH: [],
                config.MODE: [],
                config.IGNORE: [],
                config.FILE:   [],
                "flags": {
                    config.HELP:        False,
                    config.SORT:        False,
                    config.DRY_RUN:     False,
                    config.RECURSIVE:   False,
                    config.UNDO:        False
                }}
    
    flags = (config.SORT,config.HELP, config.DRY_RUN, config.RECURSIVE, config.UNDO)
    main_attributes = (config.PATH, config.MODE, config.IGNORE, config.FILE)

    i = 1
    list_len = len(argv)

    while i < list_len:
        
        arg = argv[i]
        
        if arg in main_attributes:
            i += 1
            if i >= list_len:
                raise ValueError(f"Error: missing argument after {arg}' ")
            if  argv[i].startswith("--"):
                raise ValueError(f"Error: missing argument after {arg} ")
            while i < list_len and not argv[i].startswith("--"):
                commands[arg].append(argv[i])
                i += 1
            continue
        elif arg in flags:
            commands["flags"][arg] = True
        else:
            raise ValueError(f"Error: Unknown argument: {arg}")
        i += 1

    return commands