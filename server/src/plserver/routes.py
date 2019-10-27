from plserver import app
from .database import Database

from flask import request

import json

db = Database()

@app.route('/')
@app.route('/index')
def index():
	return "I am a placeholder. Watch me hold places."

@app.route('/login', methods = ['POST'])
def login():
    return db.login(request.get_json())

@app.route('/signUp', methods = ['POST'])
def signUp():
	return db.signUp(request.get_json())
    
@app.route('/addItem', methods = ['POST'])
def addItem():
    return db.addItem(request.get_json())

@app.route('/getItem', methods = ['POST'])
def getItem():
    return db.getItem(request.get_json())
    
@app.route('/delItem', methods = ['POST'])
def delItem():
    return db.delItem(request.get_json())

@app.route('/getInventory', methods = ['POST'])
def getInventory():
    return db.getInventory(request.get_json())
    
@app.route('/searchItem', methods = ['POST'])
def searchItem():
    return db.searchItem(request.get_json())

@app.route('/getReccRecipes', methods = ['POST'])
def getReccRecipes():
    return db.getReccRecipes(request.get_json())

@app.route('/addRecipe', methods = ['POST'])
def addRecipe():
    return db.addRecipe(request.get_json())

@app.route('/delRecipe', methods = ['POST'])
def delRecipe():
    return db.delRecipe(request.get_json())
    
@app.route('/getPersonalRecipes', methods = ['POST'])
def getPersonalRecipes():
    return db.getPersonalRecipes(request.get_json())
    
@app.route('/getTrends', methods = ['POST'])
def getTrends():
    return db.getTrends(request.get_json())
    
@app.route('/getShoppingList', methods = ['POST'])
def getShoppingList():
    return db.getShoppingList(request.get_json())
    
@app.route('/updateMeasurementSetting', methods = ['POST'])
def updateMeasurementSetting():
    return db.updateMeasurementSetting(request.get_json())