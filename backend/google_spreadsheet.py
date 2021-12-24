import datetime

import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

"""
Reference: 
- https://qiita.com/164kondo/items/eec4d1d8fd7648217935
- https://www.cdatablog.jp/entry/2019/04/16/191006

"""


def connect_gspread(jsonf: str, key: str, sheet_name: str):

    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    gc = gspread.authorize(credentials)
    workbook = gc.open_by_key(key)
    worksheet = workbook.worksheet(sheet_name)
    
    return worksheet


def next_available_row(sheet) -> int:
    ''' Return the number of available row '''

    str_list = list(filter(None, sheet.col_values(1)))
    return int(len(str_list)+1)


def create_columns(sheet):
    ''' If the spreadsheet is empty, Add column on header(from (1,1))'''

    COLUMN_FORMAT = ['title', 
                'parts_of_speechs', 
                'us_pronunciation', 
                'uk_pronunciation', 
                'definition', 
                'example_sentence', 
                'timestamp', 
                'check']
    for i, cf in enumerate(COLUMN_FORMAT, start=1):
        sheet.update_cell(1, i, cf)


def get_columns_data(sheet):
    ''''Return list of header data'''

    # If the spreadsheet is empty
    if sheet.row_values(1) == []:
        create_columns(sheet)
    
    columns = sheet.row_values(1)
    return columns


def write_vocabulary_to_google_spreadsheet(sheet, columns: list, vocabularies: list):
    ''''Write on the spreadsheet'''

    # Set up the date data
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    date = now.strftime('%Y/%m/%d')

    next_row = next_available_row(sheet)

    for voc in vocabularies:
        voc['timestamp'] = date
        voc['check'] = False

        for j, column in enumerate(columns, start=1):
            sheet.update_cell(next_row, j, voc[column])
        next_row += 1