class OwnExampleSentence(object):
    def __init__(self, path: str):
        examples = OwnExampleSentence.create_example_list_from_txt(path)

        self.titles = OwnExampleSentence.get_titles(examples)
        self.example_sentences = OwnExampleSentence.get_example_sentences(examples)
        self.dict_of_examples = OwnExampleSentence.get_dict_of_examples(examples)


    @classmethod
    def create_example_list_from_txt(cls, path):
        ''' '''
        print('Retrieve examples')
        with open(path, 'r') as f:            
            data = f.read()

            if data:
                examples = data.split("\n\n")
            
        return examples


    @classmethod
    def get_titles(cls, examples):
        ''' '''
        titles = [example.split("\n")[0] for example in examples]            
        return titles


    @classmethod
    def get_example_sentences(cls, examples):
        ''' '''
        example_sentences = [example.split("\n")[1] for example in examples]            
        return example_sentences


    @classmethod
    def get_dict_of_examples(cls, examples):
        ''' '''
        dict_of_examples = [{'title': example.split("\n")[0], 'example_sentence': example.split("\n")[1]} for example in examples]
            
        return dict_of_examples


    def get_urls_for_scraping(self, scraping_url):
        urls = []
        for title in self.titles:
            url = scraping_url + title
            urls.append(url)
        return urls