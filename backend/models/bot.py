"""Defined a robot model """
# from roboter.models import ranking
import config_ as config_
from views import console
from models.url import UrlModel
from models import scraping
from models import vocabulary as voc
import helper

class Bot(object):
    """Base model for Robot."""

    def __init__(self, config: dict, speak_color='green'):
        self.speak_color = speak_color
        self.is_GSS = False
        self.is_CSV = False
        self.GSS = None
        self.config = config_.set_up()
        self.urls = []
        self.result = {'scraping': [],
                        'voc_written': [],
                        'voc_not_written': [],
                        'ex_written': [],
                        'ex_not_written': []}

    def hello(self):
        """Returns words to the user that the robot speaks at the beginning."""
        while True:
            template = console.get_template('hello.txt', self.speak_color)
            print(template.substitute())
            break


class InputVocabularyBot(Bot):
    """Handle data model on restaurant."""
    def confirm_to_updates(self):
        template = console.get_template('confirm_to_update.txt', self.speak_color)
        input(template.substitute({'USER': '$USER'}))
    
    def ask_user_favorites(self):
        while True:
            template = console.get_template('ask_gss.txt', self.speak_color)
            is_yes = input(template.substitute()) 
            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                self.is_GSS = True
                self.GSS = voc.GoogleSpreadSheet(self.config['SPREAD_SHEET_KEY'], 
                            self.config['SPREAD_SHEET_NAME'],
                            self.config['COLUMNS'],
                            self.config['SLEEP_TIME'])
                break
            elif is_yes.lower() == 'n' or is_yes.lower() == 'no':
                break

        while True:
            template = console.get_template('ask_csv.txt', self.speak_color)
            is_yes = input(template.substitute()) 
            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                self.is_CSV = True
                break
            elif is_yes.lower() == 'n' or is_yes.lower() == 'no':
                break
        
        if self.is_GSS == False and self.is_CSV == False:
            print("goodbye")
            quit()
        return None

    def get_urls(self):
        self.urls = UrlModel.from_bookmarks(self.config['BOOKMARK_NAME'])
        urls_num = len(self.urls)

        template = console.get_template('how_many_urls.txt', self.speak_color)
        print(template.substitute({'urls': urls_num}))

        return None

    
    def write_vocabularies(self):
        cambridge = scraping.Cambridge()

        for url in self.urls:
            # Get vocabulary from URL
            vocabulary = cambridge.scraping(url)
            self.result['scraping'].append(vocabulary['title'])
        
            if self.is_GSS == True:
                self.GSS.write(vocabulary)

        return None

    def check_files(self):

        if helper.is_file(self.config['PATH_BOOKMARKS'] + self.config['FILE_BOOKMARKS']):
            template = console.get_template('confirm_to_update_bookmarks.txt', self.speak_color)
            input(template.substitute({'USER': '$USER'}))
        else:
            while True:
                template = console.get_template('copy_bookmarks.txt', self.speak_color)
                i = input(template.substitute({'USER': '$USER'}))
                if helper.is_file(self.config['PATH_BOOKMARKS'] + self.config['FILE_BOOKMARKS']):
                    break
                if i == 'quit':
                    quit()
                  
        if helper.is_file(self.config['PATH_EX'] + self.config['FILE_EX']):
            print("There is example file")
        else:
            print("There is no example file")
            helper.create_file(self.config['PATH_EX'] + self.config['FILE_EX'])

        if helper.is_file(self.config['PATH_CSV'] + self.config['FILE_CSV']):
            print("There is example file")
        else:
            print("There is no example file")
            helper.create_file(self.config['PATH_CSV'] + self.config['FILE_CSV'])



    # def __init__(self, name=DEFAULT_ROBOT_NAME):
    #     super().__init__(name=name)
    #     self.ranking_model = ranking.RankingModel()

    # def _hello_decorator(func):
    #     """Decorator to say a greeting if you are not greeting the user."""
    #     def wrapper(self):
    #         if not self.user_name:
    #             self.hello()
    #         return func(self)
    #     return wrapper

    # @_hello_decorator
    # def recommend_restaurant(self):
    #     """Show restaurant recommended restaurant to the user."""
    #     new_recommend_restaurant = self.ranking_model.get_most_popular()
    #     if not new_recommend_restaurant:
    #         return None

    #     will_recommend_restaurants = [new_recommend_restaurant]
    #     while True:
    #         template = console.get_template('greeting.txt', self.speak_color)
    #         is_yes = input(template.substitute({
    #             'robot_name': self.name,
    #             'user_name': self.user_name,
    #             'restaurant': new_recommend_restaurant
    #         }))

    #         if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
    #             break

    #         if is_yes.lower() == 'n' or is_yes.lower() == 'no':
    #             new_recommend_restaurant = self.ranking_model.get_most_popular(
    #                 not_list=will_recommend_restaurants)
    #             if not new_recommend_restaurant:
    #                 break
    #             will_recommend_restaurants.append(new_recommend_restaurant)

    # @_hello_decorator
    # def ask_user_favorite(self):
    #     """Collect favorite restaurant information from users."""
    #     while True:
    #         template = console.get_template(
    #             'which_restaurant.txt', self.speak_color)
    #         restaurant = input(template.substitute({
    #             'robot_name': self.name,
    #             'user_name': self.user_name,
    #         }))
    #         if restaurant:
    #             self.ranking_model.increment(restaurant)
    #             break

    # @_hello_decorator
    # def thank_you(self):
    #     """Show words of appreciation to users."""
    #     template = console.get_template('good_by.txt', self.speak_color)
    #     print(template.substitute({
    #         'robot_name': self.name,
    #         'user_name': self.user_name,
    #     }))
