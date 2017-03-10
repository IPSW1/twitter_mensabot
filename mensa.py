import requests
import csv


url = "https://www.stwno.de/infomax/daten-extern/csv/UNI-P/10.csv"
response = requests.get(url)
menu = response.content.decode('utf-8', 'ignore') # FIXME: don't ignore umlauts

menureader = csv.reader(menu.splitlines(), delimiter=';')
for row in menureader:
    print(row)