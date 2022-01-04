class Result(object):
    def __init__(self):
        self.vocabularies_scraped = []
        self.vocabularies_not_scraped = []
        self.vocabularies_written = []
        self.vocabularies_existed = []
        self.examples_written = []
        self.examples_not_written = []
        self.difinitions_written = []
        self.difinitions_not_written = []

    
    def write_files_for_result(self, file_path_and_result):
        text_lists = []
        for vocabulary in file_path_and_result['result']:
            text_lists.append(vocabulary.title + "\n")
            text_lists.append(vocabulary.example_sentence + "\n\n")

        with open(file_path_and_result['file_path'], 'w') as f:
            f.writelines(text_lists)