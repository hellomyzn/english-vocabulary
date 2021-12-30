import abc

class Url(object):
    def __init__(self):
        self.urls = []
    
    
    @abc.abstractmethod
    def get_urls(self):
        pass