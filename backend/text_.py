import os
import pathlib

import conversation as conv


def is_exist_examples():
    with open('data/examples.txt', 'r', newline='') as txt:
        data = txt.readline()

        if not data:
            conv.say_something("There is no example sentence you write on 'data/examples.txt'")
            return False
        return True


def get_list_of_example():
    '''Get list including dict from data/examples.txt'''
    
    with open('./data/examples.txt', 'r') as f:
        # SBV = Suplited by Vocabulary
        examples_SBV = f.read().split("\n\n")
        examples = [{'title': example.split("\n")[0], 'example_sentence': example.split("\n")[1]} for example in examples_SBV]
        
    return examples