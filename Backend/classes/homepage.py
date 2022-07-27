from logging import error
from yahoo_fin.stock_info import *
from bs4 import BeautifulSoup
import requests

# Class for homepage. Has methods for displaying required elements.
class Homepage():
    
    # Gets the most active NASDAQ stocks.
    def most_active_nasdaq():
        # Returns dictionary, key = stock_code, value = %change
        temp = {}
        # Gets the top 25 stocks in pandas dataframe.
        active = get_day_most_active()
        
        # Only get 'N' stocks.
        count = 0
        N = 6
        while count < N:
            temp[active.iat[count, 0]] = active.iat[count, 4]
            count += 1
        
        try:
            return temp
		
        except Exception as E:
            return {"error_message" : "Something is wrong!"}, 404


    # Gets the highest moving NASDAQ stocks (top gainers and top losers).
    def highest_moving_nasdaq():
        # Returns dictionary, key = stock_code, value = %change
        movers = {}
        gainers = get_day_gainers()
        losers = get_day_losers()
        
        # Highest 'N' Moving Stocks
        count = 0
        N = 6
        while count < N:
            movers[gainers.iat[count, 0]] = gainers.iat[count, 4]
            movers[losers.iat[count, 0]] = losers.iat[count, 4]
            count += 1

        try:
            return movers
            
        except Exception as E:
            return {"error_message" : "Something is wrong!"}, 404
    
    # Gets the highest moving ASX stocks (top gainers and top losers), using requests.
    def highest_moving_asx():
        # Some issues with requests, if internet is too slow
        try:
            # Returns dictionary, key = stock_code, value = %change
            movers = {}

            # Get values from website table.
            resp_gainers = requests.get('https://au.finance.yahoo.com/gainers/')
            resp_losers = requests.get('https://au.finance.yahoo.com/losers/')
            bsoup_gainers = BeautifulSoup(resp_gainers.text, features="lxml")
            bsoup_losers = BeautifulSoup(resp_losers.text, features="lxml")
            table_gainers = bsoup_gainers.find('tbody')
            table_losers = bsoup_losers.find('tbody')

            # Highest 'N' Moving Stocks
            count = 0
            N = 6

            # Add to dictionary
            # ONLY .AX is ASX, do not add XA. (That is CHI-X)
            # Must remove commas in strings for type conversion to work
            for row in table_gainers.findAll('tr'):
                if row.find('a').get_text()[-2:] == 'AX' and count < N:
                    movers[row.find('a').get_text()[:-3]] = float(row.find('td', { "aria-label" : f"% change" }).get_text()[:-1].replace(',',''))
                    count += 1
            count = 0
            for row in table_losers.findAll('tr'):
                if row.find('a').get_text()[-2:] == 'AX' and count < N:
                    movers[row.find('a').get_text()[:-3]] = float(row.find('td', { "aria-label" : f"% change" }).get_text()[:-1].replace(',',''))
                    count += 1
            return movers
            
        except Exception as E:
            return {'Error': E}
    
    # Gets the most active ASX stocks using requests.
    def most_active_asx():
        # Some issues with requests, if internet is too slow
        try:
            # Returns dictionary, key = stock_code, value = %change
            temp = {}

            # Get values from website table.
            resp_active = requests.get('https://au.finance.yahoo.com/most-active/')
            bsoup_active = BeautifulSoup(resp_active.text, features="lxml")
            table_active = bsoup_active.find('tbody')
            
            # Highest 'N' Moving Stocks
            count = 0
            N = 6

            # Add to dictionary
            # ONLY .AX is ASX, do not add XA.
            # Must remove commas in strings for type conversion to work
            for row in table_active.findAll('tr'):
                if row.find('a').get_text()[-2:] == 'AX' and count < N:
                    temp[row.find('a').get_text()[:-3]] = float(row.find('td', { "aria-label" : f"% change" }).get_text()[:-1].replace(',',''))
                    count += 1
            return temp

        except Exception as E:
            return {'Error': E + ' Try refreshing, your internet may be slow.'}

if __name__ == "__main__":
    Homepage.market_index()


