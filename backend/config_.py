import os

from dotenv import load_dotenv

def set_up() ->dict:
    '''Set up env dict'''

    config = {}
    load_dotenv()
    # GOOGLE API
    config['JSONF'] = os.getenv('JSONF')
    config['JSONF_DIR'] = './src/'
    config['SPREAD_SHEET_KEY'] = os.getenv('SPREAD_SHEET_KEY')
    config['SPREAD_SHEET_NAME'] = os.getenv('SHEET_NAME')
    
    config['BOOKMARK_NAME'] = os.getenv('BOOKMARK_NAME')
    config['SLEEP_TIME'] = float(os.getenv('SLEEP_TIME'))

    # FILE PATH AND FILE NAME
    config['PATH_EX'] = os.getenv('PATH_EX')
    config['FILE_EX'] = os.getenv('FILE_EX')
    config['PATH_BOOKMARKS'] = os.getenv('PATH_BOOKMARKS')
    config['FILE_BOOKMARKS'] = os.getenv('FILE_BOOKMARKS')
    config['PATH_CSV'] = os.getenv('PATH_CSV')
    config['FILE_CSV'] = os.getenv('FILE_CSV')

    config['COLUMNS'] = [\
        'title', 
        'part_of_speech', 
        'us_pronunciation', 
        'uk_pronunciation', 
        'definition', 
        'example_sentence', 
        'timestamp', 
        'check']

    return config