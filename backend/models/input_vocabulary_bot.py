from interfaces.bot import Bot
from models.cambridge import Cambridge
from models.bookmarks import Bookmarks
from models.result import Result
from models.google_spreadsheet import GoogleSpreadSheet
from models.own_files import OwnFiles
from models.csv import CSV
from views import console
import helper



class InputVocabularyBot(Bot):
    def __init__(self, config: dict, speak_color='green'):
        super().__init__(speak_color)
        self.config = config
        self.file_path_of_bookmarks                   = config['FILES']['DIR'] + config['FILES']['FILENAME_OF_BOOKMARKS'] 
        self.file_path_of_own_examples                = config['FILES']['DIR'] + config['FILES']['FILENAME_OF_OWN_EXAMPLES'] 
        self.file_path_of_own_definitions             = config['FILES']['DIR'] + config['FILES']['FILENAME_OF_OWN_DEFINITION'] 
        self.file_path_of_csv                         = config['FILES']['DIR'] + config['FILES']['FILENAME_OF_CSV'] 
        self.file_path_of_vocabularies_to_scrape      = config['FILES']['DIR'] + config['FILES']['FILENAME_OF_VOCABULARY_TO_SCRAPE'] 
        self.file_path_of_vocabularies_scraped        = config['FILES']['DIR'] + config['FILES']['RESULT_DIR'] + config['FILES']['FILENAME_OF_VOCABULARY_SCRAPED'] 
        self.file_path_of_vocabularies_not_scraped    = config['FILES']['DIR'] + config['FILES']['RESULT_DIR'] + config['FILES']['FILENAME_OF_VOCABULARY_NOT_SCRAPED'] 
        self.file_path_of_vocabularies_written        = config['FILES']['DIR'] + config['FILES']['RESULT_DIR'] + config['FILES']['FILENAME_OF_VOCABULARY_WRITTEN'] 
        self.file_path_of_vocabularies_existed        = config['FILES']['DIR'] + config['FILES']['RESULT_DIR'] + config['FILES']['FILENAME_OF_VOCABULARY_EXISTED'] 
        self.file_path_of_own_examples_written        = config['FILES']['DIR'] + config['FILES']['RESULT_DIR'] + config['FILES']['FILENAME_OF_OWN_EXAMPLE_WRITTEN'] 
        self.file_path_of_own_examples_not_written    = config['FILES']['DIR'] + config['FILES']['RESULT_DIR'] + config['FILES']['FILENAME_OF_OWN_EXAMPLE_NOT_WRITTEN']
        self.file_path_of_own_definitions_written     = config['FILES']['DIR'] + config['FILES']['RESULT_DIR'] + config['FILES']['FILENAME_OF_OWN_DEFINITION_WRITTEN'] 
        self.file_path_of_own_definitions_not_written = config['FILES']['DIR'] + config['FILES']['RESULT_DIR'] + config['FILES']['FILENAME_OF_OWN_DEFINITION_NOT_WRITTEN'] 
        self.is_google_spreadsheet = False
        self.is_csv = False
        self.google_spreadsheet = None
        self.csv = None
        self.vocabulary = None
        self.scraping = None
        self.own_files = None
        self.result = None
        self.urls = []

    @classmethod
    def check_bookmarks(cls, bookmarks_file_path, speak_color):
        # Check whether existing a Bookmarks or no. if it doesn't exist, it goes to show how to copy the Bookmarks file until execution
        if helper.is_file(bookmarks_file_path):
            template = console.get_template('confirm_to_update_bookmarks.txt', speak_color)
            input(template.substitute({
                'USER': '$USER',
                'bookmarks_file_path': bookmarks_file_path
                }))
        else:
            while True:
                template = console.get_template('copy_bookmarks.txt', speak_color)
                is_quit = input(template.substitute({
                    'USER': '$USER',
                    'bookmarks_file_path': bookmarks_file_path
                    }))
                    
                if helper.is_file(bookmarks_file_path):
                    break
                if is_quit == 'quit':
                    quit()


    def check_files(self):
        ''' '''
        files = [
            self.file_path_of_own_examples,
            self.file_path_of_own_definitions, 
            self.file_path_of_csv,
            self.file_path_of_vocabularies_to_scrape,
            self.file_path_of_vocabularies_scraped,
            self.file_path_of_vocabularies_not_scraped,
            self.file_path_of_vocabularies_written,
            self.file_path_of_vocabularies_existed,
            self.file_path_of_own_examples_written,
            self.file_path_of_own_examples_not_written,
            self.file_path_of_own_definitions_written,
            self.file_path_of_own_definitions_not_written
            ]

        # Check whether existing an example and a csv file or no. if it doesn't exist, those files are going to be created
        for file_path in files:
            if not helper.is_file(file_path):
                helper.create_file(file_path)
                template = console.get_template('create_file.txt', self.speak_color)
                print(template.substitute({
                    'file_path': file_path,
                    'dir': self.config['FILES']['DIR']
                }))

        template = console.get_template('confirm_to_update_files.txt', self.speak_color)
        input(template.substitute({'file_path': self.file_path_of_own_examples}))

        template = console.get_template('confirm_to_update_files.txt', self.speak_color)
        input(template.substitute({'file_path': self.file_path_of_own_definitions}))

        return None


    def ask_user_favorites(self):
        ''' '''
        # Ask you want to write vocabularies on Google Spreadsheet
        while True:
            template = console.get_template('ask_favorite.txt', self.speak_color)
            is_yes = input(template.substitute({
                'favorite': 'to write vocabularies on Google spreadsheet'
                })) 
                
            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                # Set up Google Spreadsheet
                self.is_google_spreadsheet = True
                self.google_spreadsheet = GoogleSpreadSheet(
                            self.config['GOOGLE_API']['JSONF_DIR'], 
                            self.config['GOOGLE_API']['JSON_FILE'], 
                            self.config['GOOGLE_API']['SPREAD_SHEET_KEY'], 
                            self.config['GOOGLE_API']['SPREAD_SHEET_NAME'])
                
                break
            elif is_yes.lower() == 'n' or is_yes.lower() == 'no':
                break
        
        # Ask you want to write vocabularies on CSV
        while True:
            template = console.get_template('ask_favorite.txt', self.speak_color)
            is_yes = input(template.substitute({
                'favorite': 'to write vocabularies on CSV'
                })) 

            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                self.is_csv = True
                self.csv = CSV()
                break
            elif is_yes.lower() == 'n' or is_yes.lower() == 'no':
                break
        
        if self.is_google_spreadsheet == False and self.is_csv == False:
            quit()
        
        # Generate instances
        # Retrieve Examples
        self.own_files = OwnFiles(
            self.file_path_of_own_examples,
            self.file_path_of_own_definitions,
            self.file_path_of_vocabularies_to_scrape)
        self.scraping = Cambridge()
        self.result = Result()

        return None


    def get_urls(self):
        ''' '''

        # Ask which do you prefer to retrieve vocabularies from
        while True:
            template = console.get_template('ask_how_you_get_urls.txt', self.speak_color)
            i = input(template.substitute({
                'path': self.file_path_of_vocabularies_to_scrape
                })) 

            # If Bookmarks
            if i == str(1):
                InputVocabularyBot.check_bookmarks(self.file_path_of_bookmarks, self.speak_color)
                bookmarks = Bookmarks(self.file_path_of_bookmarks, self.config['BOOKMARKS']['FOLDER_NAME'])
                self.urls = bookmarks.get_urls_for_scraping()
                break
            
            # If own_example_.txt
            elif i == str(2):
                self.urls = self.own_files.get_urls_for_scraping(self.scraping.url_for_search)
                break

        urls_num = len(self.urls)

        template = console.get_template('how_many_urls.txt', self.speak_color)
        print(template.substitute({'urls': urls_num}))

        return None


    def write_vocabularies(self):
        ''' 
        Regular Case: You can find vocabulary through scraping with urls and own example sentence from data/examples.txt
            - Vocabulary: written
            - Own Example: written
        CASE1: You can not find own example sentences
            - Vocabulary: written
            - Own Example: not written
        CASE2: You can not find own example sentences
            - Vocabulary: written
            - Own Example: not written
        CASE3: You can not find vocabulary through scraping with urls from text because the vocabulary's title from text doesn't exist in dictioanry web site
            - Vocabulary: not scraped
            - Own Example: not added
        CASE4: The vocabulary already exists on Google Spreadsheet
            - Vocabulary: existed
            - Own Example: not added
        '''
        for url in self.urls:
            # Get vocabulary from URL through scraping
            self.vocabulary = self.scraping.get_vocabulary(url)

            # Get own examples if it is matched by title (CASE1)
            if self.own_files.dict_of_own_examples:
                for example in self.own_files.dict_of_own_examples:
                    if example['title'] == self.vocabulary.title:
                        self.vocabulary.example_sentence = example['sentences']
                        self.vocabulary.is_own_example = True
                        continue
            
            # Get own definitions if it is matched by title (CASE2)
            if self.own_files.dict_of_own_definitions:
                for definition in self.own_files.dict_of_own_definitions:
                    if definition['title'] == self.vocabulary.title:
                        self.vocabulary.definition = definition['sentences']
                        self.vocabulary.is_own_definition = True
                        continue

            # Check whether you could get vocabulary through scraping or no (CASE3)
            if self.vocabulary.definition:
                # Add result of vocabulary scraped
                self.result.vocabularies_scraped.append(self.vocabulary)
            else:
                # Add result of vocabularies not scraped. and then proceed next url afterwards
                self.result.vocabularies_not_scraped.append(self.vocabulary)
                continue

            # Logic of writing on Goolge Spreadsheet
            if self.is_google_spreadsheet == True:

                # Check whether the vocabulary exists on Google Spreadsheet or no (CASE4)
                if self.vocabulary.title in self.google_spreadsheet.current_vocabularies:
                    # Add result of vocabularies not written. and then proceed next url afterwards
                    self.result.vocabularies_existed.append(self.vocabulary)
                    continue

                # Write vocabulary on Google Spreadsheet    
                self.google_spreadsheet.write(self.vocabulary)
                # Add result of vocabularies written
                self.result.vocabularies_written.append(self.vocabulary)
                
                # Add result of examples written or not written (CASE1)
                if self.vocabulary.is_own_example == True:
                    self.result.examples_written.append(self.vocabulary)
                else:
                    self.result.examples_not_written.append(self.vocabulary)

                # Add result of difinitions written or not written (CASE2)
                if self.vocabulary.is_own_example == True: 
                    self.result.difinitions_written.append(self.vocabulary)
                else:
                    self.result.difinitions_not_written.append(self.vocabulary)

            # Logic of writing on CSV                
            if self.is_csv == True:
                self.csv.write(self.vocabulary, self.file_path_of_csv)

        return None


    def show_result(self):
        template = console.get_template('show_result.txt', self.speak_color)
        print(template.substitute({ 'num_urls':     len(self.urls),
                                    'num_scraped':      len([vocabulary.title for vocabulary in self.result.vocabularies_scraped]),
                                    'num_not_scraped':  len([vocabulary.title for vocabulary in self.result.vocabularies_not_scraped]),
                                    
                                    'voc_scraped':     [vocabulary.title for vocabulary in self.result.vocabularies_scraped],
                                    'voc_not_scraped': [vocabulary.title for vocabulary in self.result.vocabularies_not_scraped],

                                    'num_voc_written':       len([vocabulary.title for vocabulary in self.result.vocabularies_written]),
                                    'num_voc_existed':       len([vocabulary.title for vocabulary in self.result.vocabularies_existed]),
                                    'num_ex_written':        len([vocabulary.title for vocabulary in self.result.examples_written]),
                                    'num_ex_not_written':    len([vocabulary.title for vocabulary in self.result.examples_not_written]),
                                    'num_difi_written':      len([vocabulary.title for vocabulary in self.result.difinitions_written]),
                                    'num_difi_not_written':  len([vocabulary.title for vocabulary in self.result.difinitions_not_written]),

                                    'voc_written':        [vocabulary.title for vocabulary in self.result.vocabularies_written],
                                    'voc_existed':        [vocabulary.title for vocabulary in self.result.vocabularies_existed],
                                    'ex_written':         [vocabulary.title for vocabulary in self.result.examples_written],
                                    'ex_not_written':     [vocabulary.title for vocabulary in self.result.examples_not_written],
                                    'difi_written':       [vocabulary.title for vocabulary in self.result.difinitions_written],
                                    'difi_not_written':   [vocabulary.title for vocabulary in self.result.difinitions_not_written]}))
    

    def write_result(self):
        file_path_and_result_dict = [
            {'file_path': self.file_path_of_vocabularies_scraped         ,'result': self.result.vocabularies_scraped},
            {'file_path': self.file_path_of_vocabularies_not_scraped     ,'result': self.result.vocabularies_not_scraped},
            {'file_path': self.file_path_of_vocabularies_written         ,'result': self.result.vocabularies_written},
            {'file_path': self.file_path_of_vocabularies_existed         ,'result': self.result.vocabularies_existed},
            {'file_path': self.file_path_of_own_examples_written        ,'result': self.result.examples_written},
            {'file_path': self.file_path_of_own_examples_not_written    ,'result': self.result.examples_not_written},
            {'file_path': self.file_path_of_own_definitions_written     ,'result': self.result.examples_written},
            {'file_path': self.file_path_of_own_definitions_not_written ,'result': self.result.examples_not_written}]
        
        for file_path_and_result in file_path_and_result_dict:
            self.result.write_files_for_result(file_path_and_result)


    def ask_to_delete(self):
        file_paths = [
            self.file_path_of_bookmarks, 
            self.file_path_of_own_examples,
            self.file_path_of_own_definitions,
            self.file_path_of_csv,
            self.file_path_of_vocabularies_to_scrape]

        for file_path in file_paths:
            if not helper.is_file(file_path):
                continue

            template = console.get_template('ask_to_delete_file.txt', self.speak_color)
            is_yes = input(template.substitute({'path': file_path}))

            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                helper.delete_file(file_path)
                print(file_path, 'has been deleted')


    def ending(self):
        # Ending
        # Policy: we don't touch the origin Bookmarks file directly
        template = console.get_template('ending.txt', self.speak_color)
        print(template.substitute())