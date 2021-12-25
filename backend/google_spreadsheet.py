import time
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


def create_columns(sheet, columns):
    ''' If the spreadsheet is empty, Add column on header(from (1,1))'''

    for i, column in enumerate(columns, start=1):
        sheet.update_cell(1, i, column)
    return 


def check_columns_data(sheet, columns):
    ''''Return list of header data'''

    # If the spreadsheet is empty
    if sheet.row_values(1) == []:
        create_columns(sheet, columns)
    return     


def write_vocabulary_to_google_spreadsheet(sheet, columns: list, vocabulary: dict):
    ''''Write on the spreadsheet'''

    # Set up the date data
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    date = now.strftime('%Y/%m/%d')

    next_row = next_available_row(sheet)
    vocabulary['timestamp'] = date
    vocabulary['check'] = False

    for i, column in enumerate(columns, start=1):
        try:
            sheet.update_cell(next_row, i, vocabulary[column])
            time.sleep(0.5)
        except gspread.exceptions.APIError:
            print("\n###################################################################################################")
            print("Oops! You exceeded for quota metric 'Write requests' and limit 'Write requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:856605576640'")
            print("Try it again later on!")
            print("###################################################################################################\n\n")
            break
    next_row += 1


def write_examples_to_google_spreadsheet(sheet, columns: list, examples: list):
    ''''  '''
    print("\n###################################################################################################")      
    print("Start writing examples on Google Spreadsheet")
    print("###################################################################################################\n\n")

    all_vocabularies_on_GSS = sheet.col_values(1)
    example_column_num = int(columns.index('example_sentence')) + 1
    
    for example in examples:
        title = example['title']

        if title in all_vocabularies_on_GSS:
            row_num = int(all_vocabularies_on_GSS.index(title)) + 1

            print("[", row_num, "]: ", title)

            try:
                sheet.update_cell(row_num, example_column_num, example['example_sentence'])
            except gspread.exceptions.APIError:
                print("\n###################################################################################################")
                print("Oops! You exceeded for quota metric 'Write requests' and limit 'Write requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:856605576640'")
                print("Try it again later on!")
                print("###################################################################################################\n\n")
                break