from yahoo_fin.stock_info import *

# Class for individual stocks. 
# Has methods to retrieve specific data of stock.
# Substitutes 'N/A' for unavaliable data.
class Stock():
    def __init__(self, symbol):
        self.symbol = symbol
        # Gets quote data from yahoo_fin library
        self.quote_data = get_quote_data(self.symbol)

    # Returns the name of stock, N/A for not available
    def name(self):
        try:
            return self.quote_data['longName']
        except KeyError:
            return "N/A"
    
    # Returns the stock symbol, N/A for not available
    def code(self):
        return self.symbol

    # Returns the market of stock, N/A for not available
    def market(self):
        try:
            if self.quote_data['market'] == 'us_market':
                return "US"
            elif self.quote_data['market'] == 'au_market':
                return "AU"
            else:
                return self.quote_data['market']
        except KeyError:
            return "N/A"

    # Returns the stock's previous close, N/A for not available
    def close(self):
        try:
            return self.quote_data['regularMarketPreviousClose']
        except KeyError:
            return "N/A"

    # Returns the stock's previous open, N/A for not available
    def open(self):
        try:
            return self.quote_data['regularMarketOpen']
        except KeyError:
            return "N/A"

    # Returns the stock's current intraday volume, N/A for not available
    def volume(self):
        try:
            return self.quote_data['regularMarketVolume']
        except KeyError:
            return "N/A"
        
    # Returns the stock's market capitalisation, N/A for not available
    def market_cap(self):
        try:
            return self.quote_data['marketCap']
        except KeyError:
            return "N/A"

    # Returns the stock's current price, N/A for not available
    def price(self):
        try:
            return self.quote_data['regularMarketPrice']
        except KeyError:
            return "N/A"

    # Returns the stock's currency, N/A for not available
    def currency(self):
        try:
            return self.quote_data['currency']
        except:
            return "N/A"
    
    # Returns the stock's price change as total, N/A for not available
    def change(self):
        try:
            return float("{:.2f}".format(self.quote_data['regularMarketChange']))
        except:
            return "N/A"
    
    # Returns the stock's price change as %, N/A for not available
    def change_perc(self):
        try:
            return "{:.1f}%".format(self.quote_data['regularMarketChangePercent'])
        except:
            return "N/A"
    
    # Returns the stock's bid price, N/A for not available
    def bid(self):
        try:
            return self.quote_data['bid']
        except:
            return "N/A"
    
    # Returns the stock's ask price, N/A for not available
    def ask(self):
        try:
            return self.quote_data['ask']
        except:
            return "N/A"
    
    # Returns the stock's highest price in the day, N/A for not available
    def high(self):
        try:
            return self.quote_data['regularMarketDayHigh']
        except:
            return "N/A"

    # Returns the stock's lowest price in the day, N/A for not available
    def low(self):
        try:
            return self.quote_data['regularMarketDayLow']
        except:
            return "N/A"

    # Returns the stock's price range in the day, N/A for not available
    def range(self):
        try:
            return self.quote_data['regularMarketDayRange']
        except:
            return "N/A"

    # Return historical data for the stock, empty if none
    def historic(self, start, end, index, inter):
        try:
            return get_data(ticker=self.symbol, start_date=start, end_date=end, index_as_date=index, interval=inter)
        except:
            return []
