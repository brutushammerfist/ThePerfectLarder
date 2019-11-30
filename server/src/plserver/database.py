from bs4 import BeautifulSoup
import scrape_schema_recipe
import mysql.connector
import datetime
import requests
import math
import json
import os
import collections
from email.policy import default

class Database():
    def __init__(self):
        self.connector = mysql.connector.connect(
            host = "localhost",
            user = "test",
            passwd = "test",
            database = os.environ['DATABASE_NAME']
        )
        self.cursor = self.connector.cursor()
        
    def ensureConnected(self):
        if not self.connector.is_connected():
            self.connector = mysql.connector.connect(
                host = "localhost",
                user = "test",
                passwd = "test",
                database = os.environ['DATABASE_NAME']
            )
            self.cursor = self.connector.cursor()

    def login(self, content):
        self.ensureConnected()
        sql = "SELECT id, username, password, metric, notifications, storageLocations FROM Users WHERE username = %s"
        usr = (str(content['username']), )
        self.cursor.execute(sql, usr)
        result = self.cursor.fetchall()

        if len(result) == 0:
            payload = {
                'data' : 'Invalid username.'
            }
            return (json.dumps(payload), 401)
        else:
            if content['password'] == result[0][2]:
                payload = {
                    'data' : 'Successful login.',
                    'userID' : result[0][0],
                    'measureType' : result[0][3],
                    'notifPref' : result[0][4],
                    'locations' : result[0][5]
                }
                return (json.dumps(payload), 200)
            else:
                payload = {
                    'data' : 'Incorrect password.'
                }
                return (json.dumps(payload), 401)

    def signUp(self,content):
        self.ensureConnected()
        # check if any user name or email address exist in the data base
            #if yes  
                #return 1 for name already in database
                #return 2 for email already in database
                #return 3 for name and email both in the database
            #if no
                #perform necessary operation to dump data in the database then
                #return 0 to confirm data successfully in database
        sql = "SELECT id FROM `Users` WHERE `Users`.`username` = %s"
        usrn = (str(content['username']),)
        self.cursor.execute(sql,usrn)
        result1 = self.cursor.fetchall()

        sqlTwo = "SELECT id FROM `Users` WHERE `Users`.`email` = %s"
        usre = (str(content['useremail']),)
        self.cursor.execute(sqlTwo,usre)
        result2 = self.cursor.fetchall()

        if len(result1) == 0 and len(result2) == 0:
            sql = "SELECT inventoryID FROM Users ORDER BY inventoryID DESC"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()

            if len(result) > 0:
                inventoryID = result[0][0] + 1
            else:
                inventoryID = 1

            storageLocations = {
                'locations' : ['Fridge', 'Freezer', 'Dry']
            }

            sqlInsert = "INSERT INTO Users (name, email, phone, username, password, inventoryID, storageLocations) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (content['name'], content['useremail'], content['phone'], content['username'], content['password'], inventoryID, json.dumps(storageLocations), )
            #inventoryID = result[0][0] + 1
            self.cursor.execute(sqlInsert, val)
            result = self.connector.commit()
            return (json.dumps(dict(data='0')), 200)
        elif(len(result1) != 0 and len(result2) != 0):
            return (json.dumps(dict(data='3')), 401)
        else:
            if(len(result1) != 0 ):
                return (json.dumps(dict(data='1')), 401)
            if(len(result2) != 0):
                return (json.dumps(dict(data='2')), 401)
                
    def addItem(self, content):
        self.ensureConnected()
        sql = "SELECT (inventoryID) FROM Users WHERE id = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        inventoryID = result[0][0]

        sql = "SELECT id, itemname, quantity, measurement, location FROM Items WHERE inventoryID = %s AND itemname = %s AND measurement = %s AND location = %s"
        val = (inventoryID, content['itemname'], content['measurement'], content['location'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        if content['expDate'] == "":
            sql = "SELECT expiration FROM ShelfLife WHERE name LIKE %s"
            val = ("%" + content['itemname'] + "%", )
            self.cursor.execute(sql, val)
            itemExpData = self.cursor.fetchall()

            if len(itemExpData) != 0:
                if content['location'] == 'Pantry':
                    if json.loads(itemExpData[0][0])['DOP_Pantry_Metric'] != None:
                        min = json.loads(itemExpData[0][0])['DOP_Pantry_Min']
                        metric = json.loads(itemExpData[0][0])['DOP_Pantry_Metric']
                        if metric.lower() == 'days':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=min)
                        elif metric.lower() == 'weeks':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 7))
                        elif metric.lower() == 'months':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 30))
                        elif metric.lower() == 'years':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 365))
                    elif json.loads(itemExpData[0][0])['Pantry_Metric'] != None:
                        min = json.loads(itemExpData[0][0])['Pantry_Min']
                        metric = json.loads(itemExpData[0][0])['Pantry_Metric']
                        if metric.lower() == 'days':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=min)
                        elif metric.lower() == 'weeks':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 7))
                        elif metric.lower() == 'months':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 30))
                        elif metric.lower() == 'years':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 365))
                elif content['location'] == 'Refrigerator':
                    if json.loads(itemExpData[0][0])['DOP_Refrigerate_Metric'] != None:
                        min = json.loads(itemExpData[0][0])['DOP_Refrigerate_Min']
                        metric = json.loads(itemExpData[0][0])['DOP_Refrigerate_Metric']
                        if metric.lower() == 'days':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=min)
                        elif metric.lower() == 'weeks':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 7))
                        elif metric.lower() == 'months':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 30))
                        elif metric.lower() == 'years':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 365))
                    elif json.loads(itemExpData[0][0])['Refrigerate_Metric'] != None:
                        min = json.loads(itemExpData[0][0])['Refrigerate_Min']
                        metric = json.loads(itemExpData[0][0])['Refrigerate_Metric']
                        if metric.lower() == 'days':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=min)
                        elif metric.lower() == 'weeks':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 7))
                        elif metric.lower() == 'months':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 30))
                        elif metric.lower() == 'years':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 365))
                elif content['location'] == 'Freezer':
                    if json.loads(itemExpData[0][0])['DOP_Freeze_Metric'] != None:
                        min = json.loads(itemExpData[0][0])['DOP_Freeze_Min']
                        metric = json.loads(itemExpData[0][0])['DOP_Freeze_Metric']
                        if metric.lower() == 'days':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=min)
                        elif metric.lower() == 'weeks':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 7))
                        elif metric.lower() == 'months':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 30))
                        elif metric.lower() == 'years':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 365))
                    elif json.loads(itemExpData[0][0])['Freeze_Metric'] != None:
                        min = json.loads(itemExpData[0][0])['Freeze_Min']
                        metric = json.loads(itemExpData[0][0])['Freeze_Metric']
                        if metric.lower() == 'days':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=min)
                        elif metric.lower() == 'weeks':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 7))
                        elif metric.lower() == 'months':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 30))
                        elif metric.lower() == 'years':
                            content['expDate'] = datetime.date.today() + datetime.timedelta(days=(min * 365))
            else:
                content['expDate'] = datetime.date.today() + datetime.timedelta(days=3)

        if len(result) == 0:
            useData = {
                "purchased" : [
                    {
                        "date" : datetime.datetime.now().strftime("%Y-%m-%d"),
                        "quantity" : content["quantity"]
                    }
                ],
                "purchasedTotal" : content["quantity"],
                "used" : [],
                "usedTotal" : 0,
                "wasted" : [],
                "wastedTotal" : 0
            }

            sql = "INSERT INTO FoodUse (itemname, measurement, `usage`) VALUES (%s, %s, %s)"
            val = (content['itemname'], content['measurement'], json.dumps(useData), )
            self.cursor.execute(sql, val)
            result = self.connector.commit()

            sql = "SELECT id FROM FoodUse ORDER BY id DESC;"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            useID = result[0][0]

            sql = "INSERT INTO Items (inventoryID, itemname, expiration, quantity, measurement, location, useID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (inventoryID, content['itemname'], content['expDate'], content['quantity'], content['measurement'], content['location'], useID, )
            self.cursor.execute(sql, val)
            result = self.connector.commit()
        else:
            itemID = result[0][0]

            sql = "UPDATE Items SET quantity = %s WHERE id = %s"
            val = ((float(content['quantity']) + float(result[0][2])), itemID, )
            self.cursor.execute(sql, val)
            result = self.connector.commit()

            sql = "SELECT useID FROM Items WHERE id = %s"
            val = (itemID, )
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
            useID = result[0][0]

            sql = "SELECT `usage` FROM FoodUse WHERE id = %s"
            val = (useID, )
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()

            purchased = {
                'date' : datetime.datetime.now().strftime("%Y-%m-%d"),
                'quantity' : content['quantity']
            }

            useData = json.loads(result[0][0])
            useData['purchased'].append(purchased)
            useData['purchasedTotal'] = float(useData['purchasedTotal']) + float(content['quantity'])

            sql = "UPDATE FoodUse SET `usage` = %s WHERE id = %s"
            val = (json.dumps(useData), useID, )
            self.cursor.execute(sql, val)
            result = self.connector.commit()

        return (json.dumps(dict(data='Item added.')), 200)

    def getItem(self, content):
        self.ensureConnected()
        sql = "SELECT (inventoryID) FROM Users WHERE id = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        inventoryID = result[0][0]

        sql = "SELECT id, itemname, expiration, quantity, measurement, location FROM Items WHERE inventoryID = %s"
        val = (inventoryID, )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        for i in result:
            if i[1] == content['itemname']:
                payload = {
                    'data' : 'Successfully pulled item from inventory.',
                    'item' : dict(itemID=i[0], itemname=i[1], expDate=i[2], quantity=i[3], measurement=i[4], location=i[5])
                }
                return (json.dumps(payload, default=str), 200)
        return (json.dumps(dict(data="Could not pull item.")), 401)

    def delItem(self, content):
        self.ensureConnected()
        sql = "SELECT id, itemname, quantity, measurement, location, useID FROM Items WHERE id = %s"
        val = (content['itemID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        if len(result) is not 0:
            newQuantity = result[0][2] - float(content['quantity'])
        
            if newQuantity <= 0:
                #sql = "DELETE FROM Items WHERE id = %s"
                sql = "UPDATE Items SET quantity = %s WHERE id = %s"
                val = (0, content['itemID'], )
            else:
                sql = "UPDATE Items SET quantity = %s WHERE id = %s"
                val = (newQuantity, content['itemID'], )
                
            useID = result[0][5]
            
            self.cursor.execute(sql, val)
            self.connector.commit()
            
            sql = "SELECT `usage` FROM FoodUse WHERE id = %s"
            val= (useID, )
            self.cursor.execute(sql, val)
            result = self.cursor.fetchall()
            
            useData = json.loads(result[0][0])
            
            if content['useType'] == 'used':
                used = {
                    "date" : datetime.datetime.now().strftime("%Y-%m-%d"),
                    "quantity" : content["quantity"]
                }
                useData['used'].append(used)
                useData['usedTotal'] = float(useData['usedTotal']) + float(content['quantity'])
                
                sql = "UPDATE FoodUse SET `usage` = %s WHERE id = %s"
                val = (json.dumps(useData), useID, )
                self.cursor.execute(sql, val)
                result = self.connector.commit()
            else:
                exp = {
                    "date" : datetime.datetime.now().strftime("%Y-%m-%d"),
                    "quantity" : content["quantity"]
                }
                useData['wasted'].append(exp)
                useData['wastedTotal'] = float(useData['wastedTotal']) + float(content['quantity'])
                
                sql = "UPDATE FoodUse SET `usage` = %s WHERE id = %s"
                val = (json.dumps(useData), useID, )
                self.cursor.execute(sql, val)
                result = self.connector.commit()
        
            self.cursor.execute(sql, val)
            self.connector.commit()
        
            return (json.dumps(dict(data='Item deleted.')), 200)
        else:
            return (json.dumps(dict(data='Item does not exist')), 401)

    def getInventory(self, content):
        self.ensureConnected()
        sql = "SELECT (inventoryID) FROM Users WHERE id = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        inventoryID = result[0][0]

        sql = "SELECT id, useID, itemname, expiration, quantity, measurement, location FROM Items WHERE inventoryID = %s ORDER BY expiration"
        val = (inventoryID, )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        temp = []
        for i in result:
            temp.append(dict(itemID=i[0], useID=i[1], itemname=i[2], expDate=i[3], quantity=i[4], measurement=i[5], location=i[6]))

        payload = {
            'data' : temp
        }
        
        if len(temp) == 0:
            return (json.dumps(dict(data='Inventory is currently empty.'), default=str), 401)
        else:
            return (json.dumps(payload, default=str), 200)

    def searchItem(self, content):
        self.ensureConnected()
        sql = "SELECT (inventoryID) FROM Users WHERE id = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        inventoryID = result[0][0]
        
        sql = "SELECT id, useID, itemname, expiration, quantity, measurement, location FROM Items WHERE itemname LIKE %s AND inventoryID = %s"
        val = ('%' + content['itemname'] + '%', inventoryID, )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        temp = []
        for i in result:
            temp.append(dict(itemID=i[0], useID=i[1], itemname=i[2], expDate=i[3], quantity=i[4], measurement=i[5], location=i[6]))
        
        payload = {
            'data' : temp
        }
        
        if len(temp) == 0:
            return (json.dumps(dict(data='Item not found in inventory.'), default=str), 401)
        else:
            return (json.dumps(payload, default=str), 200)

    def getReccRecipes(self, content):
        self.ensureConnected()
        sql = "SELECT (inventoryID) FROM Users WHERE id = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        inventoryID = result[0][0]

        sql = "SELECT (itemname) FROM Items WHERE inventoryID = %s ORDER BY expiration"
        val = (inventoryID, )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        searchUrl = 'https://www.foodnetwork.com/search/'

        for i in range(0, 5):
            if " " in result[i][0]:
                result[i][0].replace(' ', '-')
            searchUrl = searchUrl + "-" + result[i][0]
        searchUrl = searchUrl + '-'

        searchRequest = requests.get(searchUrl)
        soup = BeautifulSoup(searchRequest.text)

        temp = []
        for link in soup.find_all('h3', 'm-MediaBlock__a-Headline'):
            recipeUrl = link.a.get('href')
            if 'recipes' in recipeUrl:
                url = "https:" + recipeUrl
                recipe_list = scrape_schema_recipe.scrape_url(url, python_objects=True)

                if len(recipe_list) != 0:
                    recipe = {
                        'name' : recipe_list[0]['name'],
                        #'cookTime' : recipe_list[0]['cookTime'],
                        'recipeIngredient' : recipe_list[0]['recipeIngredient'],
                        'recipeInstructions' : recipe_list[0]['recipeInstructions']
                    }
                    if 'cookTime' in recipe_list[0].keys():
                        recipe['cookTime'] = recipe_list[0]['cookTime']

                    temp.append(recipe)

        payload = {
            'data' : temp
        }

        return (json.dumps(payload, default=str), 200)
        
    def getPersonalRecipes(self, content):
        self.ensureConnected()
        sql = "SELECT recipeID FROM PersonalRecipes WHERE userID = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        temp = []

        if len(result) > 0:
            for i in result:
                sql = "SELECT id, name, description, servings, ingredients FROM Recipes WHERE id = %s"
                val = (i[0], )
                self.cursor.execute(sql, val)
                recipe = self.cursor.fetchall()
                
                with open('/home/mperry/debug.log', 'w') as debug:
                    debug.write(str(i))

                tempJson = {
                    'recipeID' : recipe[0][0],
                    'name' : recipe[0][1],
                    'description' : recipe[0][2],
                    'servings' : recipe[0][3],
                    'ingredients' : '{\"ingredients\" : ' + recipe[0][4].replace("\'", "\"") + '}'
                }
                
                temp.append(tempJson)
                
            payload = {
                'data' : temp
            }
            
            return (json.dumps(payload, default=str), 200)
        else:
            return (json.dumps(dict(data='Personal Recipes Empty.')), 401)

    def updatePersonalRecipe(self, content):
        self.ensureConnected()
        sql = "UPDATE Recipes SET name=%s, description=%s, servings=%s, ingredients=%s WHERE id=%s"
        val = (content['name'], content['description'], content['servings'], str(content['ingredients']), content['recipeID'], )
        self.cursor.execute(sql, val)
        result = self.connector.commit()

        return (json.dumps(dict(data='Recipe Updated.')), 200)


    def addRecipe(self, content):
        self.ensureConnected()
        sql = "INSERT INTO Recipes (name, description, servings, ingredients) VALUES (%s, %s, %s, %s)"
        val = (content['name'], content['description'], content['servings'], str(content['ingredients']), )
        self.cursor.execute(sql, val)
        result = self.connector.commit()

        sql = "SELECT id FROM Recipes ORDER BY id DESC LIMIT 1"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        sql = "INSERT INTO PersonalRecipes (userID, recipeID) VALUES (%s, %s)"
        val = (content['userID'], result[0][0], )
        self.cursor.execute(sql, val)
        result = self.connector.commit()

        return (json.dumps(dict(data='Recipe Added.')), 200)

    def delRecipe(self, content):
        self.ensureConnected()
        sql = "DELETE FROM PersonalRecipes WHERE recipeID = %s"
        val = (content['recipeID'], )
        self.cursor.execute(sql, val)
        result = self.connector.commit()

        sql = "DELETE FROM Recipes WHERE id = %s"
        val = (content['recipeID'], )
        self.cursor.execute(sql, val)
        result = self.connector.commit()

        return (json.dumps(dict(data='Recipe Deleted.')), 200)
        
    def getTrends(self, content):
        self.ensureConnected()
        
        # Get inventoryID
        sql = "SELECT (inventoryID) FROM Users WHERE id = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        # Get items in user's inventory, along with its useID
        sql = "SELECT id, itemname, measurement, useID FROM Items WHERE inventoryID = %s"
        val = (result[0][0], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        userItems = result
        useData = []
        
        # Get usage information from FoodUse
        for x in userItems:
            sql = "SELECT itemname, measurement, `usage` FROM FoodUse WHERE id = %s"
            val = (x[3], )
            self.cursor.execute(sql, val)
            result = self.cursor.fetchone()
            temp = {
                "itemname" : result[0],
                "measurement" : result[1],
                "usage" : json.loads(result[2])
            }
            useData.append(temp)
        
        # Trim items from usage history that are older than 6 months(technically 24 weeks)
        cutOffDate = datetime.date.today() - datetime.timedelta(days=168)
        
        for x in useData:
            index = 0
            for i in x['usage']['used']:
                if datetime.date.fromisoformat(i['date']) < cutOffDate:
                    x['usage']['used'].pop(index)
                index += 1
            indexToo = 0
            for j in x['usage']['wasted']:
                if datetime.date.fromisoformat(j['date']) < cutOffDate:
                    x['usage']['wasted'].pop(indexToo)
                indexToo += 1
                
        # Calculate (x,y) values to send to mobile application
        usedPoints = []
        usedPoints.append((0, 0))
        wastedPoints = []
        wastedPoints.append((0, 0))
        itemPoints = []

        segmentBeginDate = cutOffDate
        segmentStopDate = cutOffDate + datetime.timedelta(days=14)
        xValue = 1

        largestYval = 0

        for x in useData:
            temp = {
                'used' : [],
                'wasted' : [],
                'itemname' : x['itemname'],
                'measurement' : x['measurement']
            }
            itemPoints.append(temp)

        while(segmentStopDate <= datetime.date.today()):
            
            usedSegmentTotal = 0
            wastedSegmentTotal = 0

            for index, x in enumerate(useData):
                for i in x['usage']['used']:
                    if datetime.date.fromisoformat(i['date']) > segmentBeginDate and datetime.date.fromisoformat(i['date']) <= segmentStopDate:
                        usedSegmentTotal += float(i['quantity'])
                
                for j in x['usage']['wasted']:
                    if datetime.date.fromisoformat(j['date']) > segmentBeginDate and datetime.date.fromisoformat(j['date']) <= segmentStopDate:
                        wastedSegmentTotal += float(j['quantity'])

            usedPoints.append((xValue, usedSegmentTotal))
            wastedPoints.append((xValue, wastedSegmentTotal))
            
            if usedSegmentTotal > largestYval:
                largestYval = usedSegmentTotal
            if wastedSegmentTotal > largestYval:
                largestYval = wastedSegmentTotal

            xValue += 1
            segmentBeginDate = segmentBeginDate + datetime.timedelta(days=14)
            segmentStopDate = segmentStopDate + datetime.timedelta(days=14)

        segmentBeginDate = cutOffDate
        segmentStopDate = cutOffDate + datetime.timedelta(days=14)
        xValue = 0

        while(segmentStopDate <= datetime.date.today()):
            for index, x in enumerate(useData):
                itemUsedSegmentTotal = 0
                itemWastedSegmentTotal = 0
                for i in x['usage']['used']:
                    if datetime.date.fromisoformat(i['date']) > segmentBeginDate and datetime.date.fromisoformat(i['date']) <= segmentStopDate:
                        itemUsedSegmentTotal += float(i['quantity'])
                itemPoints[index]['used'].append((xValue, itemUsedSegmentTotal))
                for i in x['usage']['wasted']:
                    if datetime.date.fromisoformat(i['date']) > segmentBeginDate and datetime.date.fromisoformat(i['date']) <= segmentStopDate:
                        itemWastedSegmentTotal += float(i['quantity'])
                itemPoints[index]['wasted'].append((xValue, itemWastedSegmentTotal))

            xValue += 1
            segmentBeginDate = segmentBeginDate + datetime.timedelta(days=14)
            segmentStopDate = segmentStopDate + datetime.timedelta(days=14)

        wasted = []
        for index, x in enumerate(itemPoints):
            total = 0
            largestY = -1
            for i in x['used']:
                if i[1] > largestY:
                    largestY = i[1]
            for i in x['wasted']:
                if i[1] > largestY:
                    largestY = i[1]
                total += i[1]
            wasted.append((index, total))
            itemPoints[index]['largest'] = largestY

        wasted.sort(reverse=True, key=lambda x:x[1])

        sortedItemPoints = []
        for x in wasted:
            sortedItemPoints.append(itemPoints[x[0]])

        # Return values to application
        payload = {
            'used' : usedPoints,
            'wasted' : wastedPoints,
            'largest' : largestYval,
            'items' : sortedItemPoints
        }
        
        return (json.dumps(payload), 200)
        
    def generatePerfectLarder(self, content):
        self.ensureConnected()
        
        # Get inventoryID
        sql = "SELECT (inventoryID) FROM Users WHERE id = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        # Get items in user's inventory, along with its useID
        sql = "SELECT id, itemname, measurement, useID FROM Items WHERE inventoryID = %s"
        val = (result[0][0], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        userItems = result
        useData = []
        
        # Get use data for each item and store in parallel list
        for x in userItems:
            sql = "SELECT id, itemname, measurement, `usage` FROM FoodUse WHERE id = %s"
            val = (x[3], )
            self.cursor.execute(sql, val)
            result = self.cursor.fetchone()
            data = {
                "id" : result[0],
                "itemname" : result[1],
                "measurement" : result[2],
                "usage" : json.loads(result[3]),
                "useValues" : [],
                "useTotal" : 0
            }
            useData.append(data)
        
        # Only look at last 6 months of use data    
        cutOffDate = datetime.date.today() - datetime.timedelta(days=168)
        
        for x in useData:
            for index, i in enumerate(x['usage']['used']):
                if datetime.date.fromisoformat(i['date']) < cutOffDate:
                    x['used'].pop(index)
        
        #useValues = []
        segmentBeginDate = cutOffDate
        segmentStopDate = cutOffDate + datetime.timedelta(days=14)
                    
        while(segmentStopDate <= datetime.date.today()):

            for x in useData:
                usedSegmentTotal = 0
                
                for i in x['usage']['used']:
                    if datetime.date.fromisoformat(i['date']) > segmentBeginDate and datetime.date.fromisoformat(i['date']) <= segmentStopDate:
                        usedSegmentTotal += i['quantity']
                
                x['useValues'].append(usedSegmentTotal)
                x['useTotal'] += usedSegmentTotal

            segmentBeginDate = segmentBeginDate + datetime.timedelta(days=14)
            segmentStopDate = segmentStopDate + datetime.timedelta(days=14)
            
        for x in useData:
            x['need'] = x['useTotal'] / 12
            
        return useData
        
    def getPerfectLarder(self, content):
        self.ensureConnected()
        
        return (json.dumps(dict(data=self.generatePerfectLarder(content))), 200)

    def getShoppingList(self, content):
        self.ensureConnected()
        
        useData = self.generatePerfectLarder(content)
        
        # Calculate how much of which items are missing from inventory based upon perfect larder
        
        # Get inventoryID
        sql = "SELECT (inventoryID) FROM Users WHERE id = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        # Get items in user's inventory, along with its useID
        sql = "SELECT id, itemname, quantity, measurement FROM Items WHERE inventoryID = %s"
        val = (result[0][0], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        userItems = result
        
        needsToDel = []

        #for index, x in enumerate(useData):
        index = 0
        for x in useData:
            for i in userItems:
                if x['itemname'] == i[1] and x['measurement'] == i[3]:
                    x['need'] -= i[2]
                    if x['need'] < 0.5:
                        if index not in needsToDel:
                            needsToDel.append(index)
                    else:
                        x['need'] = math.ceil(x['need'])
            index += 1
        
        needsToDel.sort(reverse=True)

        for x in needsToDel:
            useData.pop(x)
                
        # Return shopping list in json format
        return (json.dumps(dict(data=useData)), 200)

    def updateMeasurementSetting(self, content):
        self.ensureConnected()
        sql = "UPDATE Users SET metric = %s WHERE id = %s"
        val = (content['measureType'], content['userID'], )
        self.cursor.execute(sql, val)
        result = self.connector.commit()
        
        return (json.dumps(dict(data='Successfully Updated.')), 200)
        
    def updateStorageLocations(self, content):
        self.ensureConnected()
        sql = "UPDATE Users SET storageLocations = %s WHERE id = %s"
        val = (json.dumps(content['locations']), content['userID'], )
        self.cursor.execute(sql, val)
        result = self.connector.commit()
        
        return (json.dumps(dict(data='Successfully Updated.')), 200)
        
    def getItemsAboutToExpire(self,content):
        self.ensureConnected()
        currentDate = content["currentDate"]
        currentUserId = content['userID']
        oneWeekAheadDate = content["currentWeekAhead"]
        zero = 0
        sql = "SELECT id, inventoryID,useID,itemname,expiration,quantity,measurement,location FROM Items WHERE Items.inventoryID = %s AND Items.expiration >= %s AND Items.expiration <= %s AND Items.quantity > %s ORDER BY Items.id ASC"
        val = (currentUserId,currentDate,oneWeekAheadDate,zero)
        self.cursor.execute(sql,val)
        result = self.cursor.fetchall()
        objects_list = []
        if(len(result) ==0):
            return (json.dumps(dict(data = "empty"), default=str), 400)
        else:
            for row in result:
                d = {
                    'id' : row[0],
                    'inventoryID' : row[1],
                    'useID': row[2],
                    'itemname':row[3],
                    'expiration':row[4],
                    'quantity':row[5],
                    'measurement':row[6],
                    'location':row[7]
                }

                objects_list.append(d)
            return (json.dumps(dict(data = objects_list), default=str), 200)
    def displayAllSharedUser(self,content):        
        self.ensureConnected()
        applicationUser = (content['userID'], )
        sqlJoin = "SELECT Users.name, Users.username FROM PermittedSharedUSer INNER JOIN Users ON PermittedSharedUSer.permitedUserId = Users.id WHERE  PermittedSharedUSer.userId = %s"  
        crows = self.cursor.execute(sqlJoin, applicationUser)
        result = self.cursor.fetchall()
        if(len(result) > 0 ):         
            objects_list = []
            for row in result:
                p = {
                    'name': row[0],
                    'username': row[1]
                }
                
                objects_list.append(p)            
            return (json.dumps(dict(data = objects_list), default=str), 200)   
        elif(crows ==None):
            return (json.dumps(dict(data = "empty")), 200)
    def checkIfUserAddsThemself(self, tempName,currentUserId):
        self.ensureConnected()
        sql = 'SELECT id, username FROM Users WHERE Users.username = %s'
        valname = (tempName,)
        self.cursor.execute(sql,valname)
        result = self.cursor.fetchone()
        buildobjects_list = []
        d = collections.OrderedDict()
        
        if(result == None):         
            d['empty'] = "Yes"
            d['username'] = None
            d['userId'] = None
            d['userId'] = None
            d['duplicate'] = None
        else:
            sqlAvoidDuplicates = 'SELECT * FROM PermittedSharedUSer WHERE PermittedSharedUSer.userId = %s AND PermittedSharedUSer.permitedUserId =%s'
            valDuplicate= (currentUserId,result[0])
            rows = self.cursor.execute(sqlAvoidDuplicates,valDuplicate)
            result2 = self.cursor.fetchall()

            if(rows == 1 or len(result2) > 0 ):
                d['empty'] = "No"
                d['username'] = result[1]
                d['userId'] = result[0]
                d['duplicate'] = "Yes"
            elif(rows == None):
                d['empty'] = "No"
                d['username'] = result[1]
                d['userId'] = result[0]
                d['duplicate'] = "No"
            
        buildobjects_list.append(d)
        return dict(data = buildobjects_list)
    def addToShareList(self,content):
        self.ensureConnected()
        #check if user is not adding themselves return 
        usernameRecieved  = (content['userName'])
        userID = (content['userID'])
        tempData = self.checkIfUserAddsThemself(usernameRecieved,userID)
        
        if(tempData['data'][0]['empty'] == "No"):
            if(tempData['data'][0]['userId'] != userID):
                if(tempData['data'][0]['duplicate'] == "No"):
                    sql = "INSERT INTO PermittedSharedUSer (userId, permitedUserId) VALUES (%s, %s)"
                    val = (userID, tempData['data'][0]['userId'], )
                    self.cursor.execute(sql, val)
                    result = self.connector.commit()
                    return (json.dumps(dict(data='0')), 200)
                else:
                    return (json.dumps(dict(data='3')), 401) # That username has been added before
            else:
                return (json.dumps(dict(data='2')), 401) # You can not add yourself
        else:
            return (json.dumps(dict(data='1')), 401) # Yiu can not add a user that is not on the application 
    def removeFromShareList(self,content):
        self.ensureConnected()
        usernameRecieved  = (content['userName'])
        userID = (content['userID'])
        tempData = self.checkIfUserAddsThemself(usernameRecieved,userID)        
        if(tempData['data'][0]['empty'] == "No"):   #empty name found in the users table
            if(tempData['data'][0]['userId'] != userID):
                if(tempData['data'][0]['duplicate'] == "Yes"):
                    sql = "DELETE FROM PermittedSharedUSer WHERE userId = %s AND permitedUserId = %s"
                    val = (userID, tempData['data'][0]['userId'], )
                    self.cursor.execute(sql, val)
                    result = self.connector.commit()
                    return (json.dumps(dict(data='0')), 200)
                else:
                    return (json.dumps(dict(data='3')), 401) # You can not delete remove nothing
            else:
                return (json.dumps(dict(data='2')), 401)
        else:
            return (json.dumps(dict(data='1')), 401)
    def shareFoodItemToUser(self,content):
        self.ensureConnected()
        fromUserId = content['userID']
        quantityToShare = content['quantity']
        isMaxQuantity = content['max']
        sharedItemId = content['itemID']
        
        # to lis of users gotten from the query of permittedShare user
        sqlGetPermittedShareUserId = "SELECT permitedUserId FROM PermittedSharedUSer WHERE userId = %s "
        valname = (fromUserId,)
        self.cursor.execute(sqlGetPermittedShareUserId,valname)
        result = self.cursor.fetchall()
        if(len(result) > 0):
            for row in result:
                sqlInsertIterm = "INSERT INTO SharedItem(ownerId,userId,shareditemId,maxItem,quantity) VALUES(%s,%s,%s,%s,%s) "
                val = (fromUserId,row[0],sharedItemId,isMaxQuantity,quantityToShare,)
                self.cursor.execute(sqlInsertIterm, val)
                result2 = self.connector.commit()
            return (json.dumps(dict(data='1')), 200)
        else:
            return(json.dumps(dict(data='2')), 401)#nothing to do go add users to your shared list
    def viewAllNotification(self, content):
        self.ensureConnected()
        #username is sharing 
        #Itemname of 
        #quantity
        #click to :
        #accept or reject
        userId = (content['userID'],)
        
        sql = "SELECT Users.username, Items.itemname, SharedItem.quantity, SharedItem.maxItem, SharedItem.response, SharedItem.seen, SharedItem.shareditemId, Items.measurement,Items.location,Items.expiration,Items.quantity FROM SharedItem INNER JOIN Users ON SharedItem.ownerId = Users.id INNER JOIN Items ON SharedItem.shareditemId = Items.id WHERE SharedItem.userId =%s"
        crows = self.cursor.execute(sql,userId)
        result = self.cursor.fetchall()
        if(len(result) > 0 ):         
            objects_list = []
            for row in result:
                p = {
                    'username': row[0],
                    'itemname': row[1],
                    'quantity': row[2],
                    'maxItem': row[3],
                    'response': row[4],
                    'seen': row[5],
                    'itemId': row[6],
                    "Unit": row[7],
                    "Location": row[8],
                    "expire": row[9],
                    "maxquantity": row[10]
                }
                
                objects_list.append(p)            
            return (json.dumps(dict(data = objects_list), default=str), 200)   
        elif(crows ==None):
            return (json.dumps(dict(data = "empty")), 200)
        
    def rejectItem(self,content):
        userId = content['userID']
        sharedItemId = content['itemId']
        response = "no"
        
        sql = "UPDATE SharedItem SET response = %s WHERE SharedItem.shareditemId = %s AND SharedItem.userId = %s"
        val = (response,sharedItemId,userId, )
        self.cursor.execute(sql, val)
        result = self.connector.commit()

        return (json.dumps(dict(data='1')), 200)
    def acceptItem(self,content):
        if(content['max'] == 'yes'):
            pass
        elif(content['max'] == 'no'):
            pass
        pass