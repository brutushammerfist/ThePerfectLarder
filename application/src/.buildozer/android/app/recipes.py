# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller  



# setup GUI (kivy)

import kivy
kivy.require('1.11.1')
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class Recipes(Screen):
	pass

	#recipeName = ObjectProperty(None)
	#ingredients = ObjectProperty(None)
	#cookDirections = ObjectProperty(None)

	# Will likely be done on the server side
	#def recommendRecipes(self):
		# query the recipe database for recipes that match the users inventory
		# display to users
		
		
	#def userRecipe(self):
		# send (self.recipeName.text, self.ingredients.text, self.cookDirections.text) to database
		
		
	#def verifyRecipeWasUsed(self):
		# remove the items that were used in the recipe from the inventory
		
class AddRecipe(Screen):         #part of recipes
    pass
	
class GetRecipe(Screen):          #part of recipes
    pass