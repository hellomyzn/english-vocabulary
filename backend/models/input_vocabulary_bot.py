from interfaces.bot import Bot
from models.cambridge import Cambridge
from models.bookmarks import Bookmarks
from models.result import Result
from models.google_spreadsheet import GoogleSpreadSheet
from models.own_files import OwnFiles
from models.csv import CSV
from views import console
import helper
import setting



class InputVocabularyBot(Bot):
    def __init__(self, speak_color='green'):
        super().__init__(speak_color)
        self.is_google_spreadsheet = False
        self.google_spreadsheet = None
        self.is_csv = False
        self.csv = None
        self.vocabulary = None
        self.scraping = None
        self.own_files = None
        self.result = None
        self.urls = []

    @classmethod
    def check_bookmarks_exists(cls, bookmarks_file_path, speak_color):
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


    def check_files_exist(self):
        """
        Check whether existing all the files you will use or no. if it doesn't exist, those files are going to be created.
        Get own examples, difinitions, vocabularies which you want to scrape.

        Args:
            None

        Returns:
            None
        """

        file_paths = setting.FILES_TO_BE_CHECKED

        # Check
        for file_path in file_paths:
            if not helper.is_file(file_path):
                helper.create_file(file_path)
                template = console.get_template('create_file.txt', self.speak_color)
                print(template.substitute({
                    'file_path': file_path,
                    'dir': setting.DIR
                }))

        # Show to update own files if you want
        template = console.get_template('confirm_to_update_files.txt', self.speak_color)
        input(template.substitute({'file_path': setting.FILE_PATH_OF_OWN_EXAMPLES}))

        template = console.get_template('confirm_to_update_files.txt', self.speak_color)
        input(template.substitute({'file_path': setting.FILE_PATH_OF_OWN_DEFINITIONS}))

        # Get own examples, definitions, vacabularies to scrape from own files
        self.own_files = OwnFiles(setting.FILE_PATH_OF_OWN_EXAMPLES,
                                  setting.FILE_PATH_OF_OWN_DEFINITIONS,
                                  setting.FILE_PATH_OF_VOCABULARIES_TO_SCRAPE)

        return None


    def ask_output_format(self):
        """
        Ask where you want to write vocabularies

        Args:
            None

        Returns:
            None
        """

        # Ask you want to write vocabularies on Google Spreadsheet unless you input y or n
        while True:
            template = console.get_template('ask_favorite.txt', self.speak_color)
            user_input = input(template.substitute({'favorite': 'to write vocabularies on Google spreadsheet'})) 
                
            if helper.is_yes(user_input):
                # Set up Google Spreadsheet
                self.is_google_spreadsheet = True
                self.google_spreadsheet = GoogleSpreadSheet()
                break
            elif helper.is_no(user_input):
                break
        
        # Ask you want to write vocabularies on CSV unless you input y or n
        while True:
            template = console.get_template('ask_favorite.txt', self.speak_color)
            user_input = input(template.substitute({'favorite': 'to write vocabularies on CSV'})) 

            if helper.is_yes(user_input):
                self.is_csv = True
                self.csv = CSV()
                break
            elif helper.is_no(user_input):
                break
        
        # You don't want to any vocabularies?
        if self.is_google_spreadsheet == False and self.is_csv == False:
            quit()
            
        return None


    def ask_how_you_get_urls(self):
        """
        Ask where you want to write vocabularies

        Args:
            None

        Returns:
            None
        """
        # Create scraping instance
        self.scraping = Cambridge()

        # Ask which do you prefer to retrieve vocabularies from unless you choose
        while True:
            template = console.get_template('ask_how_you_get_urls.txt', self.speak_color)
            choice = input(template.substitute({'path': setting.FILE_PATH_OF_VOCABULARIES_TO_SCRAPE})) 

            # If Bookmarks
            if choice == str(1):
                InputVocabularyBot.check_bookmarks_exists(setting.FILE_PATH_OF_BOOKMARKS, self.speak_color)
                bookmarks = Bookmarks(setting.FILE_PATH_OF_BOOKMARKS, setting.CONFIG['BOOKMARKS']['FOLDER_NAME'])
                self.urls = bookmarks.get_urls_for_scraping()
                break
            
            # If own file (vocabularies_to_scrape.txt)
            elif choice == str(2):
                template = console.get_template('confirm_to_update_files.txt', self.speak_color)
                input(template.substitute({'file_path': setting.FILE_PATH_OF_VOCABULARIES_TO_SCRAPE}))

                self.urls = self.own_files.get_urls_for_scraping(self.scraping.url_for_search)
                break

        # Show how many urls you got
        urls_num = len(self.urls)
        template = console.get_template('how_many_urls.txt', self.speak_color)
        print(template.substitute({'urls': urls_num}))

        return None


    def write_vocabularies(self):
        ''' 
        Regular Case: You can find vocabulary through scraping with urls and own example sentence from data/examples.txt
            - Vocabulary: written
            - Own Example: written
        CASE1: You can not find vocabulary through scraping with urls from text because the vocabulary's title from text doesn't exist in dictioanry web site
            - Vocabulary: not scraped
            - Own Example: not added
        CASE2: You can not find own example sentences
            - Vocabulary: written
            - Own Example: not written
        CASE3: You can not find own difinition sentences
            - Vocabulary: written
            - Own Example: not written
        CASE4: The vocabulary already exists on Google Spreadsheet
            - Vocabulary: existed
            - Own Example: not added
        '''
        # Create Instance
        self.result = Result()

        for url in self.urls:
            # Get vocabulary from URL through scraping
            self.vocabulary = self.scraping.get_vocabulary(url)

            # Check whether you could get vocabulary through scraping or no (CASE1)
            if self.vocabulary.definition:
                # Add result of vocabulary scraped
                self.result.vocabularies_scraped.append(self.vocabulary)
            else:
                # Add result of vocabularies not scraped. and then proceed next url afterwards
                self.result.vocabularies_not_scraped.append(self.vocabulary)
                continue
            
            # There is own example file or not?
            if not self.own_files.own_example_titles:
                # Add result
                self.result.examples_not_written.append(self.vocabulary)
            else:
                # Get own examples if it is matched by title (CASE2)
                if self.vocabulary.title in self.own_files.own_example_titles:
                    # Get index number of the own examples list
                    index_number = int(self.own_files.own_example_titles.index(str(self.vocabulary.title)))
                    # Overwrite own example sentence 
                    self.vocabulary.example_sentence = self.own_files.own_example_sentences[index_number]
                    # Add result
                    self.result.examples_written.append(self.vocabulary)
                else:
                    # Add result
                    self.result.examples_not_written.append(self.vocabulary)

            # There is own difinition file or not?
            if not self.own_files.own_definition_titles:
                # Add result
                self.result.difinitions_not_written.append(self.vocabulary)
            else:                
                # Get own definitions if it is matched by title (CASE3)
                if self.own_files.own_definition_titles and self.vocabulary.title in self.own_files.own_definition_titles:
                    # Get index number of the own difinitions list
                    index_number = int(self.own_files.own_definition_titles.index(str(self.vocabulary.title)))
                    # Overwrite own difinition
                    self.vocabulary.definition = self.own_files.own_definition_sentences[index_number]
                    # Add result
                    self.result.difinitions_written.append(self.vocabulary)
                else:
                    # Add result
                    self.result.difinitions_not_written.append(self.vocabulary)

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

            # Logic of writing on CSV                
            if self.is_csv == True:
                self.csv.write(self.vocabulary, setting.FILE_PATH_OF_CSV)

        return None


    def show_result(self):
        """
        Show the result of vocabularies as a summary like how many vocabularies were written.

        Args:
            None

        Returns:
            None
        """

        result_dict = { 
            'num_urls':              len(self.urls),
            'num_scraped':           len([vocabulary.title for vocabulary in self.result.vocabularies_scraped]),
            'num_not_scraped':       len([vocabulary.title for vocabulary in self.result.vocabularies_not_scraped]),
            
            'voc_scraped':           [vocabulary.title for vocabulary in self.result.vocabularies_scraped],
            'voc_not_scraped':       [vocabulary.title for vocabulary in self.result.vocabularies_not_scraped],

            'num_voc_written':       len([vocabulary.title for vocabulary in self.result.vocabularies_written]),
            'num_voc_existed':       len([vocabulary.title for vocabulary in self.result.vocabularies_existed]),
            'num_ex_written':        len([vocabulary.title for vocabulary in self.result.examples_written]),
            'num_ex_not_written':    len([vocabulary.title for vocabulary in self.result.examples_not_written]),
            'num_difi_written':      len([vocabulary.title for vocabulary in self.result.difinitions_written]),
            'num_difi_not_written':  len([vocabulary.title for vocabulary in self.result.difinitions_not_written]),

            'voc_written':           [vocabulary.title for vocabulary in self.result.vocabularies_written],
            'voc_existed':           [vocabulary.title for vocabulary in self.result.vocabularies_existed],
            'ex_written':            [vocabulary.title for vocabulary in self.result.examples_written],
            'ex_not_written':        [vocabulary.title for vocabulary in self.result.examples_not_written],
            'difi_written':          [vocabulary.title for vocabulary in self.result.difinitions_written],
            'difi_not_written':      [vocabulary.title for vocabulary in self.result.difinitions_not_written]}

        template = console.get_template('show_result.txt', self.speak_color)
        print(template.substitute(result_dict))
    
    # saveのほうが　わかりやすい？
    def write_result(self):
        """
        Write the result of vocabularies on each files you set up
        like the written vocabularies will be written a certain file(vocabularies_written.txt) for log

        Args:
            None

        Returns:
            None
        """

        file_path_and_result_dict = [
            {'file_path': setting.FILE_PATH_OF_VOCABULARIES_SCRAPED         ,'result': self.result.vocabularies_scraped},
            {'file_path': setting.FILE_PATH_OF_VOCABULARIES_NOT_SCRAPED     ,'result': self.result.vocabularies_not_scraped},
            {'file_path': setting.FILE_PATH_OF_VOCABULARIES_WRITTEN         ,'result': self.result.vocabularies_written},
            {'file_path': setting.FILE_PATH_OF_VOCABULARIES_EXISTED         ,'result': self.result.vocabularies_existed},
            {'file_path': setting.FILE_PATH_OF_OWN_EXAMPLES_WRITTEN         ,'result': self.result.examples_written},
            {'file_path': setting.FILE_PATH_OF_OWN_EXAMPLES_NOT_WRITTEN     ,'result': self.result.examples_not_written},
            {'file_path': setting.FILE_PATH_OF_OWN_DEFINITIONS_WRITTEN      ,'result': self.result.examples_written},
            {'file_path': setting.FILE_PATH_OF_OWN_DEFINITIONS_NOT_WRITTEN  ,'result': self.result.examples_not_written}]
        
        for file_path_and_result in file_path_and_result_dict:
            self.result.write_files_for_result(file_path_and_result)


    def ask_to_delete(self):
        """
        Ask whether those files are still necessary or not

        Args:
            None

        Returns:
            None
        """

        file_paths = setting.FILES_TO_BE_DELETE

        for file_path in file_paths:
            if not helper.is_file(file_path):
                continue

            while True:
                template = console.get_template('ask_to_delete_file.txt', self.speak_color)
                user_input = input(template.substitute({'path': file_path}))

                if helper.is_yes(user_input):
                    helper.delete_file(file_path)
                    print(file_path, 'has been deleted')
                    break
                elif helper.is_no(user_input):
                    break


    def ending(self):
        # Ending
        # Policy: we don't touch the origin Bookmarks file directly
        template = console.get_template('ending.txt', self.speak_color)
        print(template.substitute())