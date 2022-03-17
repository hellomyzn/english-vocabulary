from interfaces import scraping

from models.vocabulary import Vocabulary

class Weblio(scraping.Scraping):

    def __init__(self):
        self.headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        # Set up elements for each columns
        self.title = '.summaryL > h1 > div > span'
        self.parts_of_speech = '.conjugateRowL'
        self.us_pronunciation = '.phoneticEjjeDesc'
        self.uk_pronunciation = '.phoneticEjjeDesc'
        self.definition = '.content-explanation'
        self.example_en = '.KejjeYrEn'
        self.example_jp = '.KejjeYrJp'
        self.url_for_search = 'https://ejje.weblio.jp/content/'


    def get_vocabulary(self, vocabulary: Vocabulary, soup) -> Vocabulary:
        # Get data via scraping
        print(vocabulary)
        vocabulary.title                = soup.select(self.title,            limit=1)[0].text if soup.select(self.title, limit=1) else self.substitution_title
        vocabulary.part_of_speech       = soup.select(self.parts_of_speech,  limit=1)[0].text if soup.select(self.parts_of_speech, limit=1) else ''
        vocabulary.us_pronunciation     = soup.select(self.us_pronunciation,        )[0].text if soup.select(self.us_pronunciation, limit=1) else ''
        vocabulary.uk_pronunciation     = soup.select(self.uk_pronunciation,        )[1].text if soup.select(self.uk_pronunciation, limit=1) else ''
        vocabulary.definition           = soup.select(self.definition,       limit=1)[0].text if soup.select(self.definition, limit=1) else ''
        vocabulary.example_sentence_en  = soup.select(self.example_en,          limit=1)[0].text if soup.select(self.example_en, limit=1) else ''
        vocabulary.example_sentence_jp  = soup.select(self.example_jp,          limit=1)[0].text if soup.select(self.example_jp, limit=1) else ''
        vocabulary.example_sentence = vocabulary.example_sentence_en + ': ' + vocabulary.example_sentence_jp

        # Remove unnecessary blank
        vocabulary.definition = vocabulary.definition.lstrip()

        return vocabulary