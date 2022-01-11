class OwnFiles(object):
    def __init__(
        self, 
        file_path_of_own_examples: str, 
        file_path_of_own_definitions: str,
        file_path_of_vocabularies_to_scrape: str):

        examples = OwnFiles.get_list_separated_by_vocabulary(file_path_of_own_examples)
        definitions = OwnFiles.get_list_separated_by_vocabulary(file_path_of_own_definitions)
        self.vocabularies_to_scrape = OwnFiles.get_list_separated_by_vocabulary(file_path_of_vocabularies_to_scrape)

        self.own_example_titles = OwnFiles.get_titles(examples)
        self.own_example_sentences = OwnFiles.get_sentences(examples)
        self.dict_of_own_examples = OwnFiles.get_dict_of_vocabularies(examples)

        self.own_definition_titles = OwnFiles.get_titles(definitions)
        self.own_definition_sentences = OwnFiles.get_sentences(definitions)
        self.dict_of_own_definitions = OwnFiles.get_dict_of_vocabularies(definitions)


    @classmethod
    def get_list_separated_by_vocabulary(cls, path):
        ''' '''
        print('Retrieve examples')
        with open(path, 'r') as f:            
            data = f.read()
            examples = None
            if data:
                examples = data.split("\n\n")
            
        return examples


    @classmethod
    def get_titles(cls, vocabularies):
        ''' '''
        own_titles = None
        if vocabularies:
            own_titles = [vocabulary.split("\n")[0].lower() for vocabulary in vocabularies]            
        return own_titles


    @classmethod
    def get_sentences(cls, vocabularies):
        ''' '''
        sentences = None
        if vocabularies:
            sentences = [vocabulary.split("\n")[1] for vocabulary in vocabularies]            
        return sentences


    @classmethod
    def get_dict_of_vocabularies(cls, vocabularies):
        ''' '''
        dict_of_own_examples = None
        if vocabularies:
            dict_of_own_examples = [{'title': vocabulary.split("\n")[0].lower(), 'sentences': vocabulary.split("\n")[1]} for vocabulary in vocabularies]
            
        return dict_of_own_examples


    def get_urls_for_scraping(self, scraping_url):
        urls = []

        for title in self.vocabularies_to_scrape:
            url = scraping_url + title
            urls.append(url)
        return urls