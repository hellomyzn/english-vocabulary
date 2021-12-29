import csv
import os
import pathlib

import conversation as conv


def check_columns(columns: list):
    with open('data/vocabularies.csv', 'r', newline='') as csvfile:
        data = csvfile.readline()

        if not data:
            with open('data/vocabularies.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=columns)
                writer.writeheader()
    return


def write_csv(columns: list, vocabulary: dict):
    '''Write vacabularies on CSV(/backend/data/vocabularies.csv)'''


