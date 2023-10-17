import json
import gspread
import requests 

from gspread import Client, Spreadsheet, Worksheet
from datetime import datetime
from collections import defaultdict
from datetime import datetime, timedelta


SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1UkXbNoQrl6qGlP8kOC2Tm6d0mmFJFapsmQ2m4qW7sJ8/edit#gid=0"
URL_PRODAZH= "https://statistics-api.wildberries.ru/api/v1/supplier/sales"
URL_POSTAVOK = "https://statistics-api.wildberries.ru/api/v1/supplier/incomes"
URL_SKLAD = "https://statistics-api.wildberries.ru/api/v1/supplier/stocks"
URL_ZAKAZOV = "https://statistics-api.wildberries.ru/api/v1/supplier/orders"
URL_OTCHET = "https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod"

HEADERS = {
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjczMzA1NzliLTY3MjgtNDVhMi05MDBlLTMxMzhlNDAxMzgyZCJ9.1trm4eIfJPxro3ZFncZRXY0ZhNzsXbzXy4H1s5pqDgI',
}

gc = gspread.service_account("service_account.json")
sh = gc.open_by_url(SPREADSHEET_URL)
worksheet = sh.get_worksheet(1)

        
# constants
date_from = '2023-10-01T00:00:00Z'
date_to = '2023-10-10T00:00:00Z'


def get_wildberries_data(date_from, date_to,url,):
    params = {'dateFrom': date_from, 'dateTo': date_to}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get the orders. Status code: {response.status_code}")
        return [] #данные по запросу заказы
#request data
 
prodazh = get_wildberries_data(date_from, date_to,URL_PRODAZH)
postavki = get_wildberries_data(date_from, date_to,URL_POSTAVOK) 
sklad = get_wildberries_data(date_from, date_to,URL_SKLAD)   
zakazi = get_wildberries_data(date_from, date_to,URL_ZAKAZOV)
otchet = get_wildberries_data(date_from, date_to,URL_OTCHET)

def main():
    prodazh = get_wildberries_data(date_from, date_to,URL_PRODAZH)
    postavki = get_wildberries_data(date_from, date_to,URL_POSTAVOK) 
    sklad = get_wildberries_data(date_from, date_to,URL_SKLAD)   
    zakazi = get_wildberries_data(date_from, date_to,URL_ZAKAZOV)
    otchet = get_wildberries_data(date_from, date_to,URL_OTCHET)
    
# def append_data_to_sheet(data_list):
#     # Добавьте новые данные в таблицу
#     for row_data in data_list:
#         worksheet.append_row(row_data)
 
# Определите диапазон для проверки (например, C1:C100)
range_to_check = worksheet.range('C2:L2')

# Найдите первую пустую ячейку в диапазоне
empty_cell = None
for cell in range_to_check:
    if cell.value == "":
        empty_cell = cell
        break

if empty_cell:
    # Получите значение из столбца A для строки пустой ячейки
    value_from_col_A = worksheet.cell(empty_cell.row, 1).value
    
    value_from_col_B = worksheet.cell(empty_cell.row, 2).value
    # Получите значение из строки 1 для столбца пустой ячейки
    value_from_row_1 = worksheet.cell(1, empty_cell.col).value
    
    print(f"Value from column A for the empty cell's row: {value_from_col_A}")
    print(f"Value from column B for the empty cell's row: {value_from_col_B}")
    print(f"Value from row 1 for the empty cell's column: {value_from_row_1}")
else:
    print("No empty cells found in the specified range.")


# print(sklad)
if __name__ == '__main__':
    main() 