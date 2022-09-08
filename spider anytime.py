"""
coinmarketcap.com web scraper

Created on Sat May 8 02:43:06 2021
@creator: Jack.M.Liu

Modified on Sept. 2022
@author: Liheng Tan
"""


import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import time
import datetime
import json


def date_to_timestamp(s, e):
    start = str(time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple()))[:-2]
    end = str(time.mktime(datetime.datetime.strptime(e, "%d/%m/%Y").timetuple()) + 86400)[:-2]
    return start, end


def coinmarketcap(start_date, end_date):

    url = 'https://coinmarketcap.com'
    response = rq.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find('script', id="__NEXT_DATA__", type="application/json")

    coins = {}
    coin_data = json.loads(data.contents[0])

    temp = coin_data["props"]["initialState"]

    global false,null,true
    false = ''
    null = ''
    true = ''
    temp = eval(temp)


    listings = temp["cryptocurrency"]['listingLatest']['data']

    for i in listings[1:]:
        coins[str(i[6])] = i[117]   # # you should print listings to get the number of [coin_id , name] = [6 , 117]


    start, end = date_to_timestamp(start_date, end_date)

    percent = 0
    total = len(coins)

    for coin in coins:
        Market_Cap = []
        Open = []
        High = []
        Low = []
        Volume = []
        Close = []
        Date = []
        print(coins[coin])

        print(coins[coin]+" historical data")
        try:

            start_temp = start
            end_temp = str(int(start) + 8640000)
            if int(end_temp) > int(end):
                end_temp = end


            while int(end_temp) <= int(end):

                url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=" + coin + "&convertId=2781&timeStart=" + start_temp + "&timeEnd=" + end_temp
                # url="https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id="+coin+"&convert=USD&time_start="+start+"&time_end="+end
                response = rq.get(url)

                soup = BeautifulSoup(response.text, "html.parser")
                history_data = json.loads(soup.contents[0])
                quotes = history_data["data"]['quotes']

                for quote in quotes:
                    time.sleep(0.01)
                    Market_Cap.append(quote["quote"]["marketCap"])
                    Open.append(quote["quote"]["open"])
                    Date.append(quote["quote"]["timestamp"][:10])
                    High.append(quote["quote"]["high"])
                    Low.append(quote["quote"]["low"])
                    Volume.append(quote["quote"]["volume"])
                    Close.append(quote["quote"]["close"])

                if int(end_temp) == int(end):
                    break

                start_temp = str(int(start_temp) + 8640000)
                end_temp = str(int(end_temp) +8640000)


                if int(end_temp) > int(end):
                    end_temp = end



            df = pd.DataFrame(
                columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap'])  # All Coins' Data

            df['Date'] = Date
            df['Open'] = Open
            df['High'] = High
            df['Low'] = Low
            df['Close'] = Close
            df['Volume'] = Volume
            df['Market Cap'] = Market_Cap

            df.to_csv(coins[coin]+".csv")     #save
        except:
            pass

        percent += 1
        print('\r' + '[Web Scraping]:[%s%s]%.2f%%;' % (
        '█' * int(percent * 20 / total), ' ' * (20 - int(percent * 20 / total)), float(percent / total * 100)), end=''+'\r')

coinmarketcap("01/01/2021", "01/01/2022")    #start_date,end_date = ("dd/mm/yyyy" , "dd/mm/yyyy")