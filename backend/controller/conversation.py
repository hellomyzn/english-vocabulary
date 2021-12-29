import scraping as scraping
import google_spreadsheet as gs
import csv_ as csv_
import text_ as text_
import config_ as config_
import conversation as conv
import helper

"""Controller for speaking with robot"""
from models import bot



def talk_about_input_vocabulary():
    """Function to speak with robot"""
    input_bot = bot.InputVocabularyBot()
    input_bot.hello()

    quit()
    # Set up env as dict
    config = config_.set_up()
    result = config['RESULT']

    is_GSS = False
    is_CSV = False

    EXAMPLE_PATH = config['PATH_EX'] + config['FILE_EX']
    CSV_PATH = config['PATH_CSV'] + config['FILE_CSV']
    BOOKMARKS_PATH = config['PATH_BOOKMARKS'] + config['FILE_BOOKMARKS']

    # Confirm Bookamrk updates
    if helper.is_file(BOOKMARKS_PATH):
        conv.check_with_enter("\
■ Please run this command below to update your Bookmarks.\n\
>>> $ cp /Users/$USER/Library/Application\ Support/Google/Chrome/Default/Bookmarks ./backend/data/Bookmarks\n")

    # Confirm GSS and CSV
    is_GSS = conv.check_with_yn("■ Do you want to write vocabularies on Google spread sheet? (y/n): ")
    is_CSV = conv.check_with_yn("■ Do you want to write vocabularies on CSV? (y/n): ")
    
    if is_GSS == False and is_CSV == False:
        quit()

    # Get URL list
    result['urls'] = scraping.get_urls_from_bookmarks(config['BOOKMARK_NAME'])

    # Set up for GSS
    if is_GSS == True:
        # Set up GSS
        sheet = gs.connect_gspread(config['JSONF_DIR'] + config['JSONF'], config['SPREAD_SHEET_KEY'], config['SPREAD_SHEET_NAME'])
        columns = config['COLUMNS']

        # If there is no columns, write header on GSS
        gs.check_columns_data(sheet, columns)

        # Get all vocabularies on Google Spreadsheet
        all_vocabularies = sheet.col_values(1)

        # Check examples file
        if not helper.is_file(EXAMPLE_PATH):
            helper.create_file(EXAMPLE_PATH)
        
        conv.check_with_enter(f"■ Please update your {EXAMPLE_PATH} if you need.\n")
    
    # Set up for CSV
    if is_CSV == True:
        if not helper.is_file(CSV_PATH):
            helper.create_file(CSV_PATH)
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
        if text_.is_examples():
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
    # Policy: we don't touch the origin Bookmarks file directly
    conv.say_something("\
■ Run this command below if you want to check the vocabulary table on CSV\n\
>>> $ open ./backend/data/vocabularies.csv\n\n\
■ Open the following link to remove some bookmark links you already wrote on GSS\n\
>>> chrome://bookmarks/")
    
    # Ask to delete Bookmarks
    if conv.check_with_yn(f"■ Is it okay to delete {BOOKMARKS_PATH} file? (y/n): "):
        # Delete Bookmarks
        helper.delete_file(BOOKMARKS_PATH)
        print(f'>>> {BOOKMARKS_PATH} has been deleted')
    else:
        print(f'>>> {BOOKMARKS_PATH} has been remained')

    # Ask to delete Examples
    if conv.check_with_yn(f"■ Is it okay to delete {EXAMPLE_PATH} file? (y/n): "):
        # Delete Bookmarks
        helper.delete_file(EXAMPLE_PATH)
        print(f'>>> {EXAMPLE_PATH} has been deleted')
    else:
        print(f'>>> {EXAMPLE_PATH} has been remained')

    print('>>>  done.')





# def talk_about_vocabulary():
#     """Function to speak with robot"""
#     restaurant_robot = robot.RestaurantRobot()
#     restaurant_robot.hello()
#     restaurant_robot.recommend_restaurant()
#     restaurant_robot.ask_user_favorite()
#     restaurant_robot.thank_you()