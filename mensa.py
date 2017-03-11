import requests
import csv
import datetime
import re
import tweepy

# twitter api credentials
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# twitter api setup
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twit_api = tweepy.API(auth)


def main():
    # get current date and week number
    now = datetime.datetime.now()
    date = get_date(now)
    week = get_week(now)

    # menu is saved as "[week number].csv"
    url = "https://www.stwno.de/infomax/daten-extern/csv/UNI-P/{}.csv".format(week)
    response = requests.get(url)
    menu = response.content.decode('utf-8', 'ignore') # FIXME: don't ignore umlauts

    # format menu and only use data for current day
    menureader = csv.reader(menu.splitlines(), delimiter=';')
    meals = []
    for row in menureader:
       if(row[0] == date):
            meals.append([item for item in row])

    # only post meals if canteen is open
    if meals != []:
        post = "Speiseplan für heute, den {}\n".format(date)
        post += "(https://stwno.de/de/gastronomie/speiseplan/uni-passau):"
        twit_api.update_status(status=post)

        # soups
        tweet_menu(meals, "S")
        # main dish
        tweet_menu(meals, "HG")
        # side dishes
        tweet_menu(meals, "B")
        # desserts
        tweet_menu(meals, "N")

        post = "-------------------------------\nGuten Appetit!"
        twit_api.update_status(status=post)

    else:
        post = "Heute kein Mensabetrieb"
        twit_api.update_status(status=post)


def get_date(dt):
    return dt.strftime("%d.%m.%Y")


def get_week(dt):
    return datetime.date(dt.year, dt.month, dt.day).isocalendar()[1]


def tweet_menu(menu, meal_type):
    if meal_type == "S":
        tweet_menu_type(menu, meal_type)
    elif meal_type == "HG":
        tweet_menu_type(menu, meal_type)
    elif meal_type == "B":
        tweet_menu_type(menu, meal_type)
    elif meal_type == "N":
        tweet_menu_type(menu, meal_type)


def tweet_menu_type(menu, meal_type):
    index = 1
    for item in menu:
        if item[2].startswith(meal_type):
            post = item[2] +":\n"

            post += re.sub(r'\([^)]*\)', '',item[3])    #filter out extra information in brackets (like additionals)
            post += "\n"
            if item[6] != "0,00":
                post += "{}€".format(item[6])
            else:
                post += "Kein Preis angegeben"
            twit_api.update_status(status=post)
            index += 1


if __name__ == '__main__':
    main()
