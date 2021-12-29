import json
import requests

import bs4

import conversation as conv

class CambridgeModel(object):
    """Base Cambridge model."""
    def __init__(self, url):

        # TO AVOID SCRAPING ERROR ON CAMBRIDGE SITE: requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))        
        # REF: https://gammasoft.jp/support/solutions-of-requests-get-failed/
        self.headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

        # Set class for scraping
        self.title = '.di-title .dhw'
        self.s_parts_of_speech = '.pos'
        self.s_us_pronunciation = '.us > .pron > .ipa'
        self.s_uk_pronunciation = '.uk > .pron > .ipa'
        self.s_definition = '.ddef_h > .def'
        self.s_example = '.ddef_b > .examp > .eg'

        


class ScrapingModel(CambridgeModel):
    """Definition of class that generates ranking model to write to CSV"""
    def __init__(self, url, *args, **kwargs):
        super().__init__(url, *args, **kwargs)
        self.urls = get_urls_from_bookmarks(url)


#     def get_chrome_bookmark_data(self) -> dict:
#         '''Get the json of user's Chrome bookmark.'''

#         CHROME_BOOKMARK_PATH = ('data/Bookmarks')
#         while True:
#             try:
#                 with open(CHROME_BOOKMARK_PATH) as f:
#                     return json.load(f)
#             except FileNotFoundError:
#                 conv.check_with_quit(\
#     "■ There is no Bookmarks on ./data folder. please copy a Bookmark file from Google Chrome Folder using the following command.\n\
#     >>> $ cp /Users/$USER/Library/Application\ Support/Google/Chrome/Default/Bookmarks ./backend/data/Bookmarks\n\n\
#     ■ Press Enter after copy. If you don't want, Enter 'quit': ")
#                 continue


    def get_urls_from_bookmarks(self, bookmark_name: str):
        '''Get the list of the urls '''
        urls = []
        bookmark_data = get_chrome_bookmark_data()
        bookmark_data = bookmark_data['roots']['bookmark_bar']
        
        for data in bookmark_data['children']:
            if data['type'] == 'folder' and data['name'] == bookmark_name:
                for d in data['children']:
                    urls.append(d['url'])

        conv.say_something(f"You have {len(urls)} URLs")
        return urls


# def get_data_from_cambridge(url: str) -> dict:
#     '''Get vocabulary data from cambridge'''



    #     html = requests.get(url, headers=self.headers_dic)
    # self.soup = bs4.BeautifulSoup(html.content, "html.parser")

#     # Get data via scraping
#     vocabulary = {}
#     vocabulary['title']            = soup.select(s_title, limit=1)[0].text if soup.select(s_title, limit=1) else ''
#     vocabulary['part_of_speech'] = soup.select(s_parts_of_speech, limit=1)[0].text if soup.select(s_parts_of_speech, limit=1) else ''
#     vocabulary['us_pronunciation'] = soup.select(s_us_pronunciation, limit=1)[0].text if soup.select(s_us_pronunciation, limit=1) else ''
#     vocabulary['uk_pronunciation'] = soup.select(s_uk_pronunciation, limit=1)[0].text if soup.select(s_uk_pronunciation, limit=1) else ''
#     vocabulary['definition']       = soup.select(s_definition,       limit=1)[0].text if soup.select(s_definition, limit=1) else ''
#     vocabulary['example_sentence'] = soup.select(s_example,          limit=1)[0].text if soup.select(s_example, limit=1) else ''

#     print("URL:              ", url)
#     print("TITLE:            ", vocabulary['title'])
#     print("Parts Of Speech:  ", vocabulary['part_of_speech'])
#     print("US_PRONUNCIATION: ", vocabulary['us_pronunciation'])
#     print("UK_RONUNCIATION:  ", vocabulary['uk_pronunciation'])
#     print("DEFINITION:       ", vocabulary['definition'])
#     print("EXAMPLE SENTENCE: ", vocabulary['example_sentence'], "\n\n\n")
#     return vocabulary