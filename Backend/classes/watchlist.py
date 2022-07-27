from datetime import datetime, date, timedelta
import mysql.connector
from .stock import Stock
import requests
import MySQLdb
import time

# Database connection set up
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database='watchdog'
)
cur = mydb.cursor(buffered=True)

class Watchlist():
    # Adds stock to user's watchlist
    def add_to_watch_list(user_id, stock_code):
        # Select the user's watchlist in database
        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id=%s; ", (user_id,))
        mydb.commit()

        # It should return one
        try:
            watch_list_id = cur.fetchone()[0]
        # If not, something is very wrong
        except Exception as e:
            return False
        
        # Insert into watchlist in database
        try:
            tmp = Stock(stock_code)
            cur.execute("INSERT INTO watch_list_stocks (watch_list_id, add_date, stock_code) VALUES (%s, %s, %s)", (watch_list_id, str(datetime.now()), stock_code.upper()))
            mydb.commit()
        # For now, multiple keys
        except mysql.connector.errors.IntegrityError:
            return False
        except IndexError:
            return False
        return True

    # Returns user's watchlist
    def get_watch_list(user_id):
        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id=%s; ", (user_id,))
        mydb.commit()
        
        watch_list_id = cur.fetchone()[0]

        cur.execute("SELECT stock_code FROM watch_list_stocks WHERE watch_list_id=%s ORDER BY add_date;", (watch_list_id,))
        mydb.commit()
        watch_list_stocks = cur.fetchall()

        stock_info_list = []

        # Create list of dictionaries for information for each stock
        for stock_code in watch_list_stocks:
            
            stock = Stock(stock_code[0])
            stock_dict = {
                'name' : stock.name(),
                'code' : stock_code[0],
                'price' : stock.price(),
                'open' : stock.open(),
                'change' : stock.change(), 
                'change%' : stock.change_perc(),
                'high' : stock.high(),
                'low' : stock.low(),
                'volume' : str(stock.volume())[:-3] + "k",
                'market_cap' : str(stock.market_cap())[:-6] + "m",
                'currency' : stock.currency()
            }
            stock_info_list.append(stock_dict)
            
        
        return stock_info_list

    # Remove stock from watch list
    def delete_from_watch_list(user_id, stock_code):

        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id=%s; ", (user_id,))
        mydb.commit()
        try:
            watch_list_id = cur.fetchone()[0]
        except Exception as e:
            print(e)
        cur.execute("DELETE FROM watch_list_stocks WHERE stock_code=%s AND watch_list_id=%s;", (stock_code, watch_list_id))
        mydb.commit()
        return

    #  FOR HOMEPAGE : Return short summary of watch list stocks to be displayed on homepage
    def watch_list_summary(user_id):

        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id=%s; ", (user_id,))
        mydb.commit()
        watch_list_id = cur.fetchone()[0]

        cur.execute("SELECT stock_code FROM watch_list_stocks WHERE watch_list_id=%s ORDER BY add_date;", (watch_list_id,))
        mydb.commit()
        watch_list_stocks = cur.fetchall()

        stock_info_list = []

        for stock_code in watch_list_stocks:
            stock = Stock(stock_code[0])

            stock_dict = {
                "code" : stock_code[0],
                "price" : '$' + str(stock.price()),
                "changep" : str(stock.change_perc())
            }
            stock_info_list.append(stock_dict)
        
        return stock_info_list

    # FOR GRAPH : Return historical prices to calculate total for weekly / monthly / yearly total summary
    def watch_list_historical(user_id, length):
        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id=%s; ", (user_id,))
        mydb.commit()
        watch_list_id = cur.fetchone()[0]

        cur.execute("SELECT stock_code FROM watch_list_stocks WHERE watch_list_id=%s ORDER BY add_date;", (watch_list_id,))
        mydb.commit()
        watch_list_stocks = cur.fetchall()

        # Change length of time period for graph
        # Change interval data is collected by in historical functions
        if length == '1w':
            end = 8
            interval = '1d'
        elif length == '1m':
            end = 31
            interval = '1d'
        elif length == '1y':
            end = 366
            interval = '1wk'
        else:
            end = 8
            interval = '1d'

        dict = {}

        # Generate keys for dates that data is being collected for -> graph X axis titles
        tod = date.today() - timedelta(days=1)
        first = tod
        for x in range(1,end):
            d = timedelta(days = x)
            dt = tod - d
            dict[str(dt)] = 0
        last = dt

        # Calculate daily total for all watch list stocks
        for stock_code in watch_list_stocks:
            s = Stock(stock_code[0])
            data = s.historic(last, first, 'True', interval)

            for item in dict:
                try:
                    dict[item] = dict[item] + float(data['close'][item])
                except Exception as e:
                    pass

        historyX = ""
        historyY = ""
        for key in dict:
            if length == '1y':
                if dict[key] > 0:
                    historyX = str(key) + ", " + historyX 
                    historyY = str(dict[key]) + ", " + historyY
            else:
                historyX = str(key) + ", " + historyX 
                historyY = str(dict[key]) + ", " + historyY

        return historyX[:-2], historyY[:-2]

    # Create view for displaying watch list stocks
    def create_view(user_id, title, view_list):
        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id=%s; ", (user_id,))
        mydb.commit()
        watch_list_id = cur.fetchone()[0]

        # Check user hasnot exceeded maximum views
        cur.execute("SELECT title FROM watch_list_views WHERE user_id=%s; ", (user_id,))
        mydb.commit()
        watch_list_views = cur.fetchall()
        if len(watch_list_views) > 5:
            return False

        details = ""
        for item in view_list:
            details = details + item + ","

        cur.execute("INSERT INTO watch_list_VIEWS (user_id, watch_list_id, title, details) VALUES (%s, %s, %s, %s); ", (user_id, watch_list_id, title, details[:-1]))
        mydb.commit()

        return True

    # List of all user created views
    def get_views(user_id):
        cur.execute("SELECT title FROM watch_list_views WHERE user_id=%s; ", (user_id,))
        mydb.commit()
        watch_list_views = cur.fetchall()

        views_list = []
        for item in watch_list_views:
            views_list.append(item[0])

        return views_list

    # Get details in user created view to generate stock table
    def get_view(user_id, title):
        cur.execute("SELECT * FROM watch_list_views WHERE user_id=%s and title=%s; ", (user_id,title))
        mydb.commit()
        watch_list_view = cur.fetchone()

        # Get stock details defined by user view
        view = {"title" : watch_list_view[2], "details" : watch_list_view[3]}
        view_list = view['details'].split(',')

        # Get watchlist id
        cur.execute("SELECT watch_list_id FROM watch_lists WHERE user_id=%s; ", (user_id,))
        mydb.commit()
        watch_list_id = cur.fetchone()[0]

        # get watchlist stocks
        cur.execute("SELECT stock_code FROM watch_list_stocks WHERE watch_list_id=%s ORDER BY add_date;", (watch_list_id,))
        mydb.commit()
        watch_list_stocks = cur.fetchall()

        stock_info_list = []

        # Generate string of stock details defined by the view, to pass to javascript table function
        for stock_code in watch_list_stocks:

            stock_dict = {}
            stock = Stock(stock_code[0])
            # For each detail in defined view, evaluate that function and add to string
            for item in view_list:
                try:
                    stock_dict[item] = eval('stock.' + item + '()')
                except:
                    stock_dict[item] = ""

            stock_info_list.append(stock_dict)

        return stock_info_list

    # Delete user view
    def delete_view(user_id, view_name):
        cur = mydb.cursor(buffered=True)

        cur.execute("DELETE FROM watch_list_views WHERE user_id=%s and title=%s; ", (user_id,view_name))
        mydb.commit()
        return

