import scraping as scraping
import google_spreadsheet as gs
import csv_ as csv_
import text_ as text_
import config_ as config_
import conversation as conv


def main():

    vocabularies = []
    is_GSS = False
    is_CSV = False

    # Set up env as dict
    config = config_.set_up()
    # Set up GSS
    sheet = gs.connect_gspread(config['JSONF_DIR'] + config['JSONF'], config['SPREAD_SHEET_KEY'], config['SPREAD_SHEET_NAME'])
    columns = config['COLUMNS']

    # If there is no columns, write header on GSS
    gs.check_columns_data(sheet,columns)

    # Get URL list
    urls = scraping.get_urls_from_bookmarks()

    # Confirm
    conv.check_with_enter(
        "Please run this command below.\n>>> $ cp /Users/$USER/Library/Application\ Support/Google/Chrome/Default/Bookmarks ./backend/data/Bookmarks",
        "Press Enter if you finsh.")
    conv.say_something(f"You have {len(urls)} URLs")
    is_GSS = conv.check_with_yn("1: Do you want to write those vocabularies on Google spread sheet? (y/n): ")
    is_CSV = conv.check_with_yn("2: Do you want to write those vocabularies on CSV? (y/n): ")
    
    # Get all vocabularies on Google Spreadsheet
    all_vocabularies = sheet.col_values(1)

    for url in urls:
        vocabulary = scraping.get_data_from_cambridge(url)
        
        # Check if it is exist or not on Google Spreasheet
        if vocabulary['title'] in all_vocabularies:
            conv.say_something(f"There is already '{vocabulary['title']}' on the Google Spreadsheet. so it was skiped")
            continue

        if is_GSS == True:
            conv.say_something("Start writing vocabularies on Google Spreadsheet")
            gs.write_vocabulary_to_google_spreadsheet(sheet, columns, vocabulary)
        if is_CSV == True:
            conv.say_something("Start to write on CSV")
            csv_.write_csv(vocabulary)
    quit()
    # - While URL
    #     - Scraping
    #     - GSS
    #     - CSV

    # # Get vocabularies
    # for url in urls:
    #     print("URL:              ", url)
    #     vocabularies.append(scraping.get_data_from_cambridge(url))
    
    # # Write vocabularies on google spreadsheet
    # gs.write_vocabulary_to_google_spreadsheet(sheet, columns, vocabularies)

    # Write vocabularies on CSV
    # csv_.write_csv(vocabularies)

    # # Get example sentences as list and dict
    # examples = text_.get_list_of_example()

    # # Write those example on GSS
    # gs.write_examples_to_google_spreadsheet(sheet, columns, examples)

    print("\n###################################################################################################")
    print("1. Run this command below if you want to check the vocabulary table on CSV")
    print(">>> $ open ./backend/data/vocabularies.csv\n")
    print("2. Open the following link to remove some bookmark links you already wrote on GSS")
    print(">>> chrome://bookmarks/\n")
    i = input("3. Is it okay to delete 'data/Bookmarks' file? (y/n): ")
    os.remove('./data/Bookmarks') if i == 'y' else print('>>> Bookmarks file has remained')
    print(">>> done.")
    print("###################################################################################################\n\n")


if __name__ == "__main__":
    main()