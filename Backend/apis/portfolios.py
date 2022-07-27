import re
from flask import Flask, render_template, request, make_response, session, current_app as app, url_for, send_file, redirect, jsonify
from flask_restx import Api, Resource, Namespace, fields, reqparse
import mysql.connector
from classes.portfolio import Portfolio
from classes.stock import Stock
from classes.user import User

import pandas as pd
import os
# Database connection set up
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database='watchdog'
)
cur = mydb.cursor(buffered=True)

# Namespace for the portfolios overview page
api = Namespace('portfolios', description='show users portfolios')

# API model for add_stock function
add_stock_model = api.model('add_stock', {
    'ticker' : fields.String(required=True, description='stock ticker'),
    'volume' : fields.Integer(required=True, description='purchase volume'),
    'Portfolio id' : fields.Integer(required=True, description='Id'),
    'price' : fields.Integer(required=False, description='purchase  price'),
    })
# API model for delete_stock function
delete_stock_model = api.model('delete_stock', {
    'ticker' : fields.String(required=True, description='stock ticker'),
    'Portfolio id' : fields.Integer(required=True, description='Id'),
    })

# Models for argument input for post methods
Newportfolio_model = api.model('Newportfolio', {
    'Portfolioname' : fields.String(required=True, description='username')
    })

# Default route for general overview
@api.route('')
class portfolios(Resource):
    # GET method
    # return names of all portfolios
    def get(self):
        # First, delete any files in /static/files (for space/security reasons)
        # This is from the use of uploaded files 
        dir = 'static/files'
        if os.path.exists(dir):
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

        # Check if signed in, AND your profile is in the database
        if 'profile' in session and 'db_user_id' in session['profile']:
            # register user to database if not yet registered.
            user_id = User.register_id(session['jwt_payload'])
            portfolio_list = Portfolio.portfolio_list(user_id) # returns a list of tuples, [(name, id),()..]
            
            # key = portfolio_id, val = [{stock_dict1}, {stock_dict2}..., portfolio_name]
            p = {}
            # portfolio[0] = name, portfolio[1] = id
            for portfolio in portfolio_list:
                # Retrieve stock information from method
                info, change, total = Portfolio.stocks_format(portfolio[1])

                # Get stock dictionarys from portfolio_stocks
                p[portfolio[1]] = Portfolio.portfolio_stocks(portfolio[1])

                # Then append change(profit/loss), append portfolio total, append name
                # convert to commas for the formatting
                p[portfolio[1]].append(convert_to_commas(change))
                p[portfolio[1]].append(convert_to_commas(total))
                p[portfolio[1]].append(portfolio[0]) 
            
            return make_response(render_template('portfolios.html', p = p, email = session['jwt_payload']['email'], num_p = len(portfolio_list)))
        
        # User must be logged in
        else:
            return {"Error" : "Log in to create see your Portfolios"}

    # POST method
    # Updates portfolios, based on the buttons pressed
    # Can handle deleted stocks and portfolios
    # Can handle creating portfolios or adding stocks to portfolios
    def post(self):
        # Check if user_id has been added to database
        if 'profile' in session and 'db_user_id' in session['profile']:
            user_id = User.register_id(session['jwt_payload'])
        
        # If POST receives a 'import portfolio' request
        if 'import_portfolio' in request.args.keys():
            
            # Step 1, load the html page for the guide and file upload
            if request.args['import_portfolio'] == '1':
                # First, delete any files in /static/files (for space/security reasons)
                # This is from the use of uploaded files 
                dir = 'static/files'
                if os.path.exists(dir):
                    for f in os.listdir(dir):
                        os.remove(os.path.join(dir, f))
                # Simply load the html page
                return make_response(render_template('import_portfolio_1.html'))

            # Step 2, save the file that was uploaded, then load the html page asking for name
            if request.args['import_portfolio'] == '2':
                # Receive file and save to our files database
                uploaded_file = request.files['myFile']
                file_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], uploaded_file.filename).replace("\\",'/')
                
                # If directory doesn't exist, make it
                dir = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
                if not os.path.exists(dir):
                    os.makedirs(dir)
                
                # Save to directory
                uploaded_file.save(file_path)

                # Render page asking for name
                return make_response(render_template('import_portfolio_2.html', file_path = file_path))

            # Step 3, use pandas to parse the csv file and then add to portfolio
            if request.args['import_portfolio'] == '3':
                try:
                    # Read the files that was saved
                    file_path = request.args['file_path']
                    name = request.form['name']
                    col_names = ['stock_code', 'purchase_price', 'volume']

                    # Error if files invalid
                    csv_data = pd.read_csv(file_path, names=col_names, header=None)
                    
                    # Create portfolio object
                    Portfolio.create_portfolio(user_id, name)
                    portfolio_id = Portfolio.get_id(name)
                    stocks = []

                    # Add to portfolio for each row in csv
                    # First row is headers
                    for i, row in csv_data.iterrows():
                        # if not first row
                        if i != 0:
                            Portfolio.add_to_portfolio(portfolio_id, row['stock_code'], row['volume'], row['purchase_price'])
                # Error if invalid file
                except:
                    return {"Error": "Invalid File"}, 404

        # If POST receives a 'delete' in request
        if 'delete' in request.args.keys():
            if request.args['delete'] == 'portfolio':
                # Delete Portfolio using method
                Portfolio.delete_portfolio(user_id, request.args['portfolio'])

        
        # Or, if there is a name, it must be creating new portfolio
        if 'name' in request.form:
            Portfolio.create_portfolio(user_id, request.form['name'])
        
        # Or, if there is a stock code, it must be adding to portfolio
        if 'code' in request.form:
            # Get portfolio information from html page            
            Portfolio.add_to_portfolio(request.args['portfolio'], request.form['code'], request.form['num'], request.form['price'])
            port_id = request.args['portfolio']
            port_name = request.args['name']
            portfo = Portfolio.portfolio_stocks(port_id)
            return make_response(render_template('portfolio_page.html', portfolio = portfo, port_id = port_id, name = port_name, email = session['jwt_payload']['email']))


        # If there is a 'page', it must be directing to specific page
        if 'page' in request.args.keys():
            # Get portfolio information from html page
            port_id = request.args['portfolio']
            port_name = request.args['name']
            portfo = Portfolio.portfolio_stocks(port_id)
            return make_response(render_template('portfolio_page.html', portfolio = portfo, port_id = port_id, name = port_name, email = session['jwt_payload']['email']))

        portfolio_list = Portfolio.portfolio_list(user_id) # returns a list of tuples, [(name, id),()..]
        p = {} # p is dictionary of stocks
        for portfolio in portfolio_list:
                # append data to the tuple for homepage
                info, change, total = Portfolio.stocks_format(portfolio[1])
                p[portfolio[1]] = Portfolio.portfolio_stocks(portfolio[1])
                p[portfolio[1]].append(convert_to_commas(change))
                p[portfolio[1]].append(convert_to_commas(total))
                p[portfolio[1]].append(portfolio[0])

        return make_response(render_template('portfolios.html', p = p, email = session['jwt_payload']['email'], num_p = len(portfolio_list)))


# Namespace for downloading the csv file that was uploaded
@api.route('/download')
class download(Resource):
    def get(self):
        # Uses the args that were pass from html
        try:
            # The ID for the exported portfolio 
            portfolio_id = request.args['portfolio']
            stocks = Portfolio.portfolio_stocks(portfolio_id)
            portfolio_dict = {
                            'stock_code': [],
                            'purchase_price': [],
                            'volume': []
                        }

            # Attach the stock info to the portfolio dictionary
            for stock in stocks:
                portfolio_dict['stock_code'].append(stock[0])
                portfolio_dict['purchase_price'].append(stock[2])
                portfolio_dict['volume'].append(stock[1])
            
            # Create the proper csv then user downloads as attachment
            df = pd.DataFrame(portfolio_dict)
            df.to_csv('static/files/{}_export.csv'.format(Portfolio.get_name(portfolio_id)), index=False)
            fp = os.path.join(os.getcwd(), 'static/files/{}_export.csv'.format(Portfolio.get_name(portfolio_id)))
            return send_file(fp, as_attachment=True)
        
        # For people that use this namespace incorrectly
        except:
            return redirect('/portfolios')

# 'Fake' namespace for returning a portfolio ID or 'False'
@api.route('/check-name')
class check_name(Resource):
    def get(self):
        # If Portfolio.get() works, there will be no error
        try:
            result = Portfolio.get_id(request.args['name'])
            return(result)
        
        # Error implies that this name is unique
        except TypeError:
            return("False")
            
        # Users trying to use this namespace incorrectly
        except:
            return redirect('/portfolios')

# Helper Function
# Convert values to commas, unless N/A
def convert_to_commas(attribute):
    if not isinstance(attribute, str):
        return "{:,}".format(round(attribute,2))
    else:
        return "N/A"


# Show information for each stock in selected portfolio
@api.route('/<portfolio_id>')
class portfolio_id(Resource): 

    def get(self, portfolio_id):
        if 'profile' in session and 'db_user_id' in session['profile']:
            #currency = "AUD"
            stocks = Portfolio.stocks_format(portfolio_id)
            port_name = Portfolio.get_name(portfolio_id)
            portfoFormat, change, total_now = Portfolio.stocks_format(portfolio_id)

            change = convert_to_commas(change)
            total_now = convert_to_commas(total_now)

            return make_response(render_template('portfolio_id_page.html', name = port_name, email = session['jwt_payload']['email'], port_id=portfolio_id, portfolio2=portfoFormat, total = total_now, pl=change))

        else:
            return {"Error" : "Log in to create a Portfolio"}

    def post(self, portfolio_id):
        # If delete button is clicked on portfolio, the stock will be removed from database 
        if 'delete' in request.args and request.args['delete'] == 'stock':
            Portfolio.remove_from_portfolio(request.args['portfolio'], request.args['stock'].upper())
            port_name = request.args['name']
            portfoFormat, change, total_now = Portfolio.stocks_format(portfolio_id)
            change = convert_to_commas(change)
            total_now = convert_to_commas(total_now)

            return make_response(render_template('portfolio_id_page.html', name = port_name, email = session['jwt_payload']['email'], port_id=portfolio_id, portfolio2=portfoFormat, total = total_now, pl=change))

        # if code is in the post request, the given input stock will be added.    
        if 'code' in request.form:
            # adds the input stock to the portfolio
            Portfolio.add_to_portfolio(portfolio_id, request.form['code'].upper(), request.form['num'], request.form['price'])
            port_name = request.args['name']
            # gets stock information for the updated portfolio
            portfoFormat, change, total_now = Portfolio.stocks_format(portfolio_id)
            change = convert_to_commas(change)
            total_now = convert_to_commas(total_now)

            # redirects back to portfolios page
            return make_response(render_template('portfolio_id_page.html', name = port_name, email = session['jwt_payload']['email'], port_id=portfolio_id, portfolio2=portfoFormat, total = total_now, pl=change))