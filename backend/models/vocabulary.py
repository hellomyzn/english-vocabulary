import abc
import os
import time
import datetime


import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Vocabulary(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def write(self):
        pass


class GoogleSpreadSheet(Vocabulary):
    def __init__(self, 
                key: str, 
                sheet_name: str, 
                columns: list,
                sleep_time: float):
        self.workbook = GoogleSpreadSheet.connect(key)
        self.worksheet = self.workbook.worksheet(sheet_name)
        self.columns = columns
        self.all_vocabularies = self.worksheet.col_values(1)
        self.date = GoogleSpreadSheet.get_date()
        self.next_row = GoogleSpreadSheet.next_available_row(self.worksheet)
        self.sleep_time = sleep_time
       

    @classmethod
    def connect(cls, key):
        print("Start connecting GSS...")
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('src/' + str(os.getenv('JSONF')), scope)
        gc = gspread.authorize(credentials)
        workbook = gc.open_by_key(key)
        
        return workbook


    @classmethod
    def get_date(cls):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        now = datetime.datetime.now(JST)
        date = now.strftime('%Y/%m/%d') 
        
        return date
    

    @classmethod
    def next_available_row(cls, worksheet) -> int:
        ''' Return the number of available row '''

        str_list = list(filter(None, worksheet.col_values(1)))
        return int(len(str_list)+1)


    @classmethod
    def create_columns(cls, worksheet, columns):
        print('Create header on GSS')
        for i, column in enumerate(columns, start=1):
            worksheet.update_cell(1, i, column)

        return None


    @classmethod
    def is_not_columns(cls, worksheet):
        if worksheet.row_values(1) == []:
            return True
        else:
            return False


    def write(self, vocabulary):
        # If the spreadsheet is empty, Add column on header(from (1,1))
        if GoogleSpreadSheet.is_not_columns(self.worksheet):
            GoogleSpreadSheet.create_columns(self.worksheet, self.columns)
        
        vocabulary['timestamp'] = self.date
        vocabulary['check'] = False

        for i, column in enumerate(self.columns, start=1):
            try:
                self.worksheet.update_cell(self.next_row, i, vocabulary[column])
                print(f"WRITING: {column}:            ", vocabulary[column])
                time.sleep(self.sleep_time)
            except gspread.exceptions.APIError:
                conv.say_something("Oops! You exceeded for quota metric 'Write requests' and limit 'Write requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:856605576640'\nTry it again later on!")
                break
        self.next_row += 1
        

    
    

class CSV(Vocabulary):
    def __init__(self):
        pass

    def write(self):
        print("hoge")