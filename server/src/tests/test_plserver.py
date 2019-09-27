from flask import Flask
from flask_testing import TestCase

class test_plserver(TestCase):
    
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
    
    def test_login_logout(self):
        response = self.client.post("/login", data=dict(username='username', password='password'))
        
        self.assertEqual(response.code, 200)
        self.assertEqual("Successful login.", response.data)
        
        response = self.client.post("/logout", data=dict(username='username'))
        
        self.assertEqual(response.code, 200)
        self.assertEqual("Successful logout.", response.data)
        
        response = self.client.post("/login", data=dict(username='abc', password='password'))
        
        self.assertEqual(response.code, 401)
        self.assertEqual("Invalid username.", response.data)
        
        response = self.client.post("/login", data=dict(username='username', password='abc'))
        
        self.assertEqual(response.code, 401)
        self.assertEqual("Incorrect password.", response.data)
        
    def test_addItem(self):
        pass
    
    def test_delItem(self):
        pass
    
    def test_getInventory(self):
        pass