import csv
import json
import requests

import bs4
from dotenv import load_dotenv


def get_chrome_bookmark_data() -> dict:
    '''Get the json of user's Chrome bookmark.'''

    load_dotenv()
    CHROME_BOOKMARK_PATH = ('data/Bookmarks')

    with open(CHROME_BOOKMARK_PATH) as f:
        return json.load(f)


def get_urls() -> list:
    '''Get the list of the urls '''
    
    bookmark_data = get_chrome_bookmark_data()
    bookmark_data = bookmark_data['roots']['bookmark_bar']

    for data in bookmark_data['children']:
        if data['type'] == 'folder' and data['name'] == 'voc':
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
    print(vocabulary['title'])

    vocabulary['parts_of_speechs'] = soup.select(s_parts_of_speech, limit=1)[0].text
    print(vocabulary['parts_of_speechs'])

    vocabulary['us_pronunciation'] = soup.select(s_us_pronunciation, limit=1)[0].text if soup.select(s_us_pronunciation, limit=1) else ''
    print(vocabulary['us_pronunciation'])

    vocabulary['uk_pronunciation'] = soup.select(s_uk_pronunciation, limit=1)[0].text if soup.select(s_uk_pronunciation, limit=1) else ''
    print(vocabulary['uk_pronunciation'])

    vocabulary['definition']       = soup.select(s_definition,       limit=1)[0].text if soup.select(s_definition, limit=1) else ''
    print(vocabulary['definition'])

    vocabulary['example_sentence'] = soup.select(s_example,          limit=1)[0].text if soup.select(s_example, limit=1) else ''
    print(vocabulary['example_sentence'], "\n\n\n")

    return vocabulary


def write_csv(vocabularies: list):
    '''Write vacabularies on CSV(/backend/data/vocabularies.csv)'''

    with open('data/vocabularies.csv', 'w', newline='') as csvfile:
        fieldnames = ['title', 'parts of speach', 'us pronunciation', 'uk pronunciation', 'definition', 'example sentence']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for vocabulary in vocabularies:
            writer.writerow({'title': vocabulary['title'],
                            'parts of speach': vocabulary['parts_of_speechs'],
                            'us pronunciation': vocabulary['us_pronunciation'],
                            'uk pronunciation': vocabulary['uk_pronunciation'],
                            'definition': vocabulary['definition'],
                            'example sentence': vocabulary['example_sentence']})


def main():
    urls = get_urls()
    vocabularies = []
    for url in urls:
        print(url)
        vocabularies.append(get_data_from_cambridge(url))

    write_csv(vocabularies)
    

if __name__ == "__main__":
    main()