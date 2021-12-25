import os

from dotenv import load_dotenv

def set_up() ->dict:
    '''Set up env dict'''

    config = {}
    
    load_dotenv()
    config['JSONF'] = os.getenv('JSONF')
    config['JSONF_DIR'] = './src/'
    config['SPREAD_SHEET_KEY'] = os.getenv('SPREAD_SHEET_KEY')
    config['SPREAD_SHEET_NAME'] = os.getenv('SHEET_NAME')
    config['BOOKMARK_NAME'] = os.getenv('BOOKMARK_NAME')
    config['COLUMNS'] = ['title', 
                'part_of_speech', 
                'us_pronunciation', 
                'uk_pronunciation', 
                'definition', 
                'example_sentence', 
                'timestamp', 
                'check']
    config['SLEEP_TIME'] = float(os.getenv('SLEEP_TIME'))

    return config