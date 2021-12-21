import json
import requests
import bs4
import csv
from dotenv import load_dotenv


def get_chrome_bookmark_data() -> dict:
    '''Get the json of user's Chrome bookmark.'''

    load_dotenv()
    CHROME_BOOKMARK_PATH = ('Bookmarks')

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


def get_data_from_cambridge(url: str):
    '''get vocabulary data from cambridge'''

    # TO AVOID SCRAPING ERROR ON CAMBRIDGE SITE: requests.exceptions.ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))        
    # REF: https://gammasoft.jp/support/solutions-of-requests-get-failed/
    headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

    vocabularies = []
    parts_of_speechs = []
    meanings = []
    example_sentences = []

    html = requests.get(url, headers=headers_dic)
    soup = bs4.BeautifulSoup(html.content, "html.parser")

    # Get data of pronunciation
    us_pronunciation = soup.select('.us > .pron > .ipa', limit=1)[0].text 
    uk_pronunciation = soup.select('.uk > .pron > .ipa', limit=1)[0].text
    

    # Get all difinition
    definitions = [d for d in soup.find_all(class_="pr entry-body__el")]
    for dif in definitions:
        vocabularies.append(dif.find(class_="hw dhw").text)
        parts_of_speechs.append(dif.find(class_="pos dpos").text)
        meanings.append([d.text for d in dif.select(".sense-body > .ddef_block .ddef_d")])
        # Get the first example sentence 
        example_sentences.append([d.find(class_='eg').text for d in dif.select(".sense-body > .ddef_block > .def-body")])

    return vocabularies, parts_of_speechs, us_pronunciation, uk_pronunciation, meanings, example_sentences



# with open('data/voc.csv', 'w', newline='') as csvfile:
#     fieldnames = ['vocabulary', 'parts of speach', 'us pronunciation', 'uk pronunciation', 'definition', 'example sentence']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # writer.writeheader()
    # for i in range(len(titles)):
    #     for j in range(len((definitions[i]))):
    #         writer.writerow({'vocabulary': titles[i], 
    #                     'parts of speach': parts_of_speechs[i], 
    #                     'us pronunciation': us_pronunciation, 
    #                     'uk pronunciation': uk_pronunciation, 
    #                     'definition': definitions[i][j], 
    #                     'example sentence': example_sentences[i][j]})

def main():
    urls = get_urls()
    url = 'https://dictionary.cambridge.org/dictionary/english/need'
    vocabularies, parts_of_speechs, us_pronunciation, uk_pronunciation, meanings, example_sentences = get_data_from_cambridge(url)

if __name__ == "__main__":
    main()