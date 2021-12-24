import csv

def write_csv(vocabularies: list):
    '''Write vacabularies on CSV(/backend/data/vocabularies.csv)'''

    with open('data/vocabularies.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'parts of speach', 'us pronunciation', 'uk pronunciation', 'definition', 'example sentence']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for vocabulary in vocabularies:
            writer.writerow({'title': vocabulary['title'],
                            'parts_of_speach': vocabulary['parts_of_speechs'],
                            'us_pronunciation': vocabulary['us_pronunciation'],
                            'uk_pronunciation': vocabulary['uk_pronunciation'],
                            'definition': vocabulary['definition'],
                            'example_sentence': vocabulary['example_sentence']})
