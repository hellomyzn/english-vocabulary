import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from interfaces.table import Table
from models import vocabulary
import setting

class GoogleSpreadSheet(Table):
    """
        Reference: 
        - https://qiita.com/164kondo/items/eec4d1d8fd7648217935
        - https://www.cdatablog.jp/entry/2019/04/16/191006
    """
    def __init__(self, env):
        self.columns = GoogleSpreadSheet.get_columns()
        self.workbook = GoogleSpreadSheet.get_workbook()

        if env == 'dev':
            sheet_name = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_NAME_FOR_DEV']
        elif env == 'pro':
            sheet_name = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_NAME_FOR_PRO']
        else:
            sheet_name = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_NAME_FOR_PRO']

        self.worksheet = GoogleSpreadSheet.get_worksheet(self.workbook, sheet_name)
        sheet_name = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_NAME_FOR_UNIQUE']
        self.unique_worksheet = GoogleSpreadSheet.get_worksheet(self.workbook, sheet_name)
        print('start to get vocabulary')
        self.current_vocabularies = self.worksheet.col_values(1)
        print('start to get example')
        self.examples = self.worksheet.col_values(6)
        self.next_row = GoogleSpreadSheet.next_available_row(self.worksheet)
        self.sleep_time_sec = 0.7

    @classmethod
    def get_workbook(cls):
        print("[INFO] - Start connecting GSS...")
        json_path = setting.CONFIG['GOOGLE_API']['JSONF_DIR'] + setting.CONFIG['GOOGLE_API']['JSON_FILE']
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        key = setting.CONFIG['GOOGLE_API']['SPREAD_SHEET_KEY']        

        credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        gc = gspread.authorize(credentials)
        workbook = gc.open_by_key(key)

        return workbook

    @classmethod
    def get_worksheet(cls, workbook, sheet_name):
        print(f'[INFO] - Connect to worksheet: {sheet_name}')
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


    def write(self, vocabulary):
        # If the spreadsheet is empty, Add column on header(from (1,1))
        if GoogleSpreadSheet.is_not_columns(self.worksheet):
            GoogleSpreadSheet.create_columns(self.worksheet, self.columns)
            self.next_row += 1

        for i, column in enumerate(self.columns, start=1):
            try:
                self.worksheet.update_cell(self.next_row, i, getattr(vocabulary, column))
                print(f"[WRITING]: {column}:", getattr(vocabulary, column))
                time.sleep(self.sleep_time_sec)
            except gspread.exceptions.APIError:
                print("Oops! You exceeded for quota metric 'Write requests' and limit 'Write requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:856605576640'\nTry it again later on!")
                break

        self.next_row += 1


    def update_memorized(self, vocabulary) -> None:
        # Update memorized col
        cell = self.unique_worksheet.find(vocabulary.title)
        self.unique_worksheet.update_cell(cell.row, 4, False)
        self.unique_worksheet.update_cell(cell.row, 5, False)
        time.sleep(self.sleep_time_sec)
        return None

    def get_vac_and_ex_dicts(self) -> list:
        l = []
        for v, e in zip(self.current_vocabularies, self.examples):
            d = {"voc": v, "ex": e}
            l.append(d)
        return l