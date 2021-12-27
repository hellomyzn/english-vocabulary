import scraping as scraping
import google_spreadsheet as gs
import csv_ as csv_
import text_ as text_
import config_ as config_
import conversation as conv
import helper


def main():

    # Set up env as dict
    config = config_.set_up()
    result = config['RESULT']

    is_GSS = False
    is_CSV = False
    
    # Set up GSS
    sheet = gs.connect_gspread(config['JSONF_DIR'] + config['JSONF'], config['SPREAD_SHEET_KEY'], config['SPREAD_SHEET_NAME'])
    columns = config['COLUMNS']

    # If there is no columns, write header on GSS
    gs.check_columns_data(sheet,columns)

    # Confirm
    if helper.is_file('./data/Bookmarks'):
        conv.check_with_enter("\
■ Please run this command below.\n\
>>> $ cp /Users/$USER/Library/Application\ Support/Google/Chrome/Default/Bookmarks ./backend/data/Bookmarks\n",
"■ Press Enter if you finsh.")

    is_GSS = conv.check_with_yn("■ Do you want to write vocabularies on Google spread sheet? (y/n): ")
    is_CSV = conv.check_with_yn("■ Do you want to write vocabularies on CSV? (y/n): ")
    
    if is_GSS == False and is_CSV == False:
        quit()

    # Get URL list
    scraping.get_urls_from_bookmarks(config['BOOKMARK_NAME'], result['urls'])
    conv.say_something(f"You have {len(result['urls'])} URLs")

    if is_GSS == True:
        # Get all vocabularies on Google Spreadsheet
        all_vocabularies = sheet.col_values(1)
        helper.check_file('./data/examples.txt')

    if is_CSV == True:
        helper.check_file('./data/vocabularies.csv')
        csv_.check_columns(columns)
        
    # Write vocabulary
    for url in result['urls']:

        # Get vocabulary from URL
        vocabulary = scraping.get_data_from_cambridge(url)
        result['scraping'].append(vocabulary['title'])

        if is_GSS == True:
            # Avoid the vocabulary if it exists on Google Spreasheet
            if vocabulary['title'] in all_vocabularies:
                conv.say_something(f"\t■ There is already '{vocabulary['title']}' on the Google Spreadsheet. so it was skiped")
                result['voc_not_written'].append(vocabulary['title'])
                continue

            conv.say_something("\t■ Start writing vocabularies on Google Spreadsheet")
            gs.write_vocabulary_to_google_spreadsheet(sheet, columns, vocabulary, config['SLEEP_TIME'])
            result['voc_written'].append(vocabulary['title'])
        
        if is_CSV == True:
            conv.say_something("\t■ Start writing on CSV")
            csv_.write_csv(columns, vocabulary)

    # Write example on GSS
    if is_GSS == True:
        if text_.is_exist_examples():
            # Get example sentences as list and dict
            examples = text_.get_list_of_example()
    
            # Write those example on GSS
            conv.say_something("■ Start writing examples on Google Spreadsheet")
            gs.write_examples_to_google_spreadsheet(sheet, columns, examples, config['SLEEP_TIME'], result)

  
    conv.say_something(f"\
■ Result:\n\
- URLs: {len(result['urls'])} \n\
- SCRAPING: {len(result['scraping'])} \n\
- GSS: \n\
    - VOCABULARY: \n\
        - WRITTEN: {len(result['voc_written'])} \n\
        {result['voc_written']} \n\n\
        - NOT_WRITTEN: {len(result['voc_not_written'])} \n\
        {result['voc_not_written']} \n\n\
    - EXAMPLE: \n\
        - WRITTEN: {len(result['ex_written'])} \n\
        {result['ex_written']} \n\n\
        - NOT_WRITTEN: {len(result['ex_not_written'])} \n\
        {result['ex_not_written']} ")   


    # Ending
    conv.say_something("\
■ Run this command below if you want to check the vocabulary table on CSV\n\
>>> $ open ./backend/data/vocabularies.csv\n\n\
■ Open the following link to remove some bookmark links you already wrote on GSS\n\
>>> chrome://bookmarks/")
    
    # Ask to delete Bookmarks
    if conv.check_with_yn("■ Is it okay to delete 'data/Bookmarks' file? (y/n): "):
        # Delete Bookmarks
        helper.remove_file('./data/Bookmarks')
        print('>>> Bookmarks file has been deleted')
    else:
        print('>>> Bookmarks file has been remained')

    print('>>>  done.')


if __name__ == "__main__":
    main()


"""
1. Delete example.txt
2. Create exqample.txt
3. Give a time to edit example.txt
"""