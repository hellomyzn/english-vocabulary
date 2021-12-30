# import scraping as scraping
import config_ as my_config

"""Controller for speaking with robot"""
from models import bot



def talk_about_input_vocabulary():
    """Function to speak with robot"""
    # Set up env as dict
    config = my_config.set_up()
    
    input_bot = bot.InputVocabularyBot(config)
    input_bot.hello()
    input_bot.check_files()
    input_bot.ask_user_favorites()
    input_bot.get_urls()
    input_bot.write_vocabularies()
    input_bot.show_result()
    input_bot.ask_to_delete()
    input_bot.ending()