from datetime import datetime, timedelta, date
import mysql.connector
from .stock import Stock

# connects to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database='watchdog'
)

#creates the cursors
cur = mydb.cursor(buffered=True)
cur2 = mydb.cursor(buffered=True)
class Portfolio():
    #gets portfolio id via name
    def get_id(portfolio_name):
        q = """SELECT portfolio_id FROM portfolios where name = %s;"""
        cur.execute(q, (portfolio_name,))
        mydb.commit()
        return cur.fetchone()[0]

    #gets portfolio name via id
    def get_name(portfolio_id):
        q = """SELECT name FROM portfolios where portfolio_id = %s;"""
        cur.execute(q, (portfolio_id,))
        mydb.commit()
        return cur.fetchone()[0]

    #The old create portfolio function (currently an operation in database is called upon portfolio creation)
    def create_portfolioOld(user_id, portfolio_name, portfolio_id):
        # count the number of current portfolios
        selectq = """SELECT count(portfolio_id) FROM watchdog.user_portfolios where user_id = %s;"""
        cur.execute(selectq, (user_id,))
        Profile_count = cur.fetchone()[0]
        
        if Profile_count < 11:
            cur.execute("INSERT INTO watchdog.portfolios (portfolio_id,name) VALUES (%s,%s);", (portfolio_id, portfolio_name))
            mydb.commit()
            selectq = """SELECT portfolio_id FROM watchdog.portfolios WHERE name = %s;"""
            cur.execute(selectq, (portfolio_name,))
            port_id = cur.fetchone()
            cur.execute("INSERT INTO watchdog.user_portfolios (portfolio_id,user_id) VALUES (%s,%s);", (port_id[0],user_id))
            mydb.commit()
            return 200
        else:
            error = "Maximum portfolios exceeded"
            return error

    #adds stock to portfolio
    def add_to_portfolio(portfolio_id, stock_code, volume, price):
        # check if stock exists
        try:
            s = Stock(stock_code)
        # Do nothing if it doesnt
        except:
            return
        
        try:  
            # Simply insert the stock into the portfolio in the database  
            cur.execute("INSERT INTO watchdog.portfolio_stocks (portfolio_id, purchase_date, stock_code, volume, purchase_price) VALUES (%s, %s, %s, %s, %s)", (portfolio_id, str(datetime.now()), stock_code, volume, price))
            mydb.commit()
        
        # If Duplicate Entry, update instead
        except mysql.connector.errors.IntegrityError:
            # Get current data of the stock in the portfolio
            q = """SELECT stock_code,volume,purchase_price,purchase_date FROM watchdog.portfolio_stocks WHERE portfolio_id = %s and stock_code = %s;"""
            cur.execute(q, (portfolio_id, stock_code,))
            mydb.commit()

            # cur.fetchone() contains tuple: (code, volume, purchase_price, date)
            tuple = cur.fetchone()

            # volume becomes a string when passed through the request.args
            new_volume = int(volume) + tuple[1]
            
            # if new_volume <= 0, just delete
            if new_volume <= 0:
                Portfolio.remove_from_portfolio(int(portfolio_id), stock_code)
                return

            # new average purchase price = (old_vol * old_purchase + new_vol * new_purchase) / total_vol
            avg_purchase_price = (tuple[1] * tuple[2] + int(volume) * int(price)) / new_volume
            cur.execute("UPDATE watchdog.portfolio_stocks SET volume = %s, purchase_price = %s WHERE portfolio_id = %s and stock_code = %s", (new_volume, avg_purchase_price, int(portfolio_id), stock_code))
            mydb.commit()
        return
    # reomves stock from portfolio
    def remove_from_portfolio(portfolio_id, stock_code):
        cur.execute("DELETE FROM watchdog.portfolio_stocks WHERE portfolio_id = %s AND stock_code = %s", (portfolio_id, stock_code))
        mydb.commit()
        return 200

    # gets the infromaiton of portfolio stock and returns a list of lists    
    def portfolio_stocks(portfolio_id):
        stocks = []
        mycursor = mydb.cursor()
        selectq = """SELECT stock_code,volume,purchase_price,purchase_date FROM watchdog.portfolio_stocks WHERE portfolio_id = %s;"""
        mycursor.execute(selectq ,(portfolio_id,))
        stocks = mycursor.fetchall()
       

        # converts stocks_list from a list of tuples to a list of lists       
        stocks_list = [list(elem) for elem in stocks]
        
        # adds the relevant infromation to the stock list 
        if len(stocks) == 0:
            return stocks
        else:
            for x in stocks_list:
                name = x[0]
                s = Stock(name)
                Market = s.market()
                Name = s.name()
                # 4 - Market
                x.append(Market)
                # 5 - Name
                x.append(Name)
            
                # Daily change
                try:
                    daily_change =  (s.change())                  
                    # 6 - Daily change
                    x.append(daily_change)
                except TypeError:
                    x.append("N/A")

                try:
                    # 7 - daily PNL amount
                    daily_PNL = round(daily_change * x[1],2)
                    x.append(daily_PNL)
                except TypeError:
                    x.append("N/A")

                try:
                    # 8 - daily change %
                    daily_change_p =  s.change_perc()
                    x.append(daily_change_p)
                except TypeError:
                    x.append("N/A")
                
                try:
                    # 9 - market cap
                    Market_cap = round(s.market_cap(),2)
                    x.append(Market_cap)
                except TypeError:
                    x.append("N/A")

                try:
                    # 10 - Market volume
                    Volume = round(s.volume(),2)
                    x.append(Volume)
                except TypeError:
                    x.append("N/A")

                try:
                    # 11 - price
                    price = round(s.price(),2)
                    x.append(price)
                except TypeError:
                    x.append("N/A")
            # to get the information stocklist[number] can be done!
            return stocks_list 

    # gets all the stock codes from a portfolio by portfolio id.
    def portfolio_stock_codes(portfolio_id):
        stocks = []
        mycursor = mydb.cursor()
        selectq = """SELECT stock_code FROM watchdog.portfolio_stocks WHERE portfolio_id = %s;"""
        mycursor.execute(selectq ,(portfolio_id,))
        stocks = mycursor.fetchall()
        return stocks 
        
    # gets the total value of all stocks recieved
    def portfolio_total(Stocks):
        sum = 0
        for x in Stocks:
            sum += x["Current price"]
        return sum

    # prepares stock information for portfolio page api
    def portfolio_stock_display(Stock_display_input, currency):
        
        # Get stock information from stock class
        Current_price = Stock.price(Stock(Stock_display_input[0]))
        Name = Stock_display_input[0]
        Volume = Stock_display_input[1]
        Purchase_price = Stock_display_input[2]
        Purchase_date = Stock_display_input[3].strftime("%Y:%m:%d")
        Total_investment = Purchase_price * Volume
        Total_current_value = Current_price * Volume

        Stock_display = {
            "Name": Name,
            "Volume": Volume,
            "Purchase Price": Purchase_price,
            "Purchase Date": Purchase_date,
            "Current price": Current_price,
            "Total investment": Total_investment,
            "Total current value": Total_current_value,
            "P&L": round(Total_current_value - Total_investment,2)
        }

        return Stock_display

    # creates a list of user portfolios.
    def portfolio_list(user_id):
        #mycursor = mydb.cursor()
        cur.execute("SELECT portfolio_id FROM watchdog.user_portfolios WHERE user_id = %s;", (user_id,))
        mydb.commit()
        portfolios = cur.fetchall()

        portfolio_list = []
        i = 0
        for portfolio in portfolios:
            cur.execute("SELECT name FROM watchdog.portfolios WHERE portfolio_id = %s;", (portfolio[0],))
            mydb.commit()
            portfolio_list.append(cur.fetchall()[0])
            portfolio_list[i] = portfolio_list[i] + (portfolio[0],)
            i += 1

        return portfolio_list
    # creates a portfolio with a name and connects to user id
    def create_portfolio(user_id, portfolio_name):
        selectq = """SELECT count(portfolio_id) FROM watchdog.user_portfolios where user_id = %s;"""
        cur.execute(selectq, (user_id,))
        Profile_count = cur.fetchone()[0]
        
        # checks if user has more than 10 portfolios
        if Profile_count < 11:
            try:
                cur.execute("CALL create_portfolio (%s, %s);", (user_id, portfolio_name))
                mydb.commit()
                return True
            except mysql.connector.errors.IntegrityError:
                return False

        else:
            error = "Maximum portfolios exceeded"
            return error



    # deletes portfolio and it's dependancies from database
    def delete_portfolio(user_id, portfolio_id):
        try:
            # Deletes record from junction table
            cur.execute("DELETE FROM portfolio_stocks WHERE portfolio_id=%s;", (portfolio_id,))
            mydb.commit()
            cur.execute("DELETE FROM user_portfolios WHERE user_id=%s AND portfolio_id=%s;", (user_id, portfolio_id,))
            mydb.commit()
            cur.execute("DELETE FROM portfolios WHERE portfolio_id=%s;", (portfolio_id,))
            mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

    # preprares stock for portfolio display
    def stocks_format(portfolio_id):
        mycursor = mydb.cursor()
        selectq = """SELECT stock_code,volume,purchase_price,purchase_date FROM watchdog.portfolio_stocks WHERE portfolio_id = %s;"""
        mycursor.execute(selectq ,(portfolio_id,))
        stocks = mycursor.fetchall()
        total_original = 0
        total_now = 0
        stock_info_list = []
        for stock in stocks:
            # Append stocks as needed
            try:
                s = Stock(stock[0])
                if not isinstance(s.price(), str):
                    total_now = total_now + (s.price()*stock[1])
                total_original = float(stock[1]) * float(stock[2])
                stockdict = {
                    "code" : stock[0],
                    "name" : s.name(),
                    "price" : s.price(),
                    "vol" : stock[1],
                    "purchase" : stock[2],
                    "market" : s.market(),
                    "change" : s.change(),
                    "changep" : s.change_perc()
                }
            
                # Handles N/A values for price, market_cap, volume
                if isinstance(s.price(), str):
                    stockdict["pnl"] = "N/A"
                else:
                    stockdict["pnl"] = "{:,}".format(round((s.price()-stock[2]) * stock[1],2))

                if isinstance(s.market_cap(), str):
                    stockdict["market_cap"] = "N/A"
                else:
                    stockdict["market_cap"] = "{:,}".format(s.market_cap())

                if isinstance(s.market_cap(), str):
                    stockdict["volume"] = "N/A"
                else:
                    stockdict["volume"] = "{:,}".format(s.volume())

                stock_info_list.append(stockdict)
            # Disregard the stock if there is an error
            except:
                pass
        change = total_now - total_original

        return stock_info_list, change, total_now