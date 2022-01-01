import requests

import bs4


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

    def get_vocabulary(self, url, vocabulary) ->dict:
        '''Get vocabulary data from cambridge'''
        # Get the substitution vocabulary's title from url parameter
        self.substitution_title = url.split('/')[-1]

        html = requests.get(url, headers=self.headers_dic)
        soup = bs4.BeautifulSoup(html.content, "html.parser")

        # Get data via scraping
        vocabulary.title            = soup.select(self.title,            limit=1)[0].text if soup.select(self.title, limit=1) else self.substitution_title
        vocabulary.part_of_speech   = soup.select(self.parts_of_speech,  limit=1)[0].text if soup.select(self.parts_of_speech, limit=1) else ''
        vocabulary.us_pronunciation = soup.select(self.us_pronunciation, limit=1)[0].text if soup.select(self.us_pronunciation, limit=1) else ''
        vocabulary.uk_pronunciation = soup.select(self.uk_pronunciation, limit=1)[0].text if soup.select(self.uk_pronunciation, limit=1) else ''
        vocabulary.definition       = soup.select(self.definition,       limit=1)[0].text if soup.select(self.definition, limit=1) else ''
        vocabulary.example_sentence = soup.select(self.example,          limit=1)[0].text if soup.select(self.example, limit=1) else ''
        vocabulary.is_own_example = False

        print("[SCRAPING]: URL:", url)
        print("[SCRAPING]: TITLE:", vocabulary.title)
        print("[SCRAPING]: Parts Of Speech:", vocabulary.part_of_speech)
        print("[SCRAPING]: US_PRONUNCIATION:", vocabulary.us_pronunciation)
        print("[SCRAPING]: UK_RONUNCIATION:", vocabulary.uk_pronunciation)
        print("[SCRAPING]: DEFINITION:", vocabulary.definition)
        print("[SCRAPING]: EXAMPLE SENTENCE:", vocabulary.example_sentence)
        
        return vocabulary