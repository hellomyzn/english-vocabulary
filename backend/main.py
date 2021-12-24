import os

from dotenv import load_dotenv

import scraping as scraping
import google_spreadsheet as gs
import csv_ as csv_

def main():
    # Set up
    load_dotenv()
    JSONF = os.getenv('JSONF')
    JSONF_DIR = './src/'
    SPREAD_SHEET_KEY = os.getenv('SPREAD_SHEET_KEY')
    SPREAD_SHEET_NAME = 'Vocabulary2'

    urls = scraping.get_urls()
    vocabularies = []

    # Get URL list
    for url in urls:
        print(url)
        vocabularies.append(scraping.get_data_from_cambridge(url))
    
    # Write vocabularies on google spreadsheet
    sheet = gs.connect_gspread(JSONF_DIR + JSONF, SPREAD_SHEET_KEY, SPREAD_SHEET_NAME)
    columns = gs.get_columns_data(sheet)
    try:
    x = int(input("Please enter a number: "))

    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
    gs.write_vocabulary_to_google_spreadsheet(sheet, columns, vocabularies)
    
    # Write vocabularies on CSV
    csv_.write_csv(vocabularies)
    

if __name__ == "__main__":
    main()