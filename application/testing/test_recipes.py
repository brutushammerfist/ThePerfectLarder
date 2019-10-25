# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller


import unittest
import Recipes


class TestRecipes(unittest.TestCase):
		
	def test_Addrecipe(self):

		payload = {
            'userID' : '1',
            'name' : 'Cookies',
            'servings' : '4',
            'description' : 'Peanut Butter Cookies',
            'ingredients' : '1 cup peanut butter, 1/2 cup sugar, 1 stick butter'
        }
        
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/addRecipe', headers={'Content-Type':'application/json'}, data=json.dumps(payload)).json()

        self.assertEquals(response['data'], 'Recipe Added.')

	def test_DelRecipe(self):

		headers = {'Content-Type' : 'application/json'}
           
        payload = {
            'recipeID' : '1'
        }
            
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/delRecipe', headers=headers, data=json.dumps(payload)).json()
        
        self.assertEquals(response['data'],'Recipe Deleted.')

		
#need below to run tests
if __name__ == '__main__':
	unittest.main()