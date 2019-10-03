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
        
    def test_addItem_getItem(self):
        response = self.client.post('/addItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(name='Strawberry', quantity='1', measurement='lbs', location='fridge')))
        data = json.loads(response.data)
        
        self.assert200(response, 'Adding item failed.')
        self.assertEqual("Successfully added item to inventory.", data['data'])
        
        response = self.client.post('/getItem', headers={'Content-Type':'application/json'}, data=json.dumps(dict(name='Strawberry')))
        
        self.assert200(response, 'Getting item failed.')
        self.assertEqual("Successfully pulled item from inventory.", data['data'])
        
        self.assertEqual("1", data['item']['quantity'])
        self.assertEqual("lbs", data['item']['measurement'])
        self.assertEqual("fridge", data['item']['location'])
        
    def test_delItem(self):
        pass
    
    def test_getInventory(self):
        pass

if __name__ == '__main__':
	unittest.main()
