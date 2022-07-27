from flask import Flask, session, make_response, render_template, request, redirect, jsonify
from flask_restx import Api, Resource, Namespace, fields, reqparse
from classes.watchlist import Watchlist
from classes.stock import Stock
from classes.user import User

# Namespace for watchlist 
api = Namespace('watchlist', description='show user watch list')


#       Models for argument input for post methods 
add_watch_stock_model = api.model('add_watch_stock', {
    'ticker' : fields.String(required=True, description='stock ticker'),
    })

add_view = api.model('add_view', {
    'view_detail1' : fields.String(required=True),
    'view_detail2' : fields.String,
    'view_detail3' : fields.String
    })

@api.route('')
class watch_list(Resource):

    def get(self):
        # Check user is logged in
        if 'profile' in session and 'db_user_id' in session['profile']:
            user_id = User.register_id(session['jwt_payload'])
            session['profile']['db_user_id'] = user_id 
            email = session['jwt_payload']['email']

            stock_info_list = Watchlist.get_watch_list(user_id)
            
            # Create column headings for table
            details = ""
            if len(stock_info_list) >= 1:
                for key in stock_info_list[0]:
                    details = details + key + ","

            # Get stock data for weekly graph
            histdates, histvals = Watchlist.watch_list_historical(user_id, '1w')

            # Get all user views
            views = Watchlist.get_views(user_id)

            return make_response(render_template('watchlist.html', stock_info_list = stock_info_list, email = email, historyX=histdates, historyY=histvals, details=details[:-1], stock_info_list2=stock_info_list, views=views))

        else:
            return {"Error" : "Log in to see your Watch List"}

    def post(self):
        # Check if user_id has been added to database
        if 'profile' in session and 'db_user_id' in session['profile']:
            user_id = User.register_id(session['jwt_payload'])
            session['profile']['db_user_id'] = user_id 

            # If post request has delete key, must be deleting
            if "delete" in request.args:
                if request.args["symbol"] is None:
                    return
                Watchlist.delete_from_watch_list(session['profile']['db_user_id'], request.args["symbol"])
            
            # Else, it must be adding a stock
            else:
                if request.form["stock"] ==  "":
                    return redirect('/watchlist')
                
                # Call add_to_watch_list method
                Watchlist.add_to_watch_list(session['profile']['db_user_id'], request.form["stock"])
            
            return redirect('/watchlist')

        else:
            return {"Error" : "Log in to see your Watch List"}


@api.route('/history/<period>')
class watch_list(Resource):

    def get(self, period):
        
        # If logged in 
        if 'profile' in session and 'db_user_id' in session['profile']:
            # Get user_id
            user_id = User.register_id(session['jwt_payload'])
            
            # Get historical data for the graph
            session['profile']['db_user_id'] = user_id 
            histdates, histvals = Watchlist.watch_list_historical(user_id, period)
            return make_response(jsonify({"histdates" : histdates, "histvals" : histvals}), 200)

        else:
            return {"Error" : "Log in to see your Watch List"}

# Namespace for create view
@api.route('/create_view')
class watch_list(Resource):
    #@requires_auth
    def post(self):

        details = request.get_json()

        if 'profile' in session and 'db_user_id' in session['profile']:
            user_id = User.register_id(session['jwt_payload'])
            session['profile']['db_user_id'] = user_id 
            
            # returns true if user has not exceeded view number
            result = Watchlist.create_view(user_id, details["view_name"], details["details"])

            # if user can make another view
            if result == True:
                new_view = Watchlist.get_view(user_id, details['view_name'])
                return make_response(jsonify({"message" : "Success"}), 200)
            else:
                return make_response(jsonify({"message" : "Max views reached"}), 200)
 

        else:
            return {"Error" : "Log in to see your Watch List"}

# Return stock information for selected view
@api.route('/get_view/<view_name>')
class watch_list(Resource):

    def get(self, view_name):

        details = request.get_json()
        # Check user is logged in
        if 'profile' in session and 'db_user_id' in session['profile']:
            user_id = User.register_id(session['jwt_payload'])
            session['profile']['db_user_id'] = user_id 

            stock_info_list = Watchlist.get_view(user_id, view_name)

            # Generate string of stock data to pass to javascript table function
            details = ""
            if len(stock_info_list) >= 1:
                for key in stock_info_list[0]:
                    details = details + key + ","

 
            return make_response(jsonify({"columns":details[:-1], "rows":stock_info_list}), 200)

        else:
            return {"Error" : "Log in to see your Watch List"}
        
# Delete watchlist view
@api.route('/delete_view')
class watch_list(Resource):
    def post(self):
        if 'profile' in session and 'db_user_id' in session['profile']:
            user_id = User.register_id(session['jwt_payload'])
            session['profile']['db_user_id'] = user_id 

            view_name = request.get_json()
            Watchlist.delete_view(user_id, view_name['name'])

            return 
            

        else:
            return {"Error" : "Log in to see your Watch List"}
