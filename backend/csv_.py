import csv

import subprocess

def write_csv(vocabularies: list):
    '''Write vacabularies on CSV(/backend/data/vocabularies.csv)'''

    with open('data/vocabularies.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'parts_of_speach', 'us_pronunciation', 'uk_pronunciation', 'definition', 'example_sentence']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for vocabulary in vocabularies:
            writer.writerow({'title': vocabulary['title'],
                            'parts_of_speach': vocabulary['parts_of_speech'],
                            'us_pronunciation': vocabulary['us_pronunciation'],
                            'uk_pronunciation': vocabulary['uk_pronunciation'],
                            'definition': vocabulary['definition'],
                            'example_sentence': vocabulary['example_sentence']})

