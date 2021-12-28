import time
import datetime

import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

import conversation as conv

"""
Reference: 
- https://qiita.com/164kondo/items/eec4d1d8fd7648217935
- https://www.cdatablog.jp/entry/2019/04/16/191006

"""


def connect_gspread(jsonf: str, key: str, sheet_name: str):

    conv.say_something("Start connecting GSS...")
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
    conv.say_something("Start creating header on GSS")

    for i, column in enumerate(columns, start=1):
        sheet.update_cell(1, i, column)
    return 


def check_columns_data(sheet, columns):
    ''''Return list of header data'''

    # If the spreadsheet is empty
    if sheet.row_values(1) == []:
        create_columns(sheet, columns)
    return     


def write_vocabulary_to_google_spreadsheet(sheet, columns: list, vocabulary: dict, sleep_time: float):
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
            time.sleep(sleep_time)
        except gspread.exceptions.APIError:
            conv.say_something("Oops! You exceeded for quota metric 'Write requests' and limit 'Write requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:856605576640'\nTry it again later on!")
            break
    next_row += 1


def write_examples_to_google_spreadsheet(sheet, columns: list, examples: list, sleep_time: float, result: dict) ->dict:
    '''  '''

    all_vocabularies_on_GSS = sheet.col_values(1)
    example_column_num = int(columns.index('example_sentence')) + 1

    for example in examples:
        title = example['title']

        if title in all_vocabularies_on_GSS:
            # There is the vocabulary on GSS
            row_num = int(all_vocabularies_on_GSS.index(title)) + 1
            conv.say_something(f"\t[{row_num}]: {title}")

            try:
                # Write the vocabulary on GSS
                sheet.update_cell(row_num, example_column_num, example['example_sentence'])
                result['ex_written'].append(example['title'])
                time.sleep(sleep_time)
            except gspread.exceptions.APIError:
                # If time out
                conv.say_something("Oops! You exceeded for quota metric 'Write requests' and limit 'Write requests per minute per user' of service 'sheets.googleapis.com' for consumer 'project_number:856605576640'\nTry it again later on!")
                break
        else: 
            # There is no the vocabulary on GSS
            result['ex_not_written'].append(example['title'])
