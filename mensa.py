import requests
import csv
import time


def get_date():
    return time.strftime("%d.%m.%Y")

url = "https://www.stwno.de/infomax/daten-extern/csv/UNI-P/10.csv"
response = requests.get(url)
menu = response.content.decode('utf-8', 'ignore') # FIXME: don't ignore umlauts

date = get_date()
menureader = csv.reader(menu.splitlines(), delimiter=';')
for row in menureader:
    if(row[0] == date):
        print(row)