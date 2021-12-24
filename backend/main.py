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

    print("\n###################################################################################################")
    print("Please run this command below.")
    print("$ cp /Users/$USER/Library/Application\ Support/Google/Chrome/Default/Bookmarks ./backend/data/Bookmarks")
    input('\nIf you finish, Press enter to continue.')
    print("###################################################################################################\n\n")

    urls = scraping.get_urls()
    vocabularies = []

    # Get URL list
    for url in urls:
        print("URL:              ", url)

        vocabularies.append(scraping.get_data_from_cambridge(url))
    
    # Write vocabularies on google spreadsheet
    sheet = gs.connect_gspread(JSONF_DIR + JSONF, SPREAD_SHEET_KEY, SPREAD_SHEET_NAME)
    columns = gs.get_columns_data(sheet)
    gs.write_vocabulary_to_google_spreadsheet(sheet, columns, vocabularies)

    # # Write vocabularies on CSV
    csv_.write_csv(vocabularies)
    print("\n###################################################################################################")
    print("1. Run this command below if you want to check the vocabulary table on CSV")
    print("     $ open ./backend/data/vocabularies.csv\n")
    print("2. Open the following link to remove some bookmark links you already wrote on GSS")
    print("     chrome://bookmarks/\n")
    i = input("3. Is it okay to delete 'data/Bookmarks' file? (y/n): ")
    os.remove('./data/Bookmarks') if i == 'y' else print('Bookmarks file has remained')
    print("done.")
    print("###################################################################################################\n\n")


if __name__ == "__main__":
    main()