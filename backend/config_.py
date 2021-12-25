import os

from dotenv import load_dotenv

def set_up() ->dict:
    '''Set up env dict'''

    config = {}
    
    load_dotenv()
    config['JSONF'] = os.getenv('JSONF')
    config['JSONF_DIR'] = './src/'
    config['SPREAD_SHEET_KEY'] = os.getenv('SPREAD_SHEET_KEY')
    config['SPREAD_SHEET_NAME'] = 'Vocabulary11'
    config['COLUMNS'] = ['title', 
                'part_of_speech', 
                'us_pronunciation', 
                'uk_pronunciation', 
                'definition', 
                'example_sentence', 
                'timestamp', 
                'check']

    return config