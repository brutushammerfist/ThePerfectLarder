from flask import Flask
from flask_testing import TestCase

import sys
sys.path.insert(0, '..')

import plserver

import unittest
import requests
import json

class test_plserver(TestCase):
    
    def create_app(self):    
        app = plserver.app
        return app
    
    def test_login(self):
        response = self.client.post('/login', headers={'Content-Type':'application/json'}, data=json.dumps(dict(username='Brutus', password='Hammerfist')))
        data = json.loads(response.data)

        self.assert200(response, 'Successful login failed.')
        self.assertEqual("Successful login.", data['data'])
        
        response = self.client.post('/login', headers={'Content-Type':'application/json'}, data=json.dumps(dict(username='abc', password='Hammerfist')))
        data = json.loads(response.data)

        self.assert401(response, 'Invalid username failed.')
        self.assertEqual("Invalid username.", data['data'])
        
        response = self.client.post('/login', headers={'Content-Type':'application/json'}, data=json.dumps(dict(username='Brutus', password='abc')))
        data = json.loads(response.data)

        self.assert401(response, 'Incorrect password failed.')
        self.assertEqual("Incorrect password.", data['data'])
        
    def test_addItem_getItem_delItem(self):
        response = self.client.post('/addItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname='Strawberry', quantity='1', measurement='lbs', location='fridge', expDate='2020-01-01')))
        data = json.loads(response.data)
        
        self.assert200(response, 'Adding item failed.')
        self.assertEqual("Item added.", data['data'])
        
        response = self.client.post('/getItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname='Strawberry')))
        data = json.loads(response.data)
        
        self.assert200(response, 'Getting item failed.')
        self.assertEqual("Successfully pulled item from inventory.", data['data'])
        
        self.assertEqual(float(1), data['item']['quantity'])
        self.assertEqual("lbs", data['item']['measurement'])
        self.assertEqual("fridge", data['item']['location'])
        self.assertEqual("2020-01-01", data['item']['expDate'])
        
        print(data)
        print(data['item'])
        print(data['item']['itemID'])
        response = self.client.post('/delItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(itemID=data['item']['itemID'])))
        data = json.loads(response.data)
        
        self.assert200(response, "Deleting item failed.")
        self.assertEqual("Successfully deleted item from inventory.", data['data'])
        
        response = self.client.post('/delItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname="Stewberry")))
        data = json.loads(response.data)
        
        self.assert401(response, "Found item that doesn't exist.")
        self.assertEqual("Found item that doesn't exist", data['data'])
        
        response = self.client.post('/getItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname="Strawberry")))
        data = json.loads(response.data)
        
        self.assert401(response, "Item does not exist.")
        self.assertEqual("Item does not exist.", data['data'])
    
    def test_getInventory(self):
        response = self.client.post('/addItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname='Strawberry', quantity='1', measurement='lbs', location='fridge', expDate='2020-01-01')))
        response = self.client.post('/addItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname='Ground Beef', quantity='3', measurement='lbs', location='fridge', expDate='2020-02-02')))
        response = self.client.post('/addItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname='Milk', quantity='1', measurement='gallon', location='fridge', expDate='2020-03-03')))
        
        response = self.client.post('/getInventory', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1)))
        data = json.loads(response.data)
        
        self.assertEqual(3, len(data['data']))
        self.assertEqual('Ground Beef', data['data'][0]['name'])
        self.assertEqual('3', data['data'][0]['quantity'])
        self.assertEqual('lbs', data['data'][0]['measurement'])
        self.assertEqual('fridge', data['data'][0]['location'])
        self.assertEqual('2020-01-01', data['data'][0]['expDate'])
        self.assertEqual('Milk', data['data'][1]['name'])
        self.assertEqual('1', data['data'][1]['quantity'])
        self.assertEqual('gallon', data['data'][1]['measurement'])
        self.assertEqual('fridge', data['data'][1]['location'])
        self.assertEqual('2020-02-02', data['data'][1]['expDate'])
        self.assertEqual('Strawberry', data['data'][2]['name'])
        self.assertEqual('1', data['data'][2]['quantity'])
        self.assertEqual('lbs', data['data'][2]['measurement'])
        self.assertEqual('fridge', data['data'][2]['location'])
        self.assertEqual('2020-03-03', data['data'][2]['expDate'])

        response = self.client.post('/delItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(itemname='Strawberry')))
        response = self.client.post('/delItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(itemname='Ground Beef')))
        response = self.client.post('/delItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(itemname='Milk')))

        response = self.client.post('/getInventory', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1)))
        data = json.loads(response.data)

        self.assert401(response, "Found items when should be empty.")
        self.assertEquals("Inventory is currently empty.", data['data'])

    def test_searchItem(self):
        response = self.client.post('/addItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname='Buttermilk', quantity='0.5', measurement='gallon', location='fridge', expDate='2020-01-01')))
        response = self.client.post('/addItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname='Ground Beef', quantity='3', measurement='lbs', location='fridge', expDate='2020-02-02')))
        response = self.client.post('/addItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname='Milk', quantity='1', measurement='gallon', location='fridge', expDate='2020-03-03')))
        
        response = self.client.post('/searchItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname="Milk")))
        data = json.loads(response.data)

        self.assert200(response, "Could not find item.")
        self.assertEqual('Buttermilk', data['data'][0]['itemname'])
        self.assertEqual('0.5', data['data'][0]['quantity'])
        self.assertEqual('gallon', data['data'][0]['measurement'])
        self.assertEqual('fridge', data['data'][0]['location'])
        self.assertEqual('2020-01-01', data['data'][0]['expDate'])
        self.assertEqual('Milk', data['data'][1]['itemname'])
        self.assertEqual('1', data['data'][1]['quantity'])
        self.assertEqual('gallon', data['data'][1]['measurement'])
        self.assertEqual('fridge', data['data'][1]['location'])
        self.assertEqual('2020-03-03', data['data'][1]['expDate'])

        response = self.client.post('/searchItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(userID=1, itemname="Strawberry")))
        data = json.loads(response.data)

        self.assert401(response, "Item found that shouldn't be.")
        self.assertEqual('Item not found in inventory.', data['data'])

if __name__ == '__main__':
	unittest.main()
