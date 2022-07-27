from datetime import datetime
import mysql.connector
#from .stock import Stock
import requests
from yahoo_fin.stock_info import 


#       Database connection set up
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database='watchdog'
)
cur = mydb.cursor(buffered=True)

AVkey = "P59UFB8DUY2WFYM8"

iexUrl = "https://sandbox.iexapis.com"
iexToken = "token=pk_ce69492f2f3e455da56b46591ea016cc"
iexTest = "token=Tpk_ae7222c303f4491caaa28b28a7e76f8c"

class Watchlist():

    def add_to_watch_list(user_id, stock_code):

        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id='%s' ", (user_id,))
        mydb.commit()

        try:
            watch_list_id = cur.fetchone()[0]
        except Exception as e:
            watch_list_id = 1
        cur.execute("INSERT INTO watch_list_stocks (watch_list_id, add_date, stock_code) VALUES (%s, %s, %s)", (watch_list_id, str(datetime.now()), stock_code))
        mydb.commit()
        return

    def get_watch_list(user_id, view_id):

        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id='%s' ", (user_id,))
        mydb.commit()
        watch_list_id = cur.fetchone()[0]

        cur.execute("SELECT stock_code FROM watch_list_stocks WHERE watch_list_id='%s' ORDER BY  add_date", (watch_list_id,))
        mydb.commit()
        watch_list_stocks = cur.fetchall()

        stock_info_list = []

        print(watch_list_stocks)
        print(len(watch_list_stocks))

        
        for stock_code in watch_list_stocks:
            #stock = Stock(stock_code[0])
            url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + stock_code[0] + '&apikey=' + AVkey
            url2 = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + stock_code[0] + '&apikey=' + AVkey
            r = requests.get(url)
            r2 = requests.get(url2)
            data = r.json()
            data2 = r2.json()

            print(stock_code)
            print(data2)

            stock_dict = {
                'name' : data2['Name'],
                'code' : stock_code[0],
                'market' : data2['Exchange'],
                'price' : data['Global Quote']['05. price'],
                'open' : data['Global Quote']['02. open'],
                'change' : data['Global Quote']['09. change'],
                'change%' : data['Global Quote']['10. change percent'],
                'high' : data['Global Quote']['03. high'],
                'low' : data['Global Quote']['04. low'],
                'volume' : data['Global Quote']['06. volume'],
                #'market_cap' : stock.market_cap(),
            }
            stock_info_list.append(stock_dict)
        
        return stock_info_list

    def delete_from_watch_list(user_id, stock_code):

        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id='%s' ", (user_id,))
        mydb.commit()
        try:
            watch_list_id = cur.fetchone()[0]
        except Exception as e:
            watch_list_id = 1
        cur.execute("DELETE FROM watch_list_stocks WHERE stock_code=%s AND watch_list_id=%s", (stock_code, watch_list_id))
        mydb.commit()
        return


    def watch_list_summary(user_id):

        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id='%s' ", (user_id,))
        mydb.commit()
        watch_list_id = cur.fetchone()[0]

        cur.execute("SELECT stock_code FROM watch_list_stocks WHERE watch_list_id='%s' ORDER BY  add_date", (watch_list_id,))
        mydb.commit()
        watch_list_stocks = cur.fetchall()

        stock_info_list = []

        
        for stock_code in watch_list_stocks:
            #stock = Stock(stock_code[0])
            url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=' + stock_code[0] + '&apikey=' + AVkey
            url2 = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + stock_code[0] + '&apikey=' + AVkey
            r = requests.get(url)
            r2 = requests.get(url2)
            data = r.json()
            data2 = r2.json()


            stock_dict = {
                'name' : data2['Name'],
                'code' : stock_code[0],
                'change' : data['Global Quote']['09. change']
            }
            stock_info_list.append(stock_dict)
        
        return stock_info_list

    def get_watch_list(user_id, view_id):

        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id='%s' ", (user_id,))
        mydb.commit()
        watch_list_id = cur.fetchone()[0]

        cur.execute("SELECT stock_code FROM watch_list_stocks WHERE watch_list_id='%s' ORDER BY  add_date", (watch_list_id,))
        mydb.commit()
        watch_list_stocks = cur.fetchall()

        stock_info_list = []

        print(watch_list_stocks)
        print(len(watch_list_stocks))

        
        for stock_code in watch_list_stocks:
            #stock = Stock(stock_code[0])
            url = iexUrl + '/stable/stock/' + stock_code[0] + '/quote?' + iexTest
            r = requests.get(url)
            data = r.json()

            print(stock_code[0])
            print(data)

            stock_dict = {
                'name' : data['companyName'],
                'code' : stock_code[0],
                'market' : data['primaryExchange'],
                'price' : data['latestPrice'],
                'open' : data['open'],
                'change' : data['change'],
                'change%' : data['changePercent'],
                'high' : data['high'],
                'low' : data['low'],
                'volume' : data['latestVolume'],
                #'market_cap' : stock.market_cap(),
            }
            stock_info_list.append(stock_dict)
        
        return stock_info_list

'''
{'Meta Data': {'1. Information': 'Intraday (5min) open, high, low, close prices and volume', '2. Symbol': 'IBM', '3. Last Refreshed': '2021-10-22 20:00:00', '4. Interval': '5min', '5. Output Size': 'Compact', '6. Time Zone': 'US/Eastern'}, 'Time Series (5min)': {'2021-10-22 20:00:00': {'1. open': '127.8500', '2. high': '127.8500', '3. low': '127.8500', '4. close': '127.8500', '5. volume': '1327'}, '2021-10-22 19:55:00': {'1. open': '127.8200', '2. high': '127.8500', '3. low': '127.8200', '4. close': '127.8500', '5. volume': '2223'}, '2021-10-22 19:50:00': {'1. open': '127.7600', '2. high': '127.7600', '3. low': '127.7600', '4. close': '127.7600', '5. volume': '559'}, '2021-10-22 19:40:00': {'1. open': '127.8000', '2. high': '127.8000', '3. low': '127.8000', '4. close': '127.8000', '5. volume': '493'}, '2021-10-22 19:35:00': {'1. open': '127.8000', '2. high': '127.8000', '3. low': '127.8000', '4. close': '127.8000', '5. volume': '201'}, '2021-10-22 19:25:00': {'1. open': '127.7500', '2. high': '127.7500', '3. low': '127.7500', '4. close': '127.7500', '5. volume': '655'}, '2021-10-22 19:20:00': {'1. open': '127.8000', '2. high': '127.8000', '3. low': '127.8000', '4. close': '127.8000', '5. volume': '600'}, '2021-10-22 19:05:00': {'1. open': '127.7500', '2. high': '127.7500', '3. low': '127.7500', '4. close': '127.7500', '5. volume': '215'}, '2021-10-22 18:55:00': {'1. open': '127.8000', '2. high': '127.8000', '3. low': '127.7500', '4. close': '127.7500', '5. volume': '532'}, '2021-10-22 18:50:00': {'1. open': '127.7900', '2. high': '127.7900', '3. low': '127.7800', '4. close': '127.7800', '5. volume': '302'}, '2021-10-22 18:45:00': {'1. open': '127.8200', '2. high': '127.8800', '3. low': '127.8200', '4. close': '127.8800', '5. volume': '2752'}, '2021-10-22 18:35:00': {'1. open': '127.7900', '2. high': '127.7900', '3. low': '127.7801', '4. close': '127.7801', '5. volume': '499'}, '2021-10-22 18:30:00': {'1. open': '127.8000', '2. high': '127.8000', '3. low': '127.8000', '4. close': '127.8000', '5. volume': '471'}, '2021-10-22 18:25:00': {'1. open': '127.8000', '2. high': '127.8000', '3. low': '127.8000', '4. close': '127.8000', '5. volume': '140'}, '2021-10-22 18:20:00': {'1. open': '127.8000', '2. high': '127.8000', '3. low': '127.7500', '4. close': '127.7500', '5. volume': '1097'}, '2021-10-22 18:15:00': {'1. open': '127.8000', '2. high': '127.8000', '3. low': '127.8000', '4. close': '127.8000', '5. volume': '200'}, '2021-10-22 18:10:00': {'1. open': '127.8000', '2. high': '127.8000', '3. low': '127.8000', '4. close': '127.8000', '5. volume': '263'}, '2021-10-22 17:45:00': {'1. open': '127.8800', '2. high': '127.8800', '3. low': '127.8800', '4. close': '127.8800', '5. volume': '116'}, '2021-10-22 17:40:00': {'1. open': '127.7100', '2. high': '127.8000', '3. low': '127.7100', '4. close': '127.8000', '5. volume': '491'}, '2021-10-22 17:35:00': {'1. open': '127.8200', '2. high': '127.8200', '3. low': '127.8000', '4. close': '127.8000', '5. volume': '952'}, '2021-10-22 17:30:00': {'1. open': '127.8500', '2. high': '127.8500', '3. low': '127.8001', '4. close': '127.8500', '5. volume': '1659'}, '2021-10-22 17:20:00': {'1. open': '127.8000', '2. high': '127.8000', '3. low': '127.8000', '4. close': '127.8000', '5. volume': '300'}, '2021-10-22 17:10:00': {'1. open': '127.8800', '2. high': '127.8800', '3. low': '127.8800', '4. close': '127.8800', '5. volume': '1503'}, '2021-10-22 17:05:00': {'1. open': '127.7500', '2. high': '127.8500', '3. low': '127.7500', '4. close': '127.8500', '5. volume': '861'}, '2021-10-22 16:55:00': {'1. open': '127.6800', '2. high': '127.6800', '3. low': '127.6800', '4. close': '127.6800', '5. volume': '169'}, '2021-10-22 16:50:00': {'1. open': '127.6900', '2. high': '127.6900', '3. low': '127.6900', '4. close': '127.6900', '5. volume': '417'}, '2021-10-22 16:45:00': {'1. open': '127.6700', '2. high': '127.6800', '3. low': '127.6700', '4. close': '127.6800', '5. volume': '1644'}, '2021-10-22 16:40:00': {'1. open': '127.7600', '2. high': '127.7600', '3. low': '127.7500', '4. close': '127.7500', '5. volume': '5373'}, '2021-10-22 16:25:00': {'1. open': '127.8500', '2. high': '127.8500', '3. low': '127.8500', '4. close': '127.8500', '5. volume': '177'}, '2021-10-22 16:20:00': {'1. open': '127.8600', '2. high': '127.8800', '3. low': '127.8600', '4. close': '127.8800', '5. volume': '12565'}, '2021-10-22 16:15:00': {'1. open': '127.8000', '2. high': '127.8600', '3. low': '127.8000', '4. close': '127.8600', '5. volume': '1570'}, '2021-10-22 16:10:00': {'1. open': '127.9000', '2. high': '127.9000', '3. low': '127.9000', '4. close': '127.9000', '5. volume': '302'}, '2021-10-22 16:05:00': {'1. open': '127.8800', '2. high': '127.9000', '3. low': '127.8800', '4. close': '127.8999', '5. volume': '115234'}, '2021-10-22 16:00:00': {'1. open': '127.7000', '2. high': '127.9200', '3. low': '127.6800', '4. close': '127.9100', '5. volume': '411149'}, '2021-10-22 15:55:00': {'1. open': '127.5600', '2. high': '127.7400', '3. low': '127.4800', '4. close': '127.6900', '5. volume': '227377'}, '2021-10-22 15:50:00': {'1. open': '127.4500', '2. high': '127.5300', '3. low': '127.3900', '4. close': '127.5300', '5. volume': '138500'}, '2021-10-22 15:45:00': {'1. open': '127.4591', '2. high': '127.6300', '3. low': '127.4000', '4. close': '127.4800', '5. volume': '141700'}, '2021-10-22 15:40:00': {'1. open': '127.6600', '2. high': '127.7000', '3. low': '127.4400', '4. close': '127.4500', '5. volume': '119196'}, '2021-10-22 15:35:00': {'1. open': '127.5200', '2. high': '127.7000', '3. low': '127.4762', '4. close': '127.6400', '5. volume': '117481'}, '2021-10-22 15:30:00': {'1. open': '127.6400', '2. high': '127.6800', '3. low': '127.4400', '4. close': '127.5200', '5. volume': '85930'}, '2021-10-22 15:25:00': {'1. open': '127.5850', '2. high': '127.6500', '3. low': '127.5300', '4. close': '127.6400', '5. volume': '114342'}, '2021-10-22 15:20:00': {'1. open': '127.7000', '2. high': '127.7400', '3. low': '127.5700', '4. close': '127.5700', '5. volume': '68379'}, '2021-10-22 15:15:00': {'1. open': '127.7706', '2. high': '127.8500', '3. low': '127.5500', '4. close': '127.7000', '5. volume': '108309'}, '2021-10-22 15:10:00': {'1. open': '128.0150', '2. high': '128.0700', '3. low': '127.7200', '4. close': '127.7500', '5. volume': '118934'}, '2021-10-22 15:05:00': {'1. open': '128.1350', '2. high': '128.2100', '3. low': '128.0000', '4. close': '128.0200', '5. volume': '87949'}, '2021-10-22 15:00:00': {'1. open': '128.4000', '2. high': '128.4437', '3. low': '128.1200', '4. close': '128.1200', '5. volume': '94826'}, '2021-10-22 14:55:00': {'1. open': '128.5737', '2. high': '128.6200', '3. low': '128.3800', '4. close': '128.3950', '5. volume': '120231'}, '2021-10-22 14:50:00': {'1. open': '128.4500', '2. high': '128.5800', '3. low': '128.3100', '4. close': '128.5756', '5. volume': '130380'}, '2021-10-22 14:45:00': {'1. open': '128.0800', '2. high': '128.4900', '3. low': '128.0500', '4. close': '128.4500', '5. volume': '186520'}, '2021-10-22 14:40:00': {'1. open': '127.9250', '2. high': '128.1300', '3. low': '127.9100', '4. close': '128.0700', '5. volume': '100207'}, '2021-10-22 14:35:00': {'1. open': '127.6500', '2. high': '127.9600', '3. low': '127.6200', '4. close': '127.9218', '5. volume': '104712'}, '2021-10-22 14:30:00': {'1. open': '127.5546', '2. high': '127.6500', '3. low': '127.5400', '4. close': '127.6400', '5. volume': '42927'}, '2021-10-22 14:25:00': {'1. open': '127.5500', '2. high': '127.6400', '3. low': '127.5300', '4. close': '127.5600', '5. volume': '60749'}, '2021-10-22 14:20:00': {'1. open': '127.4063', '2. high': '127.5597', '3. low': '127.3500', '4. close': '127.5500', '5. volume': '55999'}, '2021-10-22 14:15:00': {'1. open': '127.1900', '2. high': '127.4100', '3. low': '127.1750', '4. close': '127.4100', '5. volume': '57229'}, '2021-10-22 14:10:00': {'1. open': '127.1200', '2. high': '127.1900', '3. low': '127.0800', '4. close': '127.1800', '5. volume': '45705'}, '2021-10-22 14:05:00': {'1. open': '127.1600', '2. high': '127.2200', '3. low': '127.1000', '4. close': '127.1400', '5. volume': '60782'}, '2021-10-22 14:00:00': {'1. open': '127.2900', '2. high': '127.3100', '3. low': '127.1100', '4. close': '127.1500', '5. volume': '91613'}, '2021-10-22 13:55:00': {'1. open': '127.2500', '2. high': '127.3300', '3. low': '127.2400', '4. close': '127.2910', '5. volume': '46427'}, '2021-10-22 13:50:00': {'1. open': '127.3300', '2. high': '127.3785', '3. low': '127.2300', '4. close': '127.2396', '5. volume': '57434'}, '2021-10-22 13:45:00': {'1. open': '127.3900', '2. high': '127.4900', '3. low': '127.3300', '4. close': '127.3360', '5. volume': '52193'}, '2021-10-22 13:40:00': {'1. open': '127.0800', '2. high': '127.4900', '3. low': '127.0800', '4. close': '127.4100', '5. volume': '98774'}, '2021-10-22 13:35:00': {'1. open': '127.0300', '2. high': '127.0800', '3. low': '126.9300', '4. close': '127.0800', '5. volume': '77562'}, '2021-10-22 13:30:00': {'1. open': '127.1500', '2. high': '127.1950', '3. low': '127.0300', '4. close': '127.0300', '5. volume': '45844'}, '2021-10-22 13:25:00': {'1. open': '127.0650', '2. high': '127.2300', '3. low': '127.0650', '4. close': '127.1700', '5. volume': '93936'}, '2021-10-22 13:20:00': {'1. open': '126.9001', '2. high': '127.1300', '3. low': '126.8950', '4. close': '127.0700', '5. volume': '73328'}, '2021-10-22 13:15:00': {'1. open': '126.7800', '2. high': '127.0500', '3. low': '126.7200', '4. close': '126.9200', '5. volume': '132906'}, '2021-10-22 13:10:00': {'1. open': '126.6850', '2. high': '126.7800', '3. low': '126.6110', '4. close': '126.7800', '5. volume': '71888'}, '2021-10-22 13:05:00': {'1. open': '126.7400', '2. high': '126.7950', '3. low': '126.6490', '4. close': '126.6700', '5. volume': '103074'}, '2021-10-22 13:00:00': {'1. open': '126.9000', '2. high': '126.9100', '3. low': '126.7100', '4. close': '126.7400', '5. volume': '99341'}, '2021-10-22 12:55:00': {'1. open': '126.9500', '2. high': '127.0300', '3. low': '126.8500', '4. close': '126.8991', '5. volume': '53396'}, '2021-10-22 12:50:00': {'1. open': '127.0750', '2. high': '127.1500', '3. low': '126.9300', '4. close': '126.9500', '5. volume': '109250'}, '2021-10-22 12:45:00': {'1. open': '126.7700', '2. high': '127.0900', '3. low': '126.7500', '4. close': '127.0600', '5. volume': '115625'}, '2021-10-22 12:40:00': {'1. open': '127.1000', '2. high': '127.1800', '3. low': '126.7700', '4. close': '126.7700', '5. volume': '268499'}, '2021-10-22 12:35:00': {'1. open': '127.1650', '2. high': '127.2500', '3. low': '127.1100', '4. close': '127.1100', '5. volume': '89021'}, '2021-10-22 12:30:00': {'1. open': '127.3000', '2. high': '127.3500', '3. low': '127.1000', '4. close': '127.1899', '5. volume': '160760'}, '2021-10-22 12:25:00': {'1. open': '127.5900', '2. high': '127.5900', '3. low': '127.3000', '4. close': '127.3000', '5. volume': '162859'}, '2021-10-22 12:20:00': {'1. open': '127.8250', '2. high': '127.8250', '3. low': '127.5100', '4. close': '127.5750', '5. volume': '114130'}, '2021-10-22 12:15:00': {'1. open': '127.9300', '2. high': '128.0800', '3. low': '127.8100', '4. close': '127.8300', '5. volume': '64608'}, '2021-10-22 12:10:00': {'1. open': '127.9193', '2. high': '128.0194', '3. low': '127.8800', '4. close': '127.9100', '5. volume': '60818'}, '2021-10-22 12:05:00': {'1. open': '127.7800', '2. high': '127.9900', '3. low': '127.7200', '4. close': '127.9280', '5. volume': '96753'}, '2021-10-22 12:00:00': {'1. open': '127.8600', '2. high': '127.8700', '3. low': '127.7300', '4. close': '127.7800', '5. volume': '70656'}, '2021-10-22 11:55:00': {'1. open': '127.7700', '2. high': '127.8900', '3. low': '127.7500', '4. close': '127.8600', '5. volume': '83009'}, '2021-10-22 11:50:00': {'1. open': '127.6889', '2. high': '127.8326', '3. low': '127.6400', '4. close': '127.7519', '5. volume': '75931'}, '2021-10-22 11:45:00': {'1. open': '127.5900', '2. high': '127.7950', '3. low': '127.5800', '4. close': '127.6950', '5. volume': '95527'}, '2021-10-22 11:40:00': {'1. open': '127.6300', '2. high': '127.7700', '3. low': '127.5473', '4. close': '127.5700', '5. volume': '121419'}, '2021-10-22 11:35:00': {'1. open': '127.5800', '2. high': '127.6800', '3. low': '127.4400', '4. close': '127.6200', '5. volume': '176600'}, '2021-10-22 11:30:00': {'1. open': '127.6400', '2. high': '127.8000', '3. low': '127.5800', '4. close': '127.5900', '5. volume': '95760'}, '2021-10-22 11:25:00': {'1. open': '127.7800', '2. high': '127.9300', '3. low': '127.5500', '4. close': '127.6100', '5. volume': '162279'}, '2021-10-22 11:20:00': {'1. open': '127.6500', '2. high': '127.7900', '3. low': '127.6300', '4. close': '127.7600', '5. volume': '90332'}, '2021-10-22 11:15:00': {'1. open': '127.7900', '2. high': '127.8700', '3. low': '127.6400', '4. close': '127.6700', '5. volume': '169753'}, '2021-10-22 11:10:00': {'1. open': '127.6300', '2. high': '127.9000', '3. low': '127.6100', '4. close': '127.8100', '5. volume': '170370'}, '2021-10-22 11:05:00': {'1. open': '127.6500', '2. high': '127.7300', '3. low': '127.5300', '4. close': '127.6500', '5. volume': '228930'}, '2021-10-22 11:00:00': {'1. open': '128.1821', '2. high': '128.1883', '3. low': '127.6300', '4. close': '127.6600', '5. volume': '236651'}, '2021-10-22 10:55:00': {'1. open': '128.4000', '2. high': '128.4000', '3. low': '128.1300', '4. close': '128.1700', '5. volume': '113491'}, '2021-10-22 10:50:00': {'1. open': '128.5950', '2. high': '128.6600', '3. low': '128.4100', '4. close': '128.4100', '5. volume': '100759'}, '2021-10-22 10:45:00': {'1. open': '128.7350', '2. high': '128.7500', '3. low': '128.4800', '4. close': '128.5900', '5. volume': '126518'}, '2021-10-22 10:40:00': {'1. open': '129.1150', '2. high': '129.1300', '3. low': '128.5900', '4. close': '128.7100', '5. volume': '230297'}, '2021-10-22 10:35:00': {'1. open': '129.3300', '2. high': '129.3300', '3. low': '129.0214', '4. close': '129.1100', '5. volume': '99650'}, '2021-10-22 10:30:00': {'1. open': '129.2560', '2. high': '129.4300', '3. low': '129.0800', '4. close': '129.3300', '5. volume': '133989'}}}

////    DAILYY    ////


{'Meta Data': {'1. Information': 'Daily Prices (open, high, low, close) and Volumes', '2. Symbol': 'IBM', '3. Last Refreshed': '2021-10-22', '4. Output Size': 'Compact', '5. Time Zone': 'US/Eastern'}, 'Time Series (Daily)': {'2021-10-22': {'1. open': '128.0500', '2. high': '130.2500', '3. low': '126.6110', '4. close': '127.8800', '5. volume': '11582195'}, '2021-10-21': {'1. open': '133.5100', '2. high': '133.7200', '3. low': '128.1000', '4. close': '128.3300', '5. volume': '31466529'}, '2021-10-20': {'1. open': '141.6800', '2. high': '142.2000', '3. low': '140.7000', '4. close': '141.9000', '5. volume': '6189255'}, '2021-10-19': {'1. open': '141.0800', '2. high': '142.9400', '3. low': '140.5201', '4. close': '141.9800', '5. volume': '4339548'}, '2021-10-18': {'1. open': '144.0000', '2. high': '144.9400', '3. low': '141.7590', '4. close': '142.3200', '5. volume': '6154055'}, '2021-10-15': {'1. open': '143.3900', '2. high': '144.8500', '3. low': '142.7900', '4. close': '144.6100', '5. volume': '3222778'}, '2021-10-14': {'1. open': '141.0400', '2. high': '143.9200', '3. low': '141.0100', '4. close': '143.3900', '5. volume': '4217305'}, '2021-10-13': {'1. open': '140.5200', '2. high': '141.4100', '3. low': '139.6600', '4. close': '140.7600', '5. volume': '2880747'}, '2021-10-12': {'1. open': '142.2100', '2. high': '142.3000', '3. low': '140.3000', '4. close': '140.4700', '5. volume': '3148559'}, '2021-10-11': {'1. open': '143.5000', '2. high': '144.0800', '3. low': '142.4000', '4. close': '142.4300', '5. volume': '2793298'}, '2021-10-08': {'1. open': '141.8100', '2. high': '143.6500', '3. low': '141.0500', '4. close': '143.2200', '5. volume': '3731279'}, '2021-10-07': {'1. open': '142.7300', '2. high': '143.3950', '3. low': '141.5300', '4. close': '141.8100', '5. volume': '3823803'}, '2021-10-06': {'1. open': '142.4800', '2. high': '143.3700', '3. low': '140.8900', '4. close': '142.3600', '5. volume': '5328433'}, '2021-10-05': {'1. open': '144.7500', '2. high': '145.0000', '3. low': '142.6400', '4. close': '143.1500', '5. volume': '6976648'}, '2021-10-04': {'1. open': '142.7400', '2. high': '146.0000', '3. low': '142.3501', '4. close': '144.1100', '5. volume': '7351128'}, '2021-10-01': {'1. open': '141.0000', '2. high': '143.9700', '3. low': '140.3700', '4. close': '143.3200', '5. volume': '6604064'}, '2021-09-30': {'1. open': '140.0000', '2. high': '140.5700', '3. low': '138.5000', '4. close': '138.9300', '5. volume': '5824431'}, '2021-09-29': {'1. open': '137.7300', '2. high': '139.9300', '3. low': '136.4400', '4. close': '139.1800', '5. volume': '3774236'}, '2021-09-28': {'1. open': '139.1700', '2. high': '139.6880', '3. low': '137.2100', '4. close': '137.4700', '5. volume': '4314595'}, '2021-09-27': {'1. open': '137.9600', '2. high': '139.0650', '3. low': '137.4800', '4. close': '138.5600', '5. volume': '3306865'}, '2021-09-24': {'1. open': '137.0300', '2. high': '138.4800', '3. low': '136.7500', '4. close': '137.4900', '5. volume': '2964397'}, '2021-09-23': {'1. open': '135.2500', '2. high': '137.4200', '3. low': '135.0300', '4. close': '136.7300', '5. volume': '3013238'}, '2021-09-22': {'1. open': '133.7200', '2. high': '135.3700', '3. low': '133.4700', '4. close': '134.6300', '5. volume': '3602416'}, '2021-09-21': {'1. open': '135.1100', '2. high': '135.6500', '3. low': '132.9400', '4. close': '132.9700', '5. volume': '4074528'}, '2021-09-20': {'1. open': '133.9000', '2. high': '135.1800', '3. low': '132.7800', '4. close': '134.3100', '5. volume': '4770651'}, '2021-09-17': {'1. open': '135.7500', '2. high': '135.9199', '3. low': '135.0500', '4. close': '135.2300', '5. volume': '5633480'}, '2021-09-16': {'1. open': '137.2800', '2. high': '137.9500', '3. low': '135.7100', '4. close': '136.4300', '5. volume': '2643975'}, '2021-09-15': {'1. open': '136.2200', '2. high': '137.8000', '3. low': '135.6700', '4. close': '137.2000', '5. volume': '3254122'}, '2021-09-14': {'1. open': '138.4000', '2. high': '138.5700', '3. low': '135.3400', '4. close': '136.2200', '5. volume': '4454291'}, '2021-09-13': {'1. open': '138.4000', '2. high': '138.9900', '3. low': '137.5100', '4. close': '138.1500', '5. volume': '4144345'}, '2021-09-10': {'1. open': '138.8200', '2. high': '139.3699', '3. low': '137.0000', '4. close': '137.0200', '5. volume': '3975115'}, '2021-09-09': {'1. open': '137.8500', '2. high': '138.9600', '3. low': '137.5550', '4. close': '137.7400', '5. volume': '3508363'}, '2021-09-08': {'1. open': '138.1400', '2. high': '139.0900', '3. low': '137.6000', '4. close': '138.6700', '5. volume': '2985409'}, '2021-09-07': {'1. open': '139.6500', '2. high': '139.7900', '3. low': '137.7614', '4. close': '138.0600', '5. volume': '3285363'}, '2021-09-03': {'1. open': '139.6800', '2. high': '140.4700', '3. low': '139.3000', '4. close': '139.5800', '5. volume': '1924215'}, '2021-09-02': {'1. open': '139.7200', '2. high': '140.0500', '3. low': '139.0300', '4. close': '140.0100', '5. volume': '2715659'}, '2021-09-01': {'1. open': '139.9800', '2. high': '140.0699', '3. low': '139.1900', '4. close': '139.3000', '5. volume': '2474544'}, '2021-08-31': {'1. open': '139.5400', '2. high': '140.9400', '3. low': '138.9500', '4. close': '140.3400', '5. volume': '4235101'}, '2021-08-30': {'1. open': '139.5000', '2. high': '139.8800', '3. low': '138.8150', '4. close': '138.9700', '5. volume': '1995526'}, '2021-08-27': {'1. open': '138.7100', '2. high': '139.5850', '3. low': '138.4000', '4. close': '139.4100', '5. volume': '2459643'}, '2021-08-26': {'1. open': '139.9700', '2. high': '140.8000', '3. low': '138.7100', '4. close': '138.7800', '5. volume': '2498915'}, '2021-08-25': {'1. open': '139.9200', '2. high': '140.8000', '3. low': '139.4600', '4. close': '139.8600', '5. volume': '2012817'}, '2021-08-24': {'1. open': '139.7800', '2. high': '140.2300', '3. low': '139.3200', '4. close': '139.8400', '5. volume': '2365638'}, '2021-08-23': {'1. open': '139.6200', '2. high': '140.1500', '3. low': '138.8000', '4. close': '139.6200', '5. volume': '3039587'}, '2021-08-20': {'1. open': '137.7400', '2. high': '139.3800', '3. low': '137.2700', '4. close': '139.1100', '5. volume': '2657763'}, '2021-08-19': {'1. open': '138.6900', '2. high': '139.4500', '3. low': '137.2100', '4. close': '138.0200', '5. volume': '4160129'}, '2021-08-18': {'1. open': '141.6700', '2. high': '141.9150', '3. low': '139.3900', '4. close': '139.4700', '5. volume': '3510694'}, '2021-08-17': {'1. open': '143.0000', '2. high': '143.1600', '3. low': '141.0900', '4. close': '142.4200', '5. volume': '3074078'}, '2021-08-16': {'1. open': '143.2300', '2. high': '143.7400', '3. low': '142.2300', '4. close': '143.5900', '5. volume': '2786343'}, '2021-08-13': {'1. open': '142.6400', '2. high': '143.5800', '3. low': '142.4400', '4. close': '143.1800', '5. volume': '1908951'}, '2021-08-12': {'1. open': '142.2600', '2. high': '143.1500', '3. low': '142.0766', '4. close': '143.0700', '5. volume': '2089418'}, '2021-08-11': {'1. open': '141.7800', '2. high': '142.7685', '3. low': '141.5000', '4. close': '142.1300', '5. volume': '4259952'}, '2021-08-10': {'1. open': '141.2100', '2. high': '141.8110', '3. low': '140.3400', '4. close': '141.3800', '5. volume': '5299869'}, '2021-08-09': {'1. open': '142.2000', '2. high': '142.4950', '3. low': '140.9700', '4. close': '141.2500', '5. volume': '4904065'}, '2021-08-06': {'1. open': '143.0000', '2. high': '144.3900', '3. low': '142.8900', '4. close': '144.0900', '5. volume': '3826835'}, '2021-08-05': {'1. open': '143.0300', '2. high': '143.4100', '3. low': '142.2200', '4. close': '142.7700', '5. volume': '2757389'}, '2021-08-04': {'1. open': '143.8000', '2. high': '144.1800', '3. low': '142.4700', '4. close': '142.7600', '5. volume': '2830079'}, '2021-08-03': {'1. open': '141.9000', '2. high': '144.7000', '3. low': '141.6500', '4. close': '144.0700', '5. volume': '4084724'}, '2021-08-02': {'1. open': '141.4500', '2. high': '143.0600', '3. low': '141.0300', '4. close': '141.4200', '5. volume': '2929540'}, '2021-07-30': {'1. open': '141.5200', '2. high': '141.8500', '3. low': '140.7900', '4. close': '140.9600', '5. volume': '3535555'}, '2021-07-29': {'1. open': '142.3300', '2. high': '142.9600', '3. low': '141.6000', '4. close': '141.9300', '5. volume': '2657669'}, '2021-07-28': {'1. open': '143.0100', '2. high': '143.1000', '3. low': '141.6400', '4. close': '141.7700', '5. volume': '2544099'}, '2021-07-27': {'1. open': '142.5300', '2. high': '143.6400', '3. low': '141.6000', '4. close': '142.7500', '5. volume': '3137027'}, '2021-07-26': {'1. open': '141.3900', '2. high': '143.0000', '3. low': '141.1300', '4. close': '142.7700', '5. volume': '4246266'}, '2021-07-23': {'1. open': '140.9600', '2. high': '141.7000', '3. low': '140.3300', '4. close': '141.3400', '5. volume': '4474157'}, '2021-07-22': {'1. open': '141.6600', '2. high': '141.8100', '3. low': '140.4100', '4. close': '140.7100', '5. volume': '3314153'}, '2021-07-21': {'1. open': '139.9700', '2. high': '141.3900', '3. low': '139.6500', '4. close': '141.3000', '5. volume': '4803977'}, '2021-07-20': {'1. open': '143.0000', '2. high': '144.9200', '3. low': '138.7000', '4. close': '139.9700', '5. volume': '13611675'}, '2021-07-19': {'1. open': '136.4500', '2. high': '138.4900', '3. low': '136.2089', '4. close': '137.9200', '5. volume': '8582302'}, '2021-07-16': {'1. open': '141.0000', '2. high': '141.0000', '3. low': '138.5900', '4. close': '138.9000', '5. volume': '4109308'}, '2021-07-15': {'1. open': '139.3200', '2. high': '140.4600', '3. low': '138.8005', '4. close': '140.4500', '5. volume': '3639698'}, '2021-07-14': {'1. open': '140.7200', '2. high': '140.7500', '3. low': '138.9273', '4. close': '139.8200', '5. volume': '4403752'}, '2021-07-13': {'1. open': '140.9200', '2. high': '140.9200', '3. low': '139.6300', '4. close': '140.2800', '5. volume': '3164294'}, '2021-07-12': {'1. open': '141.4300', '2. high': '141.9599', '3. low': '140.1150', '4. close': '140.9200', '5. volume': '3342627'}, '2021-07-09': {'1. open': '141.4500', '2. high': '141.9800', '3. low': '140.8410', '4. close': '141.5200', '5. volume': '3904059'}, '2021-07-08': {'1. open': '137.7800', '2. high': '141.3100', '3. low': '137.6600', '4. close': '140.7400', '5. volume': '5487425'}, '2021-07-07': {'1. open': '138.7600', '2. high': '140.3300', '3. low': '138.7600', '4. close': '139.8200', '5. volume': '4059667'}, '2021-07-06': {'1. open': '139.9900', '2. high': '140.4200', '3. low': '137.1000', '4. close': '138.7800', '5. volume': '8093747'}, '2021-07-02': {'1. open': '146.9100', '2. high': '146.9500', '3. low': '139.4600', '4. close': '140.0200', '5. volume': '16828161'}, '2021-07-01': {'1. open': '146.9600', '2. high': '147.5000', '3. low': '146.5700', '4. close': '146.8400', '5. volume': '2686289'}, '2021-06-30': {'1. open': '145.1300', '2. high': '146.9300', '3. low': '144.7100', '4. close': '146.5900', '5. volume': '3245091'}, '2021-06-29': {'1. open': '145.2600', '2. high': '146.7400', '3. low': '145.1000', '4. close': '145.5500', '5. volume': '2428626'}, '2021-06-28': {'1. open': '147.0100', '2. high': '147.3000', '3. low': '144.9121', '4. close': '145.2900', '5. volume': '3888869'}, '2021-06-25': {'1. open': '145.3800', '2. high': '146.9300', '3. low': '144.9450', '4. close': '146.8400', '5. volume': '3594218'}, '2021-06-24': {'1. open': '145.8000', '2. high': '146.1900', '3. low': '144.6900', '4. close': '145.4400', '5. volume': '3609679'}, '2021-06-23': {'1. open': '146.4300', '2. high': '146.5000', '3. low': '144.5700', '4. close': '144.6100', '5. volume': '3202644'}, '2021-06-22': {'1. open': '146.5200', '2. high': '146.8100', '3. low': '145.3500', '4. close': '146.3600', '5. volume': '2437121'}, '2021-06-21': {'1. open': '144.1100', '2. high': '147.0700', '3. low': '144.0600', '4. close': '146.6500', '5. volume': '4285711'}, '2021-06-18': {'1. open': '144.4800', '2. high': '144.6800', '3. low': '143.0400', '4. close': '143.1200', '5. volume': '9156505'}, '2021-06-17': {'1. open': '147.5500', '2. high': '148.0600', '3. low': '145.2800', '4. close': '145.6000', '5. volume': '4367387'}, '2021-06-16': {'1. open': '149.7600', '2. high': '149.7600', '3. low': '147.2200', '4. close': '147.8300', '5. volume': '3795420'}, '2021-06-15': {'1. open': '149.8500', '2. high': '149.9100', '3. low': '148.6000', '4. close': '149.3600', '5. volume': '2513281'}, '2021-06-14': {'1. open': '150.7100', '2. high': '151.0300', '3. low': '148.6550', '4. close': '150.0300', '5. volume': '3344845'}, '2021-06-11': {'1. open': '150.4300', '2. high': '151.8450', '3. low': '150.3700', '4. close': '151.2800', '5. volume': '3438255'}, '2021-06-10': {'1. open': '151.4700', '2. high': '152.8400', '3. low': '149.7600', '4. close': '150.5400', '5. volume': '4758488'}, '2021-06-09': {'1. open': '149.0300', '2. high': '151.0700', '3. low': '148.8200', '4. close': '150.6700', '5. volume': '5303252'}, '2021-06-08': {'1. open': '148.1200', '2. high': '150.2000', '3. low': '148.1200', '4. close': '149.0700', '5. volume': '5080099'}, '2021-06-07': {'1. open': '147.5500', '2. high': '148.7400', '3. low': '147.1700', '4. close': '148.0200', '5. volume': '3462712'}, '2021-06-04': {'1. open': '146.0000', '2. high': '147.5500', '3. low': '145.7600', '4. close': '147.4200', '5. volume': '3117905'}, '2021-06-03': {'1. open': '144.9100', '2. high': '145.8800', '3. low': '144.0400', '4. close': '145.5500', '5. volume': '4130741'}}}


////  Global_Quote

{'Global Quote': {'01. symbol': 'IBM', '02. open': '128.0500', '03. high': '130.2500', '04. low': '126.6110', '05. price': '127.8800', '06. volume': '11582195', '07. latest trading day': '2021-10-22', '08. previous close': '128.3300', '09. change': '-0.4500', '10. change percent': '-0.3507%'}}


////  Overview  /// 

{"Symbol": "IBM", "AssetType": "Common Stock", "Name": "International Business Machines Corporation", "Description": "International Business Machines Corporation (IBM) is an American multinational technology company headquartered in Armonk, New York, with operations in over 170 countries. The company began in 1911, founded in Endicott, New York, as the Computing-Tabulating-Recording Company (CTR) and was renamed International Business Machines in 1924. IBM is incorporated in New York. IBM produces and sells computer hardware, middleware and software, and provides hosting and consulting services in areas ranging from mainframe computers to nanotechnology. IBM is also a major research organization, holding the record for most annual U.S. patents generated by a business (as of 2020) for 28 consecutive years. Inventions by IBM include the automated teller machine (ATM), the floppy disk, the hard disk drive, the magnetic stripe card, the relational database, the SQL programming language, the UPC barcode, and dynamic random-access memory (DRAM). The IBM mainframe, exemplified by the System/360, was the dominant computing platform during the 1960s and 1970s.", "CIK": "51143", "Exchange": "NYSE", "Currency": "USD", "Country": "USA", "Sector": "TECHNOLOGY", "Industry": "COMPUTER & OFFICE EQUIPMENT", "Address": "1 NEW ORCHARD ROAD, ARMONK, NY, US", "FiscalYearEnd": "December", "LatestQuarter": "2021-09-30", "MarketCapitalization": "114621399000", "EBITDA": "16436000000", "PERatio": "24.21", "PEGRatio": "1.335", "BookValue": "24.78", "DividendPerShare": "6.54", "DividendYield": "0.051", "EPS": "5.28", "RevenuePerShareTTM": "83.23", "ProfitMargin": "0.064", "OperatingMarginTTM": "0.13", "ReturnOnAssetsTTM": "0.0406", "ReturnOnEquityTTM": "0.214", "RevenueTTM": "74461004000", "GrossProfitTTM": "35575000000", "DilutedEPSTTM": "5.28", "QuarterlyEarningsGrowthYOY": "-0.338", "QuarterlyRevenueGrowthYOY": "0.003", "AnalystTargetPrice": "151.12", "TrailingPE": "24.21", "ForwardPE": "10.55", "PriceToSalesRatioTTM": "1.539", "PriceToBookRatio": "4.224", "EVToRevenue": "1.945", "EVToEBITDA": "11.17", "Beta": "1.181", "52WeekHigh": "151.1", "52WeekLow": "100.73", "50DayMovingAverage": "138.74", "200DayMovingAverage": "141.49", "SharesOutstanding": "896320000", "SharesFloat": "895521000", "SharesShort": "25805200", "SharesShortPriorMonth": "25087600", "ShortRatio": "7.16", "ShortPercentOutstanding": "0.03", "ShortPercentFloat": "0.0288", "PercentInsiders": "0.133", "PercentInstitutions": "57.78", "ForwardAnnualDividendRate": "6.56", "ForwardAnnualDividendYield": "0.0513", "PayoutRatio": "0.58", "DividendDate": "2021-09-10", "ExDividendDate": "2021-08-09", "LastSplitFactor": "2:1", "LastSplitDate": "1999-05-27"}

'''