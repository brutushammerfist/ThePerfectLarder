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
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.core.window import WindowBase

class WrapButton(Button):
    pass

class GetRecipe(Screen):
    recipes = []
    viewrecipe = -1
    def on_pre_enter(self):
        self.ids.recipes.clear_widgets()
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getReccRecipes', headers={'Content-Type': 'application/json'}, data=json.dumps(dict(userID=App.get_running_app().userID))).json()
        
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

class Ingredient(GridLayout):
    def populate(self):
        self.cols = 3
        self.add_widget(TextInput())
        self.add_widget(TextInput())
        self.add_widget(Spinner(text = 'Choose', values = ('lbs', 'oz', 'bag', 'box')))
        
    def deleteSelf(self):
        self.parent.remove_widget(self)
        
class AddRecipe(Screen):
    recipeContent = GridLayout(cols=1)
    recipeContent.add_widget(Label(text='Recipe successfully added'))
    recipeButton = Button(text='OK')
    recipeContent.add_widget(recipeButton)
    recipePopup = Popup(title='Added Recipe', content=recipeContent, auto_dismiss=False, size_hint=(.8, .2))
    recipeButton.bind(on_press=recipePopup.dismiss)

    def on_pre_enter(self):
        self.addIngredient()
        
    def addIngredient(self):
        self.ids.ingredients.add_widget(Ingredient())
        self.ids.ingredients.children[0].populate()

    def delIngredient(self):
        self.ids.ingredients.children[0].deleteSelf()
        
    def addRecipe(self):
        payload = {
            'userID' : App.get_running_app().userID,
            'name' : self.ids.name.text,
            'servings' : self.ids.servings.text,
            'description' : self.ids.description.text,
            'ingredients' : self.extractIngredients()
        }
        
        result = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/addRecipe', headers={'Content-Type':'application/json'}, data=json.dumps(payload)).json()
        
        if result['data'] == "Recipe Added.":
            self.clearFieldsAdd()
            self.addIngredient()
            self.recipePopup.open()
        else:
            print(result)
    
    def extractIngredients(self):
        ingredients = []
        
        for i in self.ids.ingredients.children:
            ingredient = i.children
            
            temp = {
                'name' : ingredient[2].text,
                'quantity' : ingredient[1].text,
                'measurement' : ingredient[0].text
            }
            
            ingredients.append(temp)
            
        return ingredients

    def clearFieldsAdd(self):
        self.ids.name.text = ""
        self.ids.servings.text = ""
        self.ids.description.text = ""
        self.ids.ingredients.clear_widgets()
    
class Recipe(Screen):
    pass
    
class ViewRecipe(Screen):
    index = NumericProperty(None)
    
    def on_pre_enter(self):
        self.ids.name.text = ""
        self.ids.ingredients.clear_widgets()
        self.ids.instructions.text = ""
        self.ids.cooktime.text = ""
        reScreen = self.manager.get_screen('getreccrecipes') # changed from getrecipes to viewrecipe
        recipe = reScreen.recipes[reScreen.viewrecipe.viewrecipe]
        self.ids.name.text = recipe['name']
        for i in recipe['recipeIngredient']:
            label = Button(text = str(i)) 
            self.ids.ingredients.add_widget(label)
        for i in recipe['recipeInstructions']:
            steptext = i['text']
            label = WrapButton(text = steptext, text_size=(700, None))
            self.ids.instructions.add_widget(label)
        self.ids.cooktime.text = recipe['cookTime']
        
class PersonalRecipe(Screen):
    recipes = []
    view = -1
    def on_pre_enter(self):
        self.ids.personalrecipe.clear_widgets()
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getPersonalRecipes', headers={'Content-Type': 'application/json'}, data=json.dumps(dict(userID=App.get_running_app().userID))).json()
        
        if response['data'] != 'Personal Recipes Empty.':
            self.recipes = response['data']
            for n in range(0, len(response['data'])):
                button = Button(text = response['data'][n]['name'])
                callback = lambda n:self.viewPersonalRecipe(n)
                button.recipe = n
                button.bind(on_press = callback)
                self.ids.personalrecipe.add_widget(button)
        else:
            self.ids.personalrecipe.add_widget(Button(text = 'Personal Recipes Currently Empty.'))
            
    def viewPersonalRecipe(self, index):
        self.view = index
        self.manager.current = 'viewpersonalrecipe'
            
    
class ViewPersonalRecipe(Screen):
    delRecipePopup = None
    ingred = []
    
    def on_pre_enter(self):
        self.ids.name.text = ""
        self.ids.ingredients.clear_widgets()
        self.ids.instructions.text = ""
        self.ids.servings.text = ""
        reScreen = self.manager.get_screen('personalrecipe')
        recipe = reScreen.recipes[reScreen.view.recipe]
        self.ids.name.text = recipe['name']
        ingred = json.loads(recipe['ingredients'])
        for n in ingred['ingredients']:
            label = Button(text = n['name']+ " - " + n['quantity'] + " " + n['measurement'])
            self.ids.ingredients.add_widget(label)
        self.ids.instructions.text = recipe['description']
        self.ids.servings.text = str(recipe['servings'])
        
    def deleteRecipe(self):
    
        delContent = GridLayout(cols=1)
        delContent.add_widget(Label(text= 'Recipe Deleted'))
        delButton = Button(text='OK')
        delContent.add_widget(delButton)
        self.delRecipePopup = Popup(title='Recipe Deleted', content=delContent, auto_dismiss=False, size_hint=(.8, .2))
        delButton.bind(on_press=self.delPopupDismiss)
        
        reScreen = self.manager.get_screen('personalrecipe')
        recipe = reScreen.recipes[reScreen.view.recipe]
        
        headers = {'Content-Type' : 'application/json'}
           
        payload = {
            'recipeID' : recipe['recipeID']
        }
            
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/delRecipe', headers=headers, data=json.dumps(payload)).json()
        
        if response['data'] == 'Recipe Deleted.':
            self.delRecipePopup.open()
            
    def addRecipeIngredientsToShoppingList(self):

        reScreen = self.manager.get_screen('personalrecipe')
        recipe = reScreen.recipes[reScreen.view.recipe]

        ingred = json.loads(recipe['ingredients'])
        for n in ingred['ingredients']:
            name = n['name']
            quantity = n['quantity']
            measurement = n['measurement']

            temp = {
                'name' : name,
                'quantity' : quantity,
                'measurement' : measurement
            }

            App.get_running_app().recipeIngredientsForShoppingList.append(temp)


    def delPopupDismiss(self, index):
        self.delRecipePopup.dismiss()
        self.manager.current = 'personalrecipe'
            