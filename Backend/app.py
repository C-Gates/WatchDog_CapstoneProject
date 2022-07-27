from flask import Flask, render_template, make_response, jsonify, redirect, render_template, session, url_for, request, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv, find_dotenv
from flask_restx import Api, Resource, reqparse
from flask_mysqldb import MySQL

from jinja2 import Environment
import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from urllib.parse import urlencode

from apis.nasdaq import api as nasdaq
from apis.asx import api as asx
from apis.stock_results import api as stock_results
from apis.watchlist import api as watchlist
from apis.portfolios import api as portfolios
from apis.homepage import api as homepage

from classes.homepage import Homepage
from classes.news import News
from classes.user import User
from classes.email import Email
from classes.stock import Stock
from classes.watchlist import Watchlist
from classes.portfolio import Portfolio

app = Flask(__name__)


app.secret_key = 'abc'

# Upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static\\files')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'watchdog'

mysql = MySQL(app)
api = Api(app)
oauth = OAuth(app)


api.add_namespace(nasdaq)
api.add_namespace(asx)
api.add_namespace(stock_results)
api.add_namespace(watchlist)
api.add_namespace(homepage)
api.add_namespace(portfolios)

auth0 = oauth.register(
    'auth0',
    client_id='GYpxBUmG13VQkAsZOIbdaqZfzPHKFuNs',
    client_secret='OMbfh-hL1ozVDaeVNr2QTN2T8pG92v0F0EBJgQobnIEwqH8_rPebxMo_AMxj_IEm',
    api_base_url='https://dev-xnf4myxq.au.auth0.com',
    access_token_url='https://dev-xnf4myxq.au.auth0.com/oauth/token',
    authorize_url='https://dev-xnf4myxq.au.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

@api.route('/import_portfolio')
class import_portfolio(Resource):
    def get(self):
        return make_response(render_template('import_portfolio.html'))

@api.route('/check_emails')
class check_emails(Resource):
    def get(self):
        try:
            #grab user details
            user_info = session['jwt_payload']
            user_email = user_info['email']
            #check all alerts
            Email.check_summary_email(user_email)       
            Email.check_percent_alert(user_email)
            Email.check_stop_alert(user_email)
            Email.check_take_alert(user_email)
        except:
            print("check email error")
        return redirect('/home')
        
#route for the settings page
@api.route('/settings')
class settings(Resource):   
    def get(self):
        if 'profile' in session:
            return make_response(render_template('settings.html'))
    
        else:
            return {"Error" : "Log in to use Settings"}

    def post(self):
        if 'profile' in session:

            user_info = session['jwt_payload']
            user_email = user_info['email']
            if 'profile' in session and 'db_user_id' in session['profile']:
                    # register user to database if not yet registered.
                    user_id = User.register_id(session['jwt_payload'])

            #if user selected take profit email alert
            if (request.form['take_email'] == "true"): 
                try:
                    stock_name = request.form['stock_take']
                    price = float(request.form['price_take'])
                    stock_test = Stock(stock_name)
                    Email.add_take_email(user_email, stock_test.code(), price)
                except:
                    print("Error with take email")
            #if user selected stop loss email alert
            if (request.form['stop_email'] == "true"):
                try:
                    stock_name = request.form['stock_stop']
                    price = float(request.form['price_stop'])
                    stock_test = Stock(stock_name)
                    Email.add_stop_email(user_email, stock_test.code(), price)
                except:
                    print("Error with stop email")
            #if user selected percent change email alert
            if (request.form['percent_email'] == "true"):
                try:
                    stock_name = request.form['stock_percent']
                    threshhold = float(request.form['threshhold_percent'])
                    stock_test = Stock(stock_name)
                    purchase_price = float(request.form['price_percent'])
                    Email.add_percent_email(user_email,stock_test.code(),threshhold,purchase_price)
                except:
                    print("Error with percent email")
            #if user selected market summary email alert     
            if (request.form['summary_email'] == "true"):
                try:
                    Email.add_summary_email(user_email)   
                except:
                    print("Error with summary email")
                    
            return redirect('/settings')
        
        else:
            return {"Error" : "Log in to use Settings"}
@api.route('/unsubscribe')
class unsubscribe(Resource):
    def get(self):
        try:
            user_info = session['jwt_payload']
            user_email = user_info['email']
            #trigger unsubscribe function
            Email.unsubscribe(user_email)
        except:
            print("unsubscribe error")

        return redirect('/settings')
@api.route('/callback')
class callback(Resource):
    def get(self):
        # Handles response from token endpoint
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()
        db_user_id = User.register_id(userinfo)

        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture'],
            'db_user_id': str(db_user_id)
        }

        return redirect('/home')

# Namespace for login
@api.route('/login')
class login(Resource):
    def get(self):
        #redirect to auth0
           return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')

n = News() #temporary news object
@api.route('/home')
class home(Resource):
    def get(self):
        mylist = n.news_list('au')
        length = len(mylist)
        # If logged in
        if session:
            # register the user to the database, or return the user_id if already
            user_id = User.register_id(session['jwt_payload'])
            if 'profile' in session and 'db_user_id' in session['profile']:
                watch_list_sum = Watchlist.watch_list_summary(user_id)
                p = Portfolio.portfolio_list(user_id) # returns list of tuples e.g. [(p1_name, p1_id), (p2_name, p2_id)]
                for i in range(len(p)):
                    tmp, change, total_now = Portfolio.stocks_format(p[i][1])
                    p[i] = p[i] + (change, total_now)
                # news_list: for news slider
                # length: number of news articles (needed for slider.js)
                # wl_stocks: for watchlist summary
                # user: home displays differently depending on the user
                # portfolio_list: for portfolio summary
                return make_response(render_template('index.html', news_list=mylist, len=length, wl_stocks=watch_list_sum,
                                                            user=session['profile'], portfolio_list = p,
                                                            userinfo=json.dumps(session['jwt_payload'])))
        else:
            return make_response(render_template('index.html', news_list=mylist, len=length,
                                                            user="",
                                                            userinfo=""))

# A 'fake' namespace for checking if a stock exists
# Provides a return value of True or False, depending if the stock code exists
# Stock() will return error if stock not found.
@api.route('/check_stock')
class check_stock(Resource):
    def get(self):
        # Redirect users who should not be here
        if 'code' not in request.args.keys():
            redirect('/home')
        try:
            s = Stock(request.args['code'].upper())
        except:
            return "False"
        return "True"

@api.route('/portfolios')
class portfolios(Resource):
    def get(self):
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()
        User.register_id(userinfo)
        return make_response(render_template('portfolios.html'))

@api.route('/news', methods=["GET", "POST"])
class news(Resource):
    def get(self):
        mylist = n.news_list('us',['business'])
        #top_headlines removed (less calls for NewsAPI is faster)
        return make_response(render_template('news.html', context= mylist))

    def post(self):
        #pref is an dictionary of news categories e.g ({'finance','on'}, {'technology','on'})
        if 'pref' in request.form:
            preferences = list(request.form.keys())
            preferences.pop()
            mylist = n.news_list('us',preferences)
            return make_response(render_template('news.html', context= mylist))
        if 'search' in request.form: #search's last value is the search input
            stocks = list(request.form.values())
            stock = stocks.pop()
            return redirect(url_for('stock_news', stock=stock))

        news_id = list(request.form.keys())[0]
        art = n.find_article(int(news_id))
        desc = art.get_title() #article title
        content=art.get_content() #article content
        img=art.get_url() #image of news article (url format)
        link=art.get_link() #url to site where the article was taken from
        return redirect(url_for('article_page', id=news_id, desc=desc, content=content, img=img, link=link))
        

#article class is a brief summary of the article that links to the page where the article was taken from
@api.route('/article/<id>')
class article_page(Resource):
    def get(self, id):
        desc=request.args.get('desc') #article title
        content=request.args.get('content') #article contents
        img=request.args.get('img') #image of news article (url)
        link=request.args.get('link') #url to site where the article was taken from
        return make_response(render_template('article.html', desc=desc, content=content, img=img, link=link))

#news about a specific stock
s_news = News()
@api.route('/news/<stock>')
class stock_news(Resource):
    def get(self, stock):
        first = s_news.top_search(stock)
        list = s_news.stock_news_list(stock)
        return make_response(render_template('stock-news.html', context= list, top=first))

    def post(self, stock):
        news_id = list(request.form.keys())[0]
        art = s_news.find_article(int(news_id))
        desc = art.get_title()
        content=art.get_content()
        img=art.get_url()
        link=art.get_link()
                                            #id: int, desc: title str, content: str, img: url str, link: url str 
        return redirect(url_for('article_page', id=news_id, desc=desc, content=content, img=img, link=link))


@api.route('/logout')
class logout(Resource):
    def get(self):
        session.clear()
        #redirect to home
        params = {'returnTo': url_for('home', _external=True), 'client_id': 'GYpxBUmG13VQkAsZOIbdaqZfzPHKFuNs'}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))




if __name__ == '__main__':
    app.run(debug=True)
