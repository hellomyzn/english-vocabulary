from interfaces import scraping

class Cambridge(scraping.Scraping):

    def __init__(self):
        self.headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        # Set up elements for each columns
        self.title = '.di-title .dhw'
        self.parts_of_speech = '.pos'
        self.us_pronunciation = '.us > .pron > .ipa'
        self.uk_pronunciation = '.uk > .pron > .ipa'
        self.definition = '.ddef_h > .def'
        self.example = '.ddef_b > .examp > .eg'
        self.url_for_search = 'https://dictionary.cambridge.org/dictionary/english/'
