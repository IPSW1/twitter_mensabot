import requests
import csv
import datetime


def get_date(dt):
    return dt.strftime("%d.%m.%Y")

def get_week(dt):
    return datetime.date(dt.year, dt.month, dt.day).isocalendar()[1]

# get current date and week number
now = datetime.datetime.now()
date = get_date(now)
week = get_week(now)

# menu is saved as "[week number].csv"
url = "https://www.stwno.de/infomax/daten-extern/csv/UNI-P/{}.csv".format(week)
response = requests.get(url)
menu = response.content.decode('utf-8', 'ignore') # FIXME: don't ignore umlauts


menureader = csv.reader(menu.splitlines(), delimiter=';')
meals = []
for row in menureader:
   if(row[0] == date):
        print(row)