import os
import pathlib

def is_file(path: str):
    if os.path.isfile(path):
        return True
    return False

def create_file(path: str):
    pathlib.Path(path).touch()

def check_and_create_file(path: str):
    if not os.path.isfile(path):        
        pathlib.Path(path).touch()

def delete_file(path: str):
    os.remove(path)