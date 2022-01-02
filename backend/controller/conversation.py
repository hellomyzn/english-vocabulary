"""Controller for speaking with robot"""
from configparser import ConfigParser

from models.input_vocabulary_bot import InputVocabularyBot


def talk_about_input_vocabulary():
    """Function to speak with robot"""
    # Set up config as dict
    config_file = 'config.ini'
    config = ConfigParser()
    config.read(config_file)

    # Start input vocabulary
    input_bot = InputVocabularyBot(config)
    input_bot.hello()
    input_bot.check_files()
    input_bot.ask_user_favorites()
    input_bot.get_urls()
    input_bot.write_vocabularies()
    input_bot.show_result()
    input_bot.write_result()
    input_bot.ask_to_delete()
    input_bot.ending()