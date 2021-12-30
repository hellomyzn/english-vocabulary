import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from interfaces import table
from models import vocabulary


class GoogleSpreadSheet(table.Table):
    """
        Reference: 
        - https://qiita.com/164kondo/items/eec4d1d8fd7648217935
        - https://www.cdatablog.jp/entry/2019/04/16/191006
    """
    def __init__(self,
                json_dir: str,
                json_file: str,
                key: str, 
                sheet_name: str, 
                columns: list):
        self.json_path = json_dir + json_file
        self.worksheet = GoogleSpreadSheet.connect(self.json_path, key, sheet_name)
        self.columns = columns
        self.all_vocabularies = self.worksheet.col_values(1)
        self.next_row = GoogleSpreadSheet.next_available_row(self.worksheet)
        self.sleep_time = 0.7
       

    @classmethod
    def connect(cls,json_path, key, sheet_name):
        print("Start connecting GSS...")
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        gc = gspread.authorize(credentials)
        workbook = gc.open_by_key(key)
        worksheet = workbook.worksheet(sheet_name)
        
        return worksheet
    

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


    def write(self, vocabulary, result):
        # If the spreadsheet is empty, Add column on header(from (1,1))
        if GoogleSpreadSheet.is_not_columns(self.worksheet):
            GoogleSpreadSheet.create_columns(self.worksheet, self.columns)
            self.next_row += 1

        for i, column in enumerate(self.columns, start=1):
            try:
                self.worksheet.update_cell(self.next_row, i, getattr(vocabulary, column))
                print(f"WRITING: {column}:", getattr(vocabulary, column))
                time.sleep(self.sleep_time)
            except gspread.exceptions.APIError:
                conv.say_something("Oops! You exceeded for quota metric 'Write requests' and limit 'Write requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:856605576640'\nTry it again later on!")
                break

        result['voc_written'].append(vocabulary.title)
        self.next_row += 1