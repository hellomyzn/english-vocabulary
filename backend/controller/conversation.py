"""Controller for speaking with robot"""

from models.input_vocabulary_bot import InputVocabularyBot


def talk_about_input_vocabulary():
    """Function to speak with robot"""


    # Start input vocabulary
    input_bot = InputVocabularyBot()
    input_bot.hello()
    input_bot.check_files()
    input_bot.ask_output_format()
    input_bot.ask_how_you_get_urls()
    input_bot.write_vocabularies()
    input_bot.show_result()
    input_bot.write_result()
    input_bot.ask_to_delete()
    input_bot.ending()