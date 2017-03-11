import requests
import csv
import datetime
import re

def get_date(dt):
    return dt.strftime("%d.%m.%Y")

def get_week(dt):
    return datetime.date(dt.year, dt.month, dt.day).isocalendar()[1]

def print_menu(menu, type):
    for item in menu:
        if item[2].startswith(type):
            print(re.sub(r'\([^)]*\)', '',item[3]))

# get current date and week number
now = datetime.datetime.now()
date = get_date(now)
week = get_week(now)

date = "09.03.2017" # temporary fixed date for testing

# menu is saved as "[week number].csv"
url = "https://www.stwno.de/infomax/daten-extern/csv/UNI-P/{}.csv".format(week)
response = requests.get(url)
menu = response.content.decode('utf-8', 'ignore') # FIXME: don't ignore umlauts


menureader = csv.reader(menu.splitlines(), delimiter=';')
meals = []
for row in menureader:
   if(row[0] == date):
        meals.append([item for item in row])

# soups
print("Suppe:")
print_menu(meals, "S")
print()

# main dish
print("Hauptgerichte:")
print_menu(meals, "HG")
print()

# side dishes
print("Beilagen:")
print_menu(meals, "B")
print()

# desserts
print("Nachspeisen:")
print_menu(meals, "N")