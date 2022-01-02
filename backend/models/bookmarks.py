import json

from interfaces.url import Url
from views import console


class Bookmarks(object):
    def __init__(self, path, folder_name):
        self.bookmark_path = path
        self.folder_name = folder_name


    @classmethod
    def get_chrome_bookmark_data(cls,path) -> dict:
        '''Get the json of user's Chrome bookmark.'''
        with open(path) as f:
            return json.load(f)


    def get_urls_for_scraping(self):
        print("Get urls")
        '''Get the list of the urls '''
        
        urls = []

        bookmark_data = Bookmarks.get_chrome_bookmark_data(self.bookmark_path)
        bookmark_data = bookmark_data['roots']['bookmark_bar']

        for data in bookmark_data['children']:
            if data['type'] == 'folder' and data['name'] == self.folder_name:
                for d in data['children']:
                    urls.append(d['url'])

        return urls

