import mysql.connector
import json
import os

from plserver import app

class Database():
    def __init__(self):
        self.connector = mysql.connector.connect(
            host = "localhost",
            user = "test",
            passwd = "test",
            database = os.environ['DATABASE_NAME']
        )
        self.cursor = self.connector.cursor()
        
    def login(self, username, password):
        self.cursor.execute("SELECT username, password FROM Users WHERE username = %s", (username, ))
        result = self.cursor.fetchall()
        
        if len(result) == 0:
            payload = {
                'data' : 'Invalid username.'
            }
	    return json.dumps(payload), 401
        else:
            if password == result['password']:
                payload = {
                    'data' : 'Successful login.'
                }
		return json.dumps(payload), 200
            else:
                payload = {
                    'data' : 'Incorrect password.'
                }
		return json.dumps(payload), 401            
   
    def addItem(self):
        pass
    
    def delItem(self):
        pass
    
    def getInventory(self):
        pass
