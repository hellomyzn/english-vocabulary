import os
import pathlib

import conversation as conv


def is_file(path: str):
    if os.path.isfile(path):
        return True
    conv.say_something(f"There is no '{path}'")
    return False

def create_file(path: str):
    conv.say_something(f"Creat a file on {path}")
    pathlib.Path(path).touch()

def check_and_create_file(path: str):
    if not os.path.isfile(path):
        
        pathlib.Path(path).touch()

def remove_file(path: str):
    os.remove(path)