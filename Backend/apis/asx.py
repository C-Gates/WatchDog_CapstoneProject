from flask import Flask, render_template, request, make_response, redirect, session
from flask_restx import Api, Resource, Namespace, fields, reqparse
import mysql.connector
from classes.stock import Stock
from classes.watchlist import Watchlist
from classes.portfolio import Portfolio

# Namespace for all ASX stocks.
api = Namespace('ASX', description='show summary information of a given stock for ASX')

# /<symbol>, Stock related page
@api.route('/<symbol>')
class stock_summary(Resource):
    # GET method
    # This returns the stock information page
    def get(self, symbol):
        # Get list of portfolios for the stock page, if logged in
        # This will allow stocks to be added to portfolios.
        # If not logged in, portfolios is None
        portfolios = None
        logged_in = None
        if session:
            portfolios = Portfolio.portfolio_list(session['profile']['db_user_id'])
            logged_in = True
        
        # Error handling for unknown stocks.
        try:
            tmp = Stock(symbol + ".AX")
        except IndexError:
            return {"Error": "Stock does not exist in our database."}, 404

        # Convert to comma for large numbers (e.g. 1000000 -> 1,000,000)
        market_cap = convert_to_commas(tmp.market_cap())
        volume = convert_to_commas(tmp.volume())
        open = convert_to_commas(tmp.open())
        close = convert_to_commas(tmp.close())
        price = convert_to_commas(tmp.price())

        return make_response(render_template('stock.html', name = tmp.name(), code = tmp.code().replace(".AX","").upper(), 
                                                            portfolios = portfolios, market = tmp.market(),
                                                            close = close, open = open, price = price,
                                                            volume = volume, market_cap = market_cap, 
                                                            currency = tmp.currency(), session = logged_in))
    # POST method
    # This handles all buttons on the stock page
    def post(self, symbol):
        # Handles the adding to portfolio
        if request.args['add'] == 'portfolio':
            # request.args['portfolios'] returns the name, NOT id.
            name = request.form['portfolio']

            # Search through user's portfolios for portfolio name
            user_id = session['profile']['db_user_id']
            for p in Portfolio.portfolio_list(user_id):
                if p[0] == name:
                    id = p[1]
            # Add to portfolio, then redirect to the page. Add ".AX" for asx stock
            Portfolio.add_to_portfolio(id, symbol.upper() + ".AX", request.form['num'], request.form['price'])
            return redirect('/portfolios/{}'.format(Portfolio.get_id(name)))
        
        # Handles the adding to watchlist, then redirect to the page.
        if request.args['add'] == 'watchlist':
            Watchlist.add_to_watch_list(session['profile']['db_user_id'], symbol.upper() + ".AX")
            return redirect('/watchlist')

# Helper Function
# Convert values to commas, unless N/A or any string
def convert_to_commas(attribute):
    if not isinstance(attribute, str):
        return "{:,}".format(round(attribute,2))
    else:
        return "N/A"




