# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 

import unittest
import Trends

class TestTrends(unittest.TestCase)
	
	def test_trends(self):
		
        headers = {'Content-Type' : 'application/json'}
           
        payload = {
            'userID' : App.get_running_app().userID   
        }
            
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getTrends', headers=headers, data=json.dumps(payload)).json()
		
        self.assertTrue(len(response['data']) > 0)
        
#need below to run tests
if __name__ == '__main__':
	unittest.main()