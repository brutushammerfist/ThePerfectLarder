import mysql.connector
import json

from plserver import app

class Database():
    def __init__(self):
        self.connector = mysql.connector.connect(
            host = "411orangef19-mgmt.cs.odu.edu",
            user = "test",
            passwd = "test",
            database = "testing"
        )
        self.cursor = self.connector.cursor()
        
    def login(self, username, password):
        self.cursor.execute(f'SELECT username, password FROM Users WHERE username ='{username}'')
        result = self.cursor.fetchone()
        
        if self.cursor.rowcount == 0:
            payload = {
                'data' : 'Invalid username.'
            }
        else:
            if password == result['password']:
                payload = {
                    'data' : 'Successful login.'
                }
            else:
                payload = {
                    'data' : 'Incorrect password.'
                }
            
        return json.dumps(payload)
    
    def addItem(self):
        pass
    
    def delItem(self):
        pass
    
    def getInventory(self):
        pass