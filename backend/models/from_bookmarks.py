import json

from interfaces import url
from views import console


class FromBookmarks(url.Url):
    def __init__(self, path, folder_name):
        self.urls = FromBookmarks.get_urls(path, folder_name)
        self.bookmark_path = path
        self.folder_name = folder_name


    @classmethod
    def get_chrome_bookmark_data(cls,path) -> dict:
        '''Get the json of user's Chrome bookmark.'''
        with open(path) as f:
            return json.load(f)


    @classmethod
    def get_urls(self, path, folder_name: str):
        print("Get urls")
        '''Get the list of the urls '''
        
        urls = []

        bookmark_data = FromBookmarks.get_chrome_bookmark_data(path)
        bookmark_data = bookmark_data['roots']['bookmark_bar']
        for data in bookmark_data['children']:
            if data['type'] == 'folder' and data['name'] == folder_name:
                for d in data['children']:
                    urls.append(d['url'])

        return urls

