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

    return config