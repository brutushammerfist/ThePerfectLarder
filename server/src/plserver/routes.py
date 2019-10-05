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
