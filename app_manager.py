import command_handler
import parser
import sys
import file_operations
import config

def run():
    try:
        commands = parser.parse_commands(sys.argv)
        execute_commands(commands)
    except ValueError as e:
        print(f"{e}")
        sys.exit(1)

def execute_commands(commands : dict):

    file_operations.create_folder(config.LOG_DIR)

    if command_handler.handle_help(commands):
        return 
    
    command_handler.validate_commands(commands)
    command_handler.run_actions(commands)


    
    




            