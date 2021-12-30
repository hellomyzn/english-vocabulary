import json
import os

from interfaces import url
from views import console


class FromBookmarks(url.Url):
    def __init__(self):
        self.urls = []


    @classmethod
    def get_chrome_bookmark_data(cls) -> dict:
        '''Get the json of user's Chrome bookmark.'''

        CHROME_BOOKMARK_PATH = os.getenv('PATH_BOOKMARKS') + os.getenv('FILE_BOOKMARKS')
        while True:
            try:
                with open(CHROME_BOOKMARK_PATH) as f:
                    return json.load(f)
            except FileNotFoundError:
                template = console.get_template('no_bookmarks.txt', 'red')
                user_name = input(template.substitute({'USER': '$USER'}))
                continue


    def get_urls(self, folder_name: str):
        print("Get urls")
        '''Get the list of the urls '''
        
        bookmark_data = FromBookmarks.get_chrome_bookmark_data()
        bookmark_data = bookmark_data['roots']['bookmark_bar']
        for data in bookmark_data['children']:
            if data['type'] == 'folder' and data['name'] == folder_name:
                for d in data['children']:
                    self.urls.append(d['url'])

        return self.urls

