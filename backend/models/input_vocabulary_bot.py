from interfaces.bot import Bot
from models.vocabulary import Vocabulary
from models.from_cambridge import FromCambridge
from models.from_bookmarks import FromBookmarks
from models.from_text import FromText
from models.result import Result
from models.google_spreadsheet import GoogleSpreadSheet
from models.own_example_sentence import OwnExampleSentence
from models.csv import CSV
from views import console
import helper



class InputVocabularyBot(Bot):
    def __init__(self, config: dict, speak_color='green'):
        super().__init__(speak_color)
        self.config = config
        self.bookmarks_file_path = config['FILES']['DIR'] + config['FILES']['BOOKMARKS_FILE_NAME'] 
        self.examples_file_path = config['FILES']['DIR'] + config['FILES']['EXAMPLES_FILE_NAME'] 
        self.csv_file_path = config['FILES']['DIR'] + config['FILES']['CSV_FILE_NAME'] 
        self.is_google_spreadsheet = False
        self.is_csv = False
        self.google_spreadsheet = None
        self.csv = None
        self.vocabulary = None
        self.scraping = None
        self.url = None
        self.own_examples = None
        self.result = None


    def check_files(self):
        ''' '''
        # Check whether existing a Bookmarks or no. if it doesn't exist, it goes to show how to copy the Bookmarks file until execution
        if helper.is_file(self.bookmarks_file_path):
            template = console.get_template('confirm_to_update_bookmarks.txt', self.speak_color)
            input(template.substitute({
                'USER': '$USER',
                'bookmarks_file_path': self.bookmarks_file_path
                }))
        else:
            while True:
                template = console.get_template('copy_bookmarks.txt', self.speak_color)
                is_quit = input(template.substitute({
                    'USER': '$USER',
                    'bookmarks_file_path': self.bookmarks_file_path
                    }))
                    
                if helper.is_file(self.bookmarks_file_path):
                    break
                if is_quit == 'quit':
                    quit()
        
        # Check whether existing an example and a csv file or no. if it doesn't exist, those files are going to be created
        for file_path in [self.examples_file_path, self.csv_file_path]:
            if not helper.is_file(file_path):
                helper.create_file(file_path)
                template = console.get_template('create_file.txt', self.speak_color)
                print(template.substitute({
                    'file_path': file_path,
                    'dir': self.config['FILES']['DIR']
                }))

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
                
                # Retrieve Examples
                self.own_examples = OwnExampleSentence(self.examples_file_path)
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
        
        self.vocabulary = Vocabulary()
        self.scraping = FromCambridge()
        self.result = Result()

        return None


    def get_urls(self):
        ''' '''
        # self.url = FromBookmarks(self.bookmarks_file_path, self.config['BOOKMARKS']['FOLDER_NAME'])
        self.url = FromText(self.examples_file_path, self.own_examples.titles, self.scraping.cambridge_url)
        urls_num = len(self.url.urls)

        template = console.get_template('how_many_urls.txt', self.speak_color)
        print(template.substitute({'urls': urls_num}))

        return None


    def write_vocabularies(self):
        ''' '''
        for url in self.url.urls:
            # Get vocabulary from URL through scraping
            self.vocabulary = self.scraping.get_vocabulary(url, self.vocabulary)
            # Add result of vocabulary scraped
            self.result.vocabularies_scraped.append(self.vocabulary.title)

            # Get examples if it is matched by title
            for example in self.own_examples.dict_of_examples:
                if example['title'] == self.vocabulary.title:
                    self.vocabulary.example_sentence = example['example_sentence']
                    self.vocabulary.is_own_example = True
                    continue

            # Logic of writing on Goolge Spreadsheet
            if self.is_google_spreadsheet == True:
                # Check whether existing the vocabulary on Google Spreadsheet or no
                if self.vocabulary.title in self.google_spreadsheet.current_vocabularies:
                    # Add result of vocabularies and examples not written. and then proceed next url afterwards
                    self.result.vocabularies_not_written.append(self.vocabulary.title)
                    self.result.examples_not_written.append(self.vocabulary.title)
                    continue

                # Write vocabulary on Google Spreadsheet    
                self.google_spreadsheet.write(self.vocabulary)
                # Add result of vocabularies written
                self.result.vocabularies_written.append(self.vocabulary.title)
                
                # Add result of examples written or not written
                if self.vocabulary.is_own_example == True:
                    self.result.examples_written.append(self.vocabulary.title)
                else:
                    self.result.examples_not_written.append(self.vocabulary.title)
                
            # Logic of writing on CSV                
            if self.is_csv == True:
                self.csv.write(self.vocabulary, self.csv_file_path)

        return None


    def show_result(self):
        template = console.get_template('show_result.txt', self.speak_color)
        print(template.substitute({ 'num_urls':     len(self.url.urls),
                                    'num_scraping': len(self.result.vocabularies_scraped),

                                    'num_voc_written':     len(self.result.vocabularies_written),
                                    'num_voc_not_written': len(self.result.vocabularies_not_written),
                                    'num_ex_written':      len(self.result.examples_written),
                                    'num_ex_not_written':  len(self.result.examples_not_written),

                                    'voc_written':      self.result.vocabularies_written,
                                    'voc_not_written':  self.result.vocabularies_not_written,
                                    'ex_written':       self.result.examples_written,
                                    'ex_not_written':   self.result.examples_not_written}))
    

    def ask_to_delete(self):
        file_paths = [
            self.bookmarks_file_path, 
            self.examples_file_path, 
            self.csv_file_path]

        for file_path in file_paths:
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