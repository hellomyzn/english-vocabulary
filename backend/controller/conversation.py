# import scraping as scraping
import config_ as my_config

"""Controller for speaking with robot"""
from models import bot



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
    input_bot.say_result()
  
    quit()

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