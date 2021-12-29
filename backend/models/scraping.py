import json
import requests

import bs4

class Scraping(object):
    def __init__(self):
        self.headers_dic = None

        # Set up elements for each columns
        self.title = None
        self.parts_of_speech = None
        self.us_pronunciation = None
        self.uk_pronunciation = None
        self.definition = None
        self.example = None

    def scraping(self, url) ->dict:
        '''Get vocabulary data from cambridge'''
        
        html = requests.get(url, headers=self.headers_dic)
        soup = bs4.BeautifulSoup(html.content, "html.parser")

        # Get data via scraping
        vocabulary = {}
        vocabulary['title']            = soup.select(self.title,            limit=1)[0].text if soup.select(self.title, limit=1) else ''
        vocabulary['part_of_speech']   = soup.select(self.parts_of_speech,  limit=1)[0].text if soup.select(self.parts_of_speech, limit=1) else ''
        vocabulary['us_pronunciation'] = soup.select(self.us_pronunciation, limit=1)[0].text if soup.select(self.us_pronunciation, limit=1) else ''
        vocabulary['uk_pronunciation'] = soup.select(self.uk_pronunciation, limit=1)[0].text if soup.select(self.uk_pronunciation, limit=1) else ''
        vocabulary['definition']       = soup.select(self.definition,       limit=1)[0].text if soup.select(self.definition, limit=1) else ''
        vocabulary['example_sentence'] = soup.select(self.example,          limit=1)[0].text if soup.select(self.example, limit=1) else ''

        print("SCRAPING: URL:              ", url)
        print("SCRAPING: TITLE:            ", vocabulary['title'])
        print("SCRAPING: Parts Of Speech:  ", vocabulary['part_of_speech'])
        print("SCRAPING: US_PRONUNCIATION: ", vocabulary['us_pronunciation'])
        print("SCRAPING: UK_RONUNCIATION:  ", vocabulary['uk_pronunciation'])
        print("SCRAPING: DEFINITION:       ", vocabulary['definition'])
        print("SCRAPING: EXAMPLE SENTENCE: ", vocabulary['example_sentence'], "\n\n\n")
        
        return vocabulary

class Cambridge(Scraping):

    def __init__(self):
        self.headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        # Set up elements for each columns
        self.title = '.di-title .dhw'
        self.parts_of_speech = '.pos'
        self.us_pronunciation = '.us > .pron > .ipa'
        self.uk_pronunciation = '.uk > .pron > .ipa'
        self.definition = '.ddef_h > .def'
        self.example = '.ddef_b > .examp > .eg'
