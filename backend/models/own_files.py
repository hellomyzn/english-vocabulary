class OwnFiles(object):
    def __init__(self, 
        file_path_of_own_examples: str, 
        file_path_of_own_definitions: str):

        # Get own vocabularies you write on own files
        own_examples                = OwnFiles.get_list_separated_by_vocabulary(file_path_of_own_examples)
        own_definitions             = OwnFiles.get_list_separated_by_vocabulary(file_path_of_own_definitions)
        # self.vocabularies_to_scrape = OwnFiles.get_list_separated_by_vocabulary(file_path_of_vocabularies_to_scrape)

        # Get own example of title, sentence and dict[title, sentence]
        self.own_example_titles     = OwnFiles.get_own_titles(own_examples)
        self.own_example_sentences  = OwnFiles.get_own_sentences(own_examples)
        self.dict_of_own_examples   = OwnFiles.get_dict_of_vocabularies(own_examples)
        
        # Get own definition of title, sentence and dict[title, sentence]
        self.own_definition_titles      = OwnFiles.get_own_titles(own_definitions)
        self.own_definition_sentences   = OwnFiles.get_own_sentences(own_definitions)
        self.dict_of_own_definitions    = OwnFiles.get_dict_of_vocabularies(own_definitions)


    @classmethod
    def get_list_separated_by_vocabulary(cls, path):
        """
        Get own vocabularies list separated by vocabulary.

        Args:
            path: file path you want to get own vocabularies.

        Returns:
            own_vocabularies: list of own vocabularies separated by vocabulary.
                              if there is no own vocabularies in the path, return None.
        """
        print(f'Retrieve data from {path}')
        with open(path, 'r') as f:            
            data = f.read()
            own_vocabularies = None
            if data:
                own_vocabularies = data.split("\n\n")
            
        return own_vocabularies


    @classmethod
    def get_own_titles(cls, vocabularies):
        """
        Get own vocabulary's title list.

        Args:
            vocabularies: own vocabularies separated by vocabulary from own file.

        Returns:
            own_titles: get only titles from vocabularies. if there is no own vocabularies in the path, return None.
        """
        own_titles = None
        if vocabularies:
            own_titles = [vocabulary.split("\n")[0].lower().rstrip() for vocabulary in vocabularies]            
        return own_titles


    @classmethod
    def get_own_sentences(cls, vocabularies):
        """
        Get own vocabulary's senteneces list.

        Args:
            vocabularies: own vocabularies separated by vocabulary from own file.

        Returns:
            own_titles: get only sentences from vocabularies. if there is no own vocabularies in the path, return None.
        """
        own_sentences = None
        if vocabularies:
            own_sentences = [vocabulary.split("\n")[1] for vocabulary in vocabularies]            
        return own_sentences


    @classmethod
    def get_dict_of_vocabularies(cls, vocabularies):
        """
        Get own vocabularies dict separated by vocabulary

        Args:
            path: file path you want to get own vocabularies

        Returns:
            dict_of_own_vocabularies: dict of own vocabularies separated by vocabulary.
                                      if there is no own vocabularies in the path, return None.
        """
        dict_of_own_vocabularies = None
        if vocabularies:
            dict_of_own_vocabularies = [{'title': vocabulary.split("\n")[0].lower(), 'sentences': vocabulary.split("\n")[1]} for vocabulary in vocabularies]
            
        return dict_of_own_vocabularies


    def get_urls_for_scraping(self, file_path_of_vocabularies_to_scrape, scraping_url) -> list:
        """
        Get the list of the urls

        Args:
            scraping_url: the web site urls for scraping.

        Returns:
            urls: the list of urls for scraping from user's Google Chrome Bookmarks
        """
        print("[INFO] - Get urls from vocabularies_to_scrape file")
        urls = []
        vocabularies_to_scrape = OwnFiles.get_list_separated_by_vocabulary(file_path_of_vocabularies_to_scrape)
        if vocabularies_to_scrape:
            for title in vocabularies_to_scrape:
                url = scraping_url + title
                urls.append(url)
            return urls
        else:
            print("[WRITING] - There is no vocabulary on 'vocabularies_to_scrape file'")
            quit()
