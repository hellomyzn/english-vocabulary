# import scraping as scraping
import google_spreadsheet as gs
import csv_ as csv_
import text_ as text_
import config_ as my_config
import conversation as conv
import helper

"""Controller for speaking with robot"""
from models import bot
from models import scraping
from models import vocabulary as voc
from models.url import UrlModel



def talk_about_input_vocabulary():
    """Function to speak with robot"""
    # Set up env as dict
    config = my_config.set_up()
    
    # Set up instances
    input_bot = bot.InputVocabularyBot(config)
    input_bot.hello()
    input_bot.check_files()
    input_bot.ask_user_favorites()
    input_bot.get_urls()
    input_bot.write_vocabularies()

    
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