import requests

import bs4

from models.vocabulary import Vocabulary

class Scraping(object):
    def __init__(self):
        self.headers_dic = None

        # Set up elements for each columns
        self.title = None
        self.substitution_title = None
        self.parts_of_speech = None
        self.us_pronunciation = None
        self.uk_pronunciation = None
        self.definition = None
        self.example = None


    def get_vocabulary(self, vocabulary: Vocabulary, soup) -> Vocabulary:
        # Get data via scraping
        print(vocabulary)
        vocabulary.title            = soup.select(self.title,            limit=1)[0].text if soup.select(self.title, limit=1) else self.substitution_title
        vocabulary.part_of_speech   = soup.select(self.parts_of_speech,  limit=1)[0].text if soup.select(self.parts_of_speech, limit=1) else ''
        vocabulary.us_pronunciation = soup.select(self.us_pronunciation, limit=1)[0].text if soup.select(self.us_pronunciation, limit=1) else ''
        vocabulary.uk_pronunciation = soup.select(self.uk_pronunciation, limit=1)[0].text if soup.select(self.uk_pronunciation, limit=1) else ''
        vocabulary.definition       = soup.select(self.definition,       limit=1)[0].text if soup.select(self.definition, limit=1) else ''
        vocabulary.example_sentence = soup.select(self.example,          limit=1)[0].text if soup.select(self.example, limit=1) else ''

        # Remove unnecessary blank
        vocabulary.definition = vocabulary.definition.lstrip()

        return vocabulary


    def scrape(self, url) ->Vocabulary:
        '''Get vocabulary data from cambridge'''
        vocabulary = Vocabulary()

        # Get the substitution vocabulary's title from url parameter
        self.substitution_title = url.split('/')[-1]

        html = requests.get(url, headers=self.headers_dic)
        soup = bs4.BeautifulSoup(html.content, "html.parser")

        vocabulary = self.get_vocabulary(vocabulary, soup)

        print("[INFO] - SCRAPED URL:", url)
        print("[INFO] - SCRAPED TITLE:", vocabulary.title)
        print("[INFO] - SCRAPED PARTS OF SPEECH:", vocabulary.part_of_speech)
        print("[INFO] - SCRAPED US_PRONUNCIATION:", vocabulary.us_pronunciation)
        print("[INFO] - SCRAPED UK_RONUNCIATION:", vocabulary.uk_pronunciation)
        print("[INFO] - SCRAPED DEFINITION:", vocabulary.definition)
        print("[INFO] - SCRAPED EXAMPLE SENTENCE:", vocabulary.example_sentence)
        
        return vocabulary