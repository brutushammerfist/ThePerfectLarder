from bs4 import BeautifulSoup
import scrape_schema_recipe
import mysql.connector
import datetime
import requests
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
    
    def searchUsers(self):
        pass

    def login(self, username, password):
        sql = "SELECT id, username, password FROM Users WHERE username = %s"
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
            if password == data[2]:
                payload = {
                    'data' : 'Successful login.',
                    'userID' : data[0]
                }
                return (json.dumps(payload), 200)
            else:
                payload = {
                    'data' : 'Incorrect password.'
                }
                return (json.dumps(payload), 401)

    def addItem(self, content):
        print("Entering add item.")
        sql = "SELECT (inventoryID) FROM Users WHERE id = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        inventoryID = result[0][0]
        print("Inventory ID is " + str(inventoryID))

        sql = "INSERT INTO Items (inventoryID, itemname, expiration, quantity, measurement, location) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (inventoryID, content['itemname'], content['expDate'], content['quantity'], content['measurement'], content['location'])
        self.cursor.execute(sql, val)
        result = self.connector.commit()

        return (json.dumps(dict(data='Item added.')), 200)
        
    def getItem(self, content):
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
        sql = "SELECT id, itemname, quantity, measurement, location FROM Items WHERE id = %s"
        val = (content['itemID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        if len(result) is not 0:
            newQuantity = result[0][2] - float(content['quantity'])
        
            if newQuantity <= 0:
                sql = "DELETE FROM Items WHERE id = %s"
                val = (content['itemID'], )
            else:
                sql = "UPDATE Items SET quantity = %s WHERE id = %s"
                val = (newQuantity, content['itemID'], )
        
            self.cursor.execute(sql, val)
            self.connector.commit()
        
            return (json.dumps(dict(data='Item deleted.')), 200)
        else:
            return (json.dumps(dict(data='Item does not exist')), 401)

    def getInventory(self, content):
        sql = "SELECT (inventoryID) FROM Users WHERE id = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()

        inventoryID = result[0][0]

        sql = "SELECT id, useID, itemname, expiration, quantity, measurement, location FROM Items WHERE inventoryID = %s ORDER BY itemname"
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
                        'cookTime' : recipe_list[0]['cookTime'],
                        #'cookingMethod' : recipe_list[0]['cookingMethod'],
                        #'recipeCategory' : recipe_list[0]['recipeCategory'],
                        #'recipeCuisine' : recipe_list[0]['recipeCuisine'],
                        'recipeIngredient' : recipe_list[0]['recipeIngredient'],
                        'recipeInstructions' : recipe_list[0]['recipeInstructions']
                    }

                    temp.append(recipe)

        payload = {
            'data' : temp
        }

        return (json.dumps(payload, default=str), 200)
        
    def getPersonalRecipes(self, content):
        sql = "SELECT recipeID FROM PersonalRecipes WHERE userID = %s"
        val = (content['userID'], )
        self.cursor.execute(sql, val)
        result = self.cursor.fetchall()
        
        temp = []

        if len(result) > 0:
            for i in result:
                sql = "SELECT name, description, servings, ingredients FROM Recipes WHERE id = %s"
                val = (i[0], )
                self.cursor.execute(sql, val)
                recipe = self.cursor.fetchall()
                
                tempJson = {
                    'name' : i[0],
                    'description' : i[1],
                    'servings' : i[2],
                    'ingredients' : i[3]
                ]
                
                temp.append(tempJson)
                
            payload = {
                'data' : temp
            }
            
            return (json.dumps(payload, default=str), 200)
        else:
            return (json.dumps(dict(data='Personal Recipes Empty.')), 401)

    def addRecipe(self, content):
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

    def editRecipes(self, content):
        pass

    def delRecipes(self, content):
        pass