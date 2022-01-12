import json

from views import console


class Bookmarks(object):
    def __init__(self, path, folder_name):
        self.bookmark_path = path
        self.folder_name = folder_name


    @classmethod
    def get_chrome_bookmark_json_data(cls,path) -> dict:
        '''Get the json of user's Chrome bookmark.'''
        with open(path) as f:
            return json.load(f)


    def get_urls_for_scraping(self):
        """
        Get the list of the urls

        Args:
            None

        Returns:
            urls: the list of urls for scraping from user's Google Chrome Bookmarks
        """
        print("[INFO] - Get urls from Google Chrome Bookmarks")
        urls = []

        bookmark_json_data = Bookmarks.get_chrome_bookmark_json_data(self.bookmark_path)
        bookmark_json_data = bookmark_json_data['roots']['bookmark_bar']

        for data in bookmark_json_data['children']:
            if data['type'] == 'folder' and data['name'] == self.folder_name:
                for d in data['children']:
                    urls.append(d['url'])

        return urls

