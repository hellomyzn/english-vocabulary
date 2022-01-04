import datetime

class Vocabulary(object):
    def __init__(self):
        self.title = None
        self.parts_of_speech = None
        self.us_pronunciation = None
        self.uk_pronunciation = None
        self.definition = None        
        self.example_sentence = None
        self.timestamp = Vocabulary.get_date()
        self.check = False
        self.is_own_example = False
        self.is_own_definition = False
        

    @classmethod
    def get_date(cls):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)
        date = now.strftime('%Y/%m/%d') 
        
        return date