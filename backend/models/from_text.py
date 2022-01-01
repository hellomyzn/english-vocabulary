from interfaces.url import Url
from models.own_example_sentence import OwnExampleSentence

class FromText(Url):
    def __init__(self, path, own_examples_titles, scraping_url):
        self.path = path
        self.own_examples_titles = own_examples_titles
        self.scraping_url = scraping_url
        self.urls = FromText.get_urls(own_examples_titles, scraping_url)

    @classmethod
    def get_urls(self, own_examples_titles, scraping_url):
        urls = []
        for title in own_examples_titles:
            url = scraping_url + title
            urls.append(url)
        return urls