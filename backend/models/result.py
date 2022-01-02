class Result(object):
    def __init__(self):
        self.vocabularies_scraped = []
        self.vocabularies_not_scraped = []
        self.vocabularies_written = []
        self.vocabularies_existed = []
        self.vocabularies_not_written = []
        self.examples_written = []
        self.examples_not_written = []

    
    def create_file_for_result(self, file_path):
        print(file_path)