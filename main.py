import time
from pprint import pprint

import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
import requests
from db_script import *
from datetime import date

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'

# ID Google Sheets документа (можно взять из его URL)
SPREADSHEET_ID = '1ZKwobmwXIdr_A1H8zP2EviuVb43Hud2sV7NxAK3v9ow'


def get_data_from_sheet(cred_file, spreadsheet_id):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        cred_file,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    # Чтение файла
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:D51',
        majorDimension='ROWS'
    ).execute()
    return values


def get_dollar_course():
    course = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    return course['Valute']['USD']['Value']


def check_cell_format(row):

    if not all(row):
        return False
    if not row[0].isdigit():
        return False
    if not row[1].isdigit():
        return False
    if not row[2].isdigit():
        return False
    if not (len(row[3].split('.')) == 3 or len(row[3].split('-')) == 3):
        return False
    return True


if __name__ == '__main__':
    while True:
        data = get_data_from_sheet(CREDENTIALS_FILE, SPREADSHEET_ID)
        table = data['values']

        course = get_dollar_course()

        table[0].append('Стоимость в рублях')
        for i in range(1, len(table)):
            if check_cell_format(table[i]):
                order_date = table[i][3].split('.')
                table[i][3] = f'{order_date[2]}-{order_date[1]}-{order_date[0]}'
                rub_cost = int(table[i][2]) * course
                table[i].append(rub_cost)

        db_manage(config, postgres_commands[0])
        db_manage(config, postgres_commands[1])
        for i in range(1, len(table)):
            if check_cell_format(table[i]):
                db_manage(config, postgres_commands[2].format(*table[i]))
        time.sleep(5)





