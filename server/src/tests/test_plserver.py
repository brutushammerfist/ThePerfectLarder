from flask import Flask
from flask_testing import TestCase

import sys
sys.path.insert(0, '..')

import plserver

import unittest

class test_plserver(TestCase):
    
    def create_app(self):
        #app = Flask(__name__)
        #app.config['TESTING'] = True
        app = plserver.app
        return app
    
    def test_login_logout(self):
        response = self.client.post("/login", data=dict(username='username', password=hash('password')))
        
        self.assert200(response, 'Successful login failed.')
        self.assertEqual("Successful login.", response.data)
        
        response = self.client.post("/logout", data=dict(username='username'))
        
        self.assert200(response, 'Succesful logout failed.')
        self.assertEqual("Successful logout.", response.data)
        
        response = self.client.post("/login", data=dict(username='abc', password='password'))
        
        self.assert401(response, 'Invalid username failed.')
        self.assertEqual("Invalid username.", response.data)
        
        response = self.client.post("/login", data=dict(username='username', password='abc'))
        
        self.assert401(response, 'Incorrect password failed.')
        self.assertEqual("Incorrect password.", response.data)
        
    def test_addItem(self):
        pass
    
    def test_delItem(self):
        pass
    
    def test_getInventory(self):
        pass

if __name__ == '__main__':
	unittest.main()
