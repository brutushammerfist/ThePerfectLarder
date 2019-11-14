# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 

import unittest
import Inventory, Additem, DeleteItem

class TestInventory(unittest.TestCase):
  
    def test_searchItem(self):
    
        headers = {'Content-Type' : 'application/json'}
           
        payload = {
            'userID' : '1',
            'itemname' : 'banana',
            'quantity' : '2',
            'measurement' : 'lbs',
            'expDate' : '2020-01-01',
            'location' : 'pantry'
        }
            
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/addItem', headers=headers, data=json.dumps(payload)).json()
        
        if response['data'] == 'Item added.':
            key = 'banana'
            search = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/searchItem', headers={'Content-Type': 'application/json'}, data=json.dumps(dict(userID='1', itemname=key))).json()
            
        self.assertTrue(len(search['data']) > 0)

class TestAddItem(unittest.TestCase):

    def test_addItems(self):

        headers = {'Content-Type' : 'application/json'}
           
        payload = {
            'userID' : '1',
            'itemname' : 'banana',
            'quantity' : '2',
            'measurement' : 'lbs',
            'expDate' : '2020-01-01',
            'location' : 'pantry'
        }
            
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/addItem', headers=headers, data=json.dumps(payload)).json()
        
        self.assertEqual(response['data'],'Item added.')
        

class TestDeleteItem(unittest.TestCase):

    def test_deleteItems(self):
    
        headers = {'Content-Type' : 'application/json'}
           
        payload = {
            'userID' : '1',
            'itemname' : 'banana',
            'quantity' : '2',
            'measurement' : 'lbs',
            'expDate' : '2020-01-01',
            'location' : 'pantry'
        }
            
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/addItem', headers=headers, data=json.dumps(payload)).json()
        
        if response['data'] == 'Item added.':
            key = 'banana'
            search = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/delItem', headers={'Content-Type': 'application/json'}, data=json.dumps(dict(userID='1', itemname=key))).json()
            
        self.assertEqual(search['data'], 'Item deleted.')
	
    
#need below to run tests
if __name__ == '__main__':
	#unittest.main()
    test_classes_to_run = [TestInventory, TestAddItem, TestDeleteItem]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)