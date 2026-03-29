import command_handler
import parser
import sys

def run():
    commands = parser.parse_commands(sys.argv)
    command_handler.check_path(commands)

    define_action(commands)


def define_action(act_dict : dict):

    res = command_handler.error_directories(act_dict["--path"])
        
    if res:
        raise ValueError(f"directories {','.join(res)} doesn't exists")




            