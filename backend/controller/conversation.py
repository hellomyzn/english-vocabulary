# import scraping as scraping
import config_ as my_config
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