from interfaces import scraping

class Weblio(scraping.Scraping):

    def __init__(self):
        self.headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        # Set up elements for each columns
        self.title = '.summaryL > h1 > div > span'
        self.parts_of_speech = '.conjugateRowL'
        self.us_pronunciation = '.phoneticEjjeDesc'
        self.uk_pronunciation = '.phoneticEjjeDesc'
        self.definition = '.content-explanation'
        self.example = '.KejjeYrEn'
        self.url_for_search = 'https://ejje.weblio.jp/content/'
