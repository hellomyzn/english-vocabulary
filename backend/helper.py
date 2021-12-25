import os
import pathlib

import conversation as conv


def is_file(path: str):
    if os.path.isfile(path):
        return True
    return False


def check_file(path: str):
    if not os.path.isfile(path):
        conv.say_something(f"Creat a file on {path}")
        pathlib.Path(path).touch()