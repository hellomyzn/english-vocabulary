import csv

from interfaces import table

class CSV(table.Table):
    def __init__(self, columns: dict):
        self.columns = columns

    @classmethod
    def create_columns(cls, url, columns):
        print('Create header on CSV')
        with open(url, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
    @classmethod
    def is_not_columns(cls, url):
        with open(url, 'r', newline='') as csvfile:
            data = csvfile.readline()
            if not data:
                return True
            else:
                return False

    def write(self, vocabulary, url):
        if CSV.is_not_columns(url):
            CSV.create_columns(url, self.columns)

        vocabulary_dict = {}
        for i, column in enumerate(self.columns, start=1):
            vocabulary_dict[column] = getattr(vocabulary, column)

        with open(url, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.columns)
            writer.writerow(vocabulary_dict)
            print(f"WRITING: {column}:", getattr(vocabulary, column))
        return