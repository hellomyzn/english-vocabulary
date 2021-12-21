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
    '''Get vocabulary data from cambridge'''

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
    for defi in definitions:
        vocabularies.append(defi.find(class_="hw dhw").text)
        parts_of_speechs.append(defi.find(class_="pos dpos").text)

        # Get the block of details 
        details_of_definitions = [d for d in defi.find_all(class_="def-block ddef_block")]
        meaning = []
        example_sentence = []

        for dod in details_of_definitions:
            print("#############################################################")
            meaning += [d.find(class_="ddef_d").text for d in dod.select(".ddef_h", limit=1)]
            # Get the first example sentence 
            print(dod)
            example_sentence += [d.find(class_='eg').text for d in dod.select(".ddef_b > .examp", limit=1)]
            
        
        meanings.append(meaning)
        example_sentences.append(example_sentence)

    return vocabularies, parts_of_speechs, us_pronunciation, uk_pronunciation, meanings, example_sentences


def write_csv(vocabularies: list, 
                parts_of_speechs: list, 
                us_pronunciation: str, 
                uk_pronunciation: str, 
                meanings: list, 
                example_sentences: list):
    '''Write vacabularies on CSV(/backend/data/vocabularies.csv)'''

    with open('data/vocabularies.csv', 'w', newline='') as csvfile:
        fieldnames = ['vocabulary', 'parts of speach', 'us pronunciation', 'uk pronunciation', 'definition', 'example sentence']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(vocabularies)):
            # Debug1: match number of meanings and number of example
            print('DEBUG1: ', len(meanings[i]), ' : ',  len(example_sentences[i]))
            for j in range(len((meanings[i]))):
                # Debug2: 
                print('DEBUG2: ', 'Meaning: ', meanings[i][j])
                print('DEBUG2: ', 'Example: ', example_sentences[i][j])
                # print(meanings[i][j], ' : ', example_sentences[i][j])
                writer.writerow({'vocabulary': vocabularies[i], 
                                'parts of speach': parts_of_speechs[i], 
                                'us pronunciation': us_pronunciation, 
                                'uk pronunciation': uk_pronunciation, 
                                'definition': meanings[i][j], 
                                'example sentence': example_sentences[i][j]})


def main():
    # urls = get_urls()
    urls = ['https://dictionary.cambridge.org/dictionary/english/make']
    for url in urls:
        print('\n\n#####################################################################################')
        print(url)
        vocabularies, parts_of_speechs, us_pronunciation, uk_pronunciation, meanings, example_sentences = get_data_from_cambridge(url)
        write_csv(vocabularies, parts_of_speechs, us_pronunciation, uk_pronunciation, meanings, example_sentences)

if __name__ == "__main__":
    main()