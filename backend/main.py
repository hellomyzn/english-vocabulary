import json
import getpass
import requests
import bs4
from dotenv import load_dotenv



load_dotenv()
CHROME_BOOKMARK_PATH = ('Bookmarks')

def get_chrome_bookmark_data() -> dict:
    '''Get the json of user's Chrome bookmark.'''
    with open(CHROME_BOOKMARK_PATH) as f:
        return json.load(f)


bookmark_data = get_chrome_bookmark_data()
bookmark_bar = bookmark_data['roots']['bookmark_bar']

for entry in bookmark_bar['children']:
    if entry['type'] == 'folder' and entry['name'] == 'voc':
        urls = [d.get('url') for d in entry['children']]
        # print(urls)

# TO AVOID ERROR: requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))        
# REF: https://gammasoft.jp/support/solutions-of-requests-get-failed/

headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

load_url = "https://dictionary.cambridge.org/dictionary/english/make"
html = requests.get(load_url, headers=headers_dic)
soup = bs4.BeautifulSoup(html.content, "html.parser")

# HTML全体を表示する
print(soup)