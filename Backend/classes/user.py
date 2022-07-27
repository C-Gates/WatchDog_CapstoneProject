from flask import Flask, render_template, request, make_response
import mysql.connector

# Setup database connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="watchdog"
)
cur = mydb.cursor(buffered=True)

class User():
    # Registers the user to the local mySQL database and return user_id
    # OR returns the user_id of found user
    def register_id(data):
        # Password and username check
        # Find the users associated with the data argument
        cur.execute("SELECT user_id FROM users WHERE user_name=%s and email=%s", (data['nickname'], data['email']))
        mydb.commit()
        user_id = cur.fetchone()
        
        # If no users found, register one.
        if user_id == None:
          # Create user in database, then select them
          cur.execute("INSERT INTO users (user_name, email) VALUES (%s, %s)", (data['nickname'], data['email']))
          mydb.commit()
          cur.execute("SELECT * FROM users WHERE user_name=%s and email=%s", (data['nickname'], data['email']))
          mydb.commit()
          user_id  = cur.fetchone()
          
          # user_id should consist of the tuple of user
          if user_id is not None:
            return user_id[0]
          # Something has gone horribly wrong if this doesn't happen
          else:
            print('ERROR: no user id found!')
            return None
        
        # Else, return the user_id of found user
        else:
          return user_id[0]


