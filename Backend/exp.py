from datetime import datetime, date, timedelta
#from .stock import Stock
import requests
from yahoo_fin.stock_info import get_analysts_info, get_quote_data, get_data


AVkey = "P59UFB8DUY2WFYM8"

iexUrl = "https://sandbox.iexapis.com"
iexToken = "token=pk_ce69492f2f3e455da56b46591ea016cc"
iexTest = "token=Tpk_ae7222c303f4491caaa28b28a7e76f8c"

def watch_list_summary():

    watch_list_stocks = ['IBM', 'TSLA', 'AAPL']

    stock_info_list = []

    
    for stock_code in watch_list_stocks:
        #stock = Stock(stock_code[0])
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock_code + '&interval=1min&apikey=' + AVkey
        r = requests.get(url)
        data = r.json()


        print(data)

        stock_dict = {
            'name' : data["Meta Data"]["Symbol"],
            'code' : stock_code
            #'change' : 
        }
        stock_info_list.append(stock_dict)
    
    return stock_info_list

def info():
    watch_list_stocks = ['IBM']
    for stock_code in watch_list_stocks:
        url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + stock_code + '&interval=1min&apikey=' + AVkey
        r = requests.get(url)
        data = r.json()
        print(data)

def iex():
    url = iexUrl + "/stable/tops?" + iexTest + "&symbols=aapl"
    url = iexUrl + '/stable/stock/WES/quote?' + iexTest
    print(url)

    r = requests.get(url)
    data = r.json()
    print(data)


def yahoofin():
    ticker = get_quote_data('nflx')
    print(ticker)


def hisData():
    from1999 = get_data('msft' , start_date = '10/20/2021', end_date = "11/03/2021" , interval = "1d")
    #get_data(ticker, start_date = None, end_date = None, index_as_date = True, interval = “1d”)
    print(from1999)

def datet():
    tod = date.today()
    for x in range(1,7):
        d = timedelta(days = x)
        date = tod - d
        dateformat = datetime.strptime(str(date), '%Y-%m-%d').strftime('%m/%d/%y')
        print(b)

    

#print(watch_list_summary())
#info()
#iex()
#yahoofin()
#hisData()
datet()

