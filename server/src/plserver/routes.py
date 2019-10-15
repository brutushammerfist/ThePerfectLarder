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
    content = request.get_json()
    credentialCheck = db.login(content['username'], content['password'])
    return credentialCheck
@app.route('/signUp', methods = ['POST'])
def signUp():
	content = request.get_json()
	resultCheck = db.signUp(content['username'],content['useremail'],content['password'])
	return resultCheck
@app.route('/addItem', methods = ['POST'])
def addItem():
    content = request.get_json()
    addCheck = db.addItem(content)
    return addCheck

@app.route('/getItem', methods = ['POST'])
def getItem():
    content = request.get_json()
    getItemCheck = db.getItem(content)
    return getItemCheck
    
@app.route('/delItem', methods = ['POST'])
def delItem():
    content = request.get_json()
    delCheck = db.delItem(content)
    return delCheck

@app.route('/getInventory', methods = ['POST'])
def getInventory():
    content = request.get_json()
    getInvCheck = db.getInventory(content)
    return getInvCheck
    
@app.route('/searchItem', methods = ['POST'])
def searchItem():
    content = request.get_json()
    searchCheck = db.searchItem(content)
    return searchCheck

@app.route('/getReccRecipes', methods = ['POST'])
def getReccRecipes():
    content = request.get_json()
    getReccRecipeCheck = db.getReccRecipes(content)
    return getReccRecipeCheck

@app.route('/addRecipe', methods = ['POST'])
def addRecipe():
    content = request.get_json()
    addRecipeCheck = db.addRecipe(content)
    return addRecipeCheck

@app.route('/delRecipe', methods = ['POST'])
def delRecipe():
    content = request.get_json()
    delRecipeCheck = db.delRecipe(content)
    return delRecipeCheck
    
@app.route('/getRecipes', methods = ['POST'])
def getRecipes():
    content = request.get_json()
    getRecipeCheck = db.getRecipes(content)
    return getRecipeCheck
    
@app.route('/getPersonalRecipes', methods = ['POST'])
def getPersonalRecipes():
    content = request.get_json()
    getPersonalRecipesCheck = db.getPersonalRecipes(content)
    return getPersonalRecipesCheck