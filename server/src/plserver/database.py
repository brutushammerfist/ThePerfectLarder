import mysql.connector
import json
import os

class Database():
    def __init__(self):
        self.connector = mysql.connector.connect(
            host = "localhost",
            user = "test",
            passwd = "test",
            database = os.environ['DATABASE_NAME']
        )
        self.cursor = self.connector.cursor()
        
    def createAccount(self):
        pass

    def login(self, username, password):
        sql = "SELECT username, password FROM Users WHERE username = %s"
        usr = (str(username), )
        self.cursor.execute(sql, usr)
        result = self.cursor.fetchall()

        if len(result) == 0:
            payload = {
                'data' : 'Invalid username.'
            }
            return (json.dumps(payload), 401)
        else:
            data = result[0]
            if password == data[1]:
                payload = {
                    'data' : 'Successful login.'
                }
                return (json.dumps(payload), 200)
            else:
                payload = {
                    'data' : 'Incorrect password.'
                }
                return (json.dumps(payload), 401)

    def addItem(self, content):
        sql = "SELECT (inventoryID) FROM Users WHERE userID = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        inventoryID = result[0][0]

        sql = "INSERT INTO Items (inventoryID, itemname, expiration, quantity, measurement, location) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (inventoryID, content['itemname'], content['expDate'], content['quantity'], content['measurement'], content['location'])
        self.cursor.execute(sql, val)
        result = self.commit()

        print(self.cursor.rowcount, "records inserted.")

        return (json.dumps(dict('data':'Item added.')), 200)
        
    def getItem(self, content):
        sql = "SELECT (inventoryID) FROM Users WHERE userID = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        inventoryID = result[0][0]

        sql = "SELECT (itemname, expiration, quantity, measurement, location) FROM Items WHERE inventoryID = %s"
        val = (inventoryID, )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        for i in result:
            if result[i][0] == content['name']:
                return (json.dumps(dict(itemname=result[i][0], expDate=result[i][1], quantity=result[i][2], measurement=result[i][3], location=result[i][4])), 200)

    def delItem(self):
        pass

    def getInventory(self):
        sql = "SELECT (inventoryID) FROM Users WHERE userID = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        inventoryID = result[0][0]

        sql = "SELECT (useID, itemname, expiration, quantity, measurement, location) FROM Items WHERE inventoryID = %s"
        val = (inventoryID, )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        temp = []
        for i in result:
            temp.append(dict(useID=result[i][0], itemname=result[i][1], expDate=result[i][2], quantity=result[i][3], measurement=result[i][4], location=result[i][5]))

        payload = {
            'data' : temp
        }

        return (json.dumps(payload), 200)

    def searchItem(self):
        pass
