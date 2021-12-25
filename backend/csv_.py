import csv
import os
import pathlib


def is_exsit_file():
    if not os.path.isfile('./data/vocabularies.csv'):
        pathlib.Path('./data/vocabularies.csv').touch()

def is_exist_columns(columns: list):
    with open('data/vocabularies.csv', 'r', newline='') as csvfile:
        data = csvfile.readline()

        if not data:
            with open('data/vocabularies.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
    return


def write_csv(columns: list, vocabulary: dict):
    '''Write vacabularies on CSV(/backend/data/vocabularies.csv)'''


    with open('data/vocabularies.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writerow(vocabulary)
    return