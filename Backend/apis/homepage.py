from flask import Flask, render_template, request, make_response, session, jsonify
#from flask_mysqldb import MySQL
from flask_restx import Api, Resource, Namespace, fields, reqparse
import mysql.connector
from classes.homepage import Homepage
from classes.watchlist import Watchlist

api = Namespace('homepage', description='show homepage')

#       Models for argument input for post methods 
register_model = api.model('register', {
    'username' : fields.String(required=True, description='username'),
    'email' : fields.String(required=True, description='email'),
    'password' : fields.String(required=True, description='password')
    })


@api.route('')
class homepage(Resource):
    def get(self):
        highestMoving = Homepage.highest_moving()
        pass

@api.route('/watchlist_sum')
class watch_list_sum(Resource):
    def get(self):
      if 'db_user_id' in session['profile']:
          user_id = session['profile']['db_user_id']
          watchlist_sum = Watchlist.watch_list_summary(user_id)
          return {"watch_list_stocks" : watchlist_sum}, 200
      else:
          return {"Message" : "Log in to see your Watch List"}

# Call methods for homepage
@api.route('/highestNas')
class highestNas(Resource):
    def get(self):
        movers = Homepage.highest_moving_nasdaq()
        return make_response(jsonify(movers))

@api.route('/highestAsx')
class highestAsx(Resource):
    def get(self):
        movers = Homepage.highest_moving_asx()
        return make_response(jsonify(movers))

@api.route('/activeNas')
class activeNas(Resource):
    def get(self):
        movers = Homepage.most_active_nasdaq()
        return make_response(jsonify(movers))

@api.route('/activeAsx')
class activeAsx(Resource):
    def get(self):
        movers = Homepage.most_active_asx()
        return make_response(jsonify(movers))
      


