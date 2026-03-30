

def parse_commands(argv : list) -> dict:
    commands = {"--path": [],
                "--help": False,
                "--o": False}

    print(argv)
    
    i = 1
    list_len = len(argv)

    while i < list_len:
        
        arg = argv[i]
        
        if arg == "--path":
            i += 1
            if i >= list_len:
                raise ValueError("Error: missing <folder_name> argument after '--path' ")
            if  argv[i].startswith("--"):
                raise ValueError("Error: missing <folder_name> argument '--path' ")
            while i < list_len and not argv[i].startswith("--"):
                commands["--path"].append(argv[i])
                i += 1
            continue

        elif arg in ('--o', "--help"):
            commands[arg] = True
        else:
            raise ValueError(f"Error: Unknown argument: {arg}")
        i += 1

    return commands