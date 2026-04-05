import command_handler
import parser
import sys

def run():
    try:
        commands = parser.parse_commands(sys.argv)
        execute_commands(commands)
    except ValueError as e:
        print(f"{e}")
        sys.exit(1)

def execute_commands(commands : dict):

    command_handler.create_log_folder()


    if command_handler.handle_help(commands):
        return 
    
    command_handler.validate_commands(commands)
    command_handler.run_actions(commands)


    
    




            