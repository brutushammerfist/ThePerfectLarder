import mysql.connector

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
        
    def login(self):
        pass
    
    def addItem(self):
        pass
    
    def delItem(self):
        pass
    
    def getInventory(self):
        pass