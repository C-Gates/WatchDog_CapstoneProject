from flask import Flask, render_template, request, make_response
from flask_restx import Api, Resource, Namespace, fields, reqparse
from fuzzywuzzy import fuzz
import mysql.connector

# Database connection set up
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='watchdog'
)
cur = mydb.cursor(buffered=True)

# Namespace for the results page of taskbar search
api = Namespace('stock_results', description='show results for given search term')

# Default route for stock results.
@api.route('', methods = ['GET', 'POST'])
class stock_search(Resource):
    # GET Method
    # Basic results for page.
    def get(self): 
        
        # What was typed, convert to uppercase for consistency
        text = request.args.get('stock_search').upper()

        # For each row in stocks table,
        # get fuzzy ratio
        # Add to dictionary if 75+ 
        # (for now, unless I find how to do pages)
        scores = {} # key = ID, val = ratio
        try:
            # query for stocks
            cur.execute("SELECT * FROM stocks;")
            mydb.commit()
            
            # Each row = (ID, stock_code, NAME)
            rows = cur.fetchall()
            for stock in rows:
                # Assign a ratio based on similarity
                # Fuzzy Matching
                # Compares the string to the code and name
                ratio = max([fuzz.ratio(stock[1].upper(), text), fuzz.partial_ratio(stock[2].upper(), text)])
                if ratio >= 75: # 75 seems to be great
                    scores[stock[0]] = ratio

        except mysql.connector.errors.IntegrityError:
            return {"Error": "mySQL database error"}
        # Handle random errors
        except Exception as E:
            return {"Error": "{}".format(E)}

        # Sort dictionary based on similarity score.
        scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))

        # Final dictionary of results
        results = {}
        # How many results to display
        N = len(scores)
        if N > 10:
            N = 10
        
        # Display all the results 
        for x in range(N):
            key = list(scores.keys())[x]
            results[key] = scores[key]

        # Voila
        try:
            return make_response(render_template('search.html', results = results))
        except Exception as E:
            return "k, something is wrong. -> {}".format(E)
        