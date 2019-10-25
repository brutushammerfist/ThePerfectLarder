# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 

import unittest
import Login

class TestLogin(unittest.TestCase):

	def test_userLogin(self):

		headers = {'Content-Type' : 'application/json'}
           
        payload = {
            'username' : 'Brutus',
            'password' : 'Hammerfist'
        }
            
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/login', headers=headers, data=json.dumps(payload)).json()

        self.assertEquals(response['data'], 'Successful login.')

        headers = {'Content-Type' : 'application/json'}
           
        payload = {
            'username' : 'Brutus',
            'password' : 'Hammerf1st'
        }
            
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/login', headers=headers, data=json.dumps(payload)).json()

        self.assertEquals(response['data'], 'Incorrect password.')

        headers = {'Content-Type' : 'application/json'}
           
        payload = {
            'username' : 'Brutos',
            'password' : 'Hammerfist'
        }
            
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/login', headers=headers, data=json.dumps(payload)).json()

        self.assertEquals(response['data'], 'Invalid username.')
	
#need below to run tests
if __name__ == '__main__':
	unittest.main()