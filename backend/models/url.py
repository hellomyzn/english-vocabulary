import json
import os

from views import console

class UrlModel(object):

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

    @staticmethod
    def from_bookmarks(folder_name: str):
        '''Get the list of the urls '''
        urls = []
        bookmark_data = UrlModel.get_chrome_bookmark_data()
        bookmark_data = bookmark_data['roots']['bookmark_bar']
        print(folder_name)
        for data in bookmark_data['children']:
            if data['type'] == 'folder' and data['name'] == folder_name:
                for d in data['children']:
                    urls.append(d['url'])
                    
        template = console.get_template('no_bookmarks.txt', 'red')
        user_name = input(template.substitute({'USER': '$USER'}))

        return urls
    
    def from_text(self, path: str):
        print("This is not yet done")

