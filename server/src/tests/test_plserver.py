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
    
    def test_login_logout(self):
        response = self.client.post('/login', headers={'Content-Type':'application/json'}, data=json.dumps(dict(username='Brutus', password='Hammerfist')))
        data = json.loads(response.data)

        self.assert200(response, 'Successful login failed.')
        self.assertEqual("Successful login.", data['data'])
        
        #Logout not really necessary in application.
        #response = self.client.post("/logout", headers={'Content-Type':'application/json'}, data=dict(username='username'))
        #data = json.loads(response.data)

        #self.assert200(response, 'Succesful logout failed.')
        #self.assertEqual("Successful logout.", data['data'])
        
        response = self.client.post('/login', headers={'Content-Type':'application/json'}, data=json.dumps(dict(username='abc', password='Hammerfist')))
        data = json.loads(response.data)

        self.assert401(response, 'Invalid username failed.')
        self.assertEqual("Invalid username.", data['data'])
        
        response = self.client.post('/login', headers={'Content-Type':'application/json'}, data=json.dumps(dict(username='Brutus', password='abc')))
        data = json.loads(response.data)

        self.assert401(response, 'Incorrect password failed.')
        self.assertEqual("Incorrect password.", data['data'])
        
    def test_addItem(self):
        pass
    
    def test_delItem(self):
        pass
    
    def test_getInventory(self):
        pass

if __name__ == '__main__':
	unittest.main()
