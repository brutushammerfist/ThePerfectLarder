# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller  

import kivy
kivy.require('1.11.1')
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
import requests
import json
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label


class GetRecipe(Screen):
    recipes = []
    viewrecipe = -1
    def on_pre_enter(self):
        self.ids.recipes.clear_widgets()
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getRecipes', headers={'Content-Type': 'application/json'}, data=json.dumps(dict(userID=App.get_running_app().userID))).json()
        
        if response['data'] != 'No Recipes Where Found.':
            self.recipes = response['data']
            for n in range(0, len(response['data'])):
                button = Button(text = response['data'][n]['name'])
                callback = lambda n:self.viewRecipe(n)
                button.viewrecipe = n
                button.bind(on_press = callback)
                self.ids.recipes.add_widget(button)
        else:
            self.ids.recipes.add_widget(Button(text = 'No recipes where found'))
            
    def viewRecipe(self, index):
        self.viewrecipe = index
        self.manager.current = 'viewrecipe'
    
    def getRecipe(self):
        pass
   
    def addRecipe(self):
        pass
    
    def verifyRecipe(self):
        pass
        
	
class AddRecipe(Screen):         #part of recipes
    pass
    
class Recipe(Screen):
    pass
    
class ViewRecipe(Screen):
    index = NumericProperty(None)
    
    def on_pre_enter(self):
        self.ids.name.text = ""
        self.ids.ingredients.clear_widgets()
        self.ids.instructions.text = ""
        self.ids.cooktime.text = ""
        reScreen = self.manager.get_screen('getrecipes')
        recipe = reScreen.recipes[reScreen.viewrecipe.viewrecipe]
        self.ids.name.text = recipe['name']
        #self.ids.ingredients.text = str(recipe['recipeIngredient'])
        ingred =  str(recipe['recipeIngredient']).split(',')
        for i in ingred:
            label = Label(text = i) 
            self.ids.ingredients.add_widget(label)
        self.ids.instructions.text = str(recipe['recipeInstructions'])
        self.ids.cooktime.text = recipe['cookTime']