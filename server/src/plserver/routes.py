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

@app.route('/addItem')
def addItem():
    content = request.get_json()
    addCheck = db.addItem(content)
    return addCheck

@app.route('/getItem')
def getItem():
    pass
    
@app.route('/delItem')
def delItem():
    pass

@app.route('/getInventory')
def getInventory():
    pass
    
@app.route('/searchItem')
def searchItem():
    pass
    
@app.route('/perfectLarder')
def perfectLarder():
    pass
