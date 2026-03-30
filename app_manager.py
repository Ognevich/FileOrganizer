import command_handler
import parser
import sys

def run():
    commands = parser.parse_commands(sys.argv)
    define_action(commands)

def define_action(act_dict : dict):

    if command_handler.check_help(act_dict):
        command_handler.execute_help()
        return

    command_handler.check_path(act_dict)
    res = command_handler.error_directories(act_dict["--path"])
    if res:
        raise ValueError(f"directories {','.join(res)} doesn't exists")

    command_handler.check_specifiers(act_dict)

    if act_dict['--o']:
        command_handler.organize_files(act_dict['--path'])


    
    




            