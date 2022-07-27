from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import mysql.connector
from classes.news import News
from classes.stock import Stock

sgAPIKey = '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'

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database='watchdog'
)
cur = mydb.cursor(buffered=True)
class Email():
        #function to unsubscribe user from all emails
    def unsubscribe(email):
        #get loggedin user details
        cur.execute("SELECT user_id FROM watchdog.users WHERE email=%s;", (email,))
        mydb.commit()
        try:
            user_id = cur.fetchone()[0]
            cur.execute("DELETE FROM watchdog.user_email_subscriptions WHERE user_id=%s", (user_id,))
            mydb.commit()
        except:
            return {"error_message" : "Something is wrong!"}, 404

    #Function which adds a user's subscription to market summary to database
    def add_summary_email(email): 
        #get loggedin user details
        cur.execute("SELECT user_id FROM watchdog.users WHERE email=%s; ", (email,))
        mydb.commit()

        try:
            user_id = cur.fetchone()[0]
            
            cur.execute("SELECT email_id FROM user_email_subscriptions WHERE user_id=%s and email_type=4", (user_id,))
            mydb.commit()
            email_id = cur.fetchone()
            print(email_id)
            if email_id == None:
                cur.execute("INSERT INTO watchdog.user_email_subscriptions (user_id, email_address, email_type) VALUES (%s, %s, %s)", (user_id, email, 4,))
                mydb.commit()
        except:
            print("error with add_summary_email")

    #read if user has a market summary subscription and trigger function to send if they do
    def check_summary_email(email):
        #get loggedin user details
        cur.execute("SELECT user_id FROM watchdog.users WHERE email=%s;", (email,))
        mydb.commit()

        try: 
            user_id = cur.fetchone()[0]
            #select all user market summary alerts
            cur.execute("SELECT * FROM watchdog.user_email_subscriptions WHERE user_id=%s AND email_type = 4;", (user_id,))
            mydb.commit()
            alerts = cur.fetchall()
            for i in alerts:
                #send the emails
                Email.market_summary(i[2])
        except:
            print("error with check_summary_email")
            

    #function for sending a market summary email
    def market_summary(receiver):
        n = News()
        mylist = n.news_list('au', ['business'])
        #render the top 4 most relevant news articles in HTML format
        heading = '<h1> Watchdog Most Relevant Market News </h1>'
        article_1 = '<div style="height:200px; width=200px"><h2>' + mylist[0][0] + '</h2>' + '<p>' + mylist[0][1] + '</p>' + '<img style="height:10%; width=10%" src= "' + mylist[0][2] + '"/>' + '<p> Read More Here: ' + mylist[0][4] + '</p>'+ '</div>'
        article_2 = '<div style="height:200px; width=200px"><h2>' + mylist[1][0] + '</h2>' + '<p>' + mylist[1][1] + '</p>' + '<img style="height:10%; width=10%" src= "' + mylist[1][2] + '"/>' + '<p> Read More Here: ' + mylist[1][4] + '</p>'+ '</div>'
        article_3 = '<div style="height:200px; width=200px"><h2>' + mylist[2][0] + '</h2>' + '<p>' + mylist[2][1] + '</p>' + '<img style="height:10%; width=10%" src= "' + mylist[2][2] + '"/>' + '<p> Read More Here: ' + mylist[2][4] + '</p>'+ '</div>'
        article_4 = '<div style="height:200px; width=200px"><h2>' + mylist[3][0] + '</h2>' + '<p>' + mylist[3][1] + '</p>' + '<img style="height:10%; width=10%" src= "' + mylist[3][2] + '"/>' + '<p> Read More Here: ' + mylist[3][4] + '</p>'+ '</div>'
        #Email inputs
        message = Mail(
                from_email='Watchdog.stock@gmail.com',
                to_emails=receiver,
                subject='Watchdog Market Summary',
                html_content= heading + article_1 + article_2 + article_3 + article_4,
                )
        
        sg = SendGridAPIClient(sgAPIKey)
        response = sg.send(message)
        print("sending market summary")

    #read if user has a take alert subscription and trigger relevant function if they do
    def check_take_alert(email):
        #get loggedin user details
        cur.execute("SELECT user_id FROM watchdog.users WHERE email=%s;", (email,))
        mydb.commit()
        try:
            user_id = cur.fetchone()[0]
            #get all relevant alerts from db
            cur.execute("SELECT * FROM watchdog.user_email_subscriptions WHERE user_id=%s AND email_type = 1;", (user_id,))
            mydb.commit()
            alerts = cur.fetchall()
            for i in alerts:
                stock = Stock(i[4])
                Email.take_profit_email(i[2], stock.code(), i[6], stock.price())

        except:
            print("check_take error")

    #function when given a user email, stock and alert price create a subscription database object
    #for a take profit email
    def add_take_email(email, stock, alert_price): 
        #get loggedin user details
        cur.execute("SELECT user_id FROM watchdog.users WHERE email=%s; ", (email,))
        mydb.commit()
        try:
            user_id = cur.fetchone()[0]
            #get all relevant alerts from db
            cur.execute("INSERT INTO watchdog.user_email_subscriptions (user_id, email_address, email_type, stock_code, take_profit) VALUES (%s, %s, %s, %s, %s)", (user_id, email, 1, stock, alert_price,))
            mydb.commit()
        except:
            print("add_take error")

    #function which sends a take profit database email via sendgrid API given relevant info
    def take_profit_email(receiver, stock, alert_price, current_price):
        if (current_price >= alert_price):
            #Email body
            content = '<h3>Take Profit Alert from Watchdog</h3><br></<p>This is an alert to inform your your stock: ' + str(stock) + '<br> Has exceeded the take price of <b> $' + str(alert_price) + ' </b> <br>The current price is $' + str(current_price) + ' </p>'
            message = Mail(
                from_email='Watchdog.stock@gmail.com',
                to_emails=receiver,
                subject='Watchdog ' + stock + ' Take Profit Alert',
                html_content= content,
                )
            sg = SendGridAPIClient(sgAPIKey)
            response = sg.send(message)
            print("sending take profit email")
    #read if user has a stop loss alert subscription and trigger relevant function if they do
    def check_stop_alert(email):
        #get loggedin user details
        cur.execute("SELECT user_id FROM watchdog.users WHERE email=%s;", (email,))
        mydb.commit()

        try: 
            user_id = cur.fetchone()[0]
            #get all relevant alerts from db 
            cur.execute("SELECT * FROM watchdog.user_email_subscriptions WHERE user_id=%s AND email_type = 2;", (user_id,))
            mydb.commit()
            alerts = cur.fetchall()
            for i in alerts:
                stock = Stock(i[4])
                Email.stop_loss_email(i[2], stock.code(), i[5], stock.price())

        except:
            print("check_stop error")

    #function when given a user email, stock and alert price create a subscription database object
    #for a stop loss email
    def add_stop_email(email, stock, alert_price): 
        #get logged n user details
        cur.execute("SELECT user_id FROM watchdog.users WHERE email=%s; ", (email,))
        mydb.commit()
        try:
            user_id = cur.fetchone()[0]
            #insert alert into db
            cur.execute("INSERT INTO watchdog.user_email_subscriptions (user_id, email_address, email_type, stock_code, stop_loss) VALUES (%s, %s, %s, %s, %s)", (user_id, email, 2, stock, alert_price,))
            mydb.commit()

        except:
            print("add_stop_email error")

    #function which sends a stop loss database email via sendgrid API given relevant info
    def stop_loss_email(receiver, stock, alert_price, current_price):
        if (current_price <= alert_price):
            # email body
            content = '<h3>Stop Loss from Watchdog</h3><br></<p>This is an alert to inform your your stock: ' + str(stock) + '<br> Has exceeded the stop loss price of <b> $' + str(alert_price) + ' </b> <br>The current price is $' + str(current_price) + ' </p>'
            message = Mail(
                from_email='Watchdog.stock@gmail.com',
                to_emails=receiver,
                subject='Watchdog ' + stock + ' Stop Loss Alert',
                html_content= content,
                )
            #send email
            sg = SendGridAPIClient(sgAPIKey)
            response = sg.send(message)
            print("sending stop loss email")

    #function when triggered will check the database for any
    #percentage change email alerts for the logged in user
    #trigger the function to send if they do
    def check_percent_alert(email):
        #get loggedin user details
        cur.execute("SELECT user_id FROM watchdog.users WHERE email=%s;", (email,))
        mydb.commit()
        try:
            user_id = cur.fetchone()[0]
            #get relevant alert from db
            cur.execute("SELECT * FROM watchdog.user_email_subscriptions WHERE user_id=%s and email_type = 3;", (user_id,))
            mydb.commit()
            alerts = cur.fetchall()
            for i in alerts:
                stock = Stock(i[4])
                Email.percent_change(i[2], stock.code(), i[8], stock.price(), i[7])
        except:
            print("check_perecent error")

    #function which creates a percent email subscription alert database object 
    def add_percent_email(email, stock, percent_threshhold, purchase_price):
        #get logged in user info
        cur.execute("SELECT user_id FROM watchdog.users WHERE email=%s; ", (email,))
        mydb.commit()
        try:
            user_id = cur.fetchone()[0]
            #insert alert into db
            cur.execute("INSERT INTO watchdog.user_email_subscriptions (user_id, email_address, email_type, stock_code, percent_change, purchase_price) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, email, 3, stock, percent_threshhold, purchase_price,))
            mydb.commit()

        except:
            return {"error_message" : "Something is wrong!"}, 404

    #function which will send a percentage change email alert via sendgrid
    def percent_change(receiver, stock, purchase_price, current_price, percent_threshhold): 
        #calculate % change and if > threshhold send email 
        change = abs(float(((current_price-purchase_price) * 100) / purchase_price))
        if (change > percent_threshhold):
            #email body
            content = '<h3>Percentage Change Alert from Watchdog</h3><p>This is an alert to inform your your stock: ' + str(stock) + ' has reached the percentage change of <b> ' + str(change) + '% </b><br>Current Price: $' + str(current_price) + '<br> Purchase Price: $' + str(purchase_price) +'<br>This has exceeded your percentage change threshold of: ' + str(percent_threshhold) + '% </p>'
            message = Mail(
                from_email='Watchdog.stock@gmail.com',
                to_emails=receiver,
                subject='Watchdog ' + stock + ' Percentage Change Alert',
                html_content=content,
                )
            sg = SendGridAPIClient(sgAPIKey)
            response = sg.send(message)
            print("sending percent change email")
