from interfaces.url import Url

class FromText(Url):
    def __init__(self):
        self.urls = []

    def get_urls(self, folder_name: str):
        print("This is not yet done")