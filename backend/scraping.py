import json
import requests

import bs4

import conversation as conv


def get_chrome_bookmark_data() -> dict:
    '''Get the json of user's Chrome bookmark.'''

    CHROME_BOOKMARK_PATH = ('data/Bookmarks')
    while True:
        try:
            with open(CHROME_BOOKMARK_PATH) as f:
                return json.load(f)
        except FileNotFoundError:
            conv.check_with_quit("There is no Bookmarks on ./data folder. please copy a Bookmark file from Google Chrome Folder using the following command.\n>>> $ cp /Users/$USER/Library/Application\ Support/Google/Chrome/Default/Bookmarks ./backend/data/Bookmarks\nIf you don't want, Enter 'quit'")
            continue


def get_urls_from_bookmarks(bookmark_name: str) -> list:
    '''Get the list of the urls '''
    
    bookmark_data = get_chrome_bookmark_data()
    bookmark_data = bookmark_data['roots']['bookmark_bar']

    for data in bookmark_data['children']:
        if data['type'] == 'folder' and data['name'] == bookmark_name:
            urls = [d['url'] for d in data['children']]
    return urls


def get_data_from_cambridge(url: str) -> dict:
    '''Get vocabulary data from cambridge'''

    # TO AVOID SCRAPING ERROR ON CAMBRIDGE SITE: requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))        
    # REF: https://gammasoft.jp/support/solutions-of-requests-get-failed/
    headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

    html = requests.get(url, headers=headers_dic)
    soup = bs4.BeautifulSoup(html.content, "html.parser")

    # Set class for scraping
    s_title = '.di-title .dhw'
    s_parts_of_speech = '.pos'
    s_us_pronunciation = '.us > .pron > .ipa'
    s_uk_pronunciation = '.uk > .pron > .ipa'
    s_definition = '.ddef_h > .def'
    s_example = '.ddef_b > .examp > .eg'

    # Get data via scraping
    vocabulary = {}
    vocabulary['title']            = soup.select(s_title, limit=1)[0].text
    

    vocabulary['part_of_speech'] = soup.select(s_parts_of_speech, limit=1)[0].text
    vocabulary['us_pronunciation'] = soup.select(s_us_pronunciation, limit=1)[0].text if soup.select(s_us_pronunciation, limit=1) else ''
    vocabulary['uk_pronunciation'] = soup.select(s_uk_pronunciation, limit=1)[0].text if soup.select(s_uk_pronunciation, limit=1) else ''
    vocabulary['definition']       = soup.select(s_definition,       limit=1)[0].text if soup.select(s_definition, limit=1) else ''
    vocabulary['example_sentence'] = soup.select(s_example,          limit=1)[0].text if soup.select(s_example, limit=1) else ''

    print("URL:              ", url)
    print("TITLE:            ", vocabulary['title'])
    print("Parts Of Speech:  ", vocabulary['part_of_speech'])
    print("US_PRONUNCIATION: ", vocabulary['us_pronunciation'])
    print("UK_RONUNCIATION:  ", vocabulary['uk_pronunciation'])
    print("DEFINITION:       ", vocabulary['definition'])
    print("EXAMPLE SENTENCE: ", vocabulary['example_sentence'], "\n\n\n")
    return vocabulary


    