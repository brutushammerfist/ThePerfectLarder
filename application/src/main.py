# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 

import kivy
import unittest
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder 

from kivy.uix.spinner import Spinner

#class Main:
class UserLogin (Screen):
    pass #like return 0

Builder.load_string("""
<UserLogin>
	name:userName                #for python code : for kivy code
	password:userPassword        #for python code : for kivy code
	email:userEmail              #for python code : for kivy code
	GridLayout:
		cols:1
		size: root.width, root.height
		GridLayout:
			cols:2
		
			Label:
				text: "Name: "
				
			TextInput:
				id: userName
				multiline: False
				
			Label:
				text: "Password: "
				
			TextInput:
				id: userPassword
				multiline: False
				
			Label:
				text: "Email: "
				
			TextInput:
				id: userEmail
				multiline: False
			
		Button:
			text:"Login"
			on_press: root.manager.current = 'homescreen' 
			#on_press: root.userLogin()    to check the login credentials
			
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Profile'
            on_press: root.manager.current = 'profile'
		
		Button:
            text: 'Recipes'
            on_press: root.manager.current = 'recipes'
			
		Button:
            text: 'Inventory'
            on_press: root.manager.current = 'inventory'
			
		Button:
            text: 'Trends'
            on_press: root.manager.current = 'trends'
			
		Button:
            text: 'Shopping List'
            on_press: root.manager.current = 'shoppinglist'
			
		Button:
            text: 'Share Items'
            on_press: root.manager.current = 'shareitems'
			
		Button:
            text: 'Logout'
            on_press: root.manager.current = 'userlogin'                
			
<Profile>:
	BoxLayout:
        orientation: 'vertical'
		Button:
            text: 'Manage Perfect Larder'
            on_press: root.manager.current = 'managepl'
		Button:
            text: 'Edit/Create Profile'
            on_press: root.manager.current = 'editcreateprofile'
		Button:
            text: 'Setup/Edit Notifications'
            on_press: root.manager.current = 'setupeditnotification'
		Button:
            text: 'Back To Home'
            on_press: root.manager.current = 'homescreen'              
			
<ManagePL>:                                                            
	BoxLayout:
        orientation: 'vertical'
		
		Button:
            text: 'Back'
            on_press: root.manager.current = 'profile'                 

<EditCreateProfile>

	name:userName                #for python code : for kivy code
	password:userPassword        #for python code : for kivy code
	email:userEmail              #for python code : for kivy code
	
	BoxLayout:
        orientation: 'vertical'
		GridLayout:
			cols:2
		
			Label:
				text: "Name: "
				
			TextInput:
				id: userName
				multiline: False
				
			Label:
				text: "Password: "
				
			TextInput:
				id: userPassword
				multiline: False
				
			Label:
				text: "Email: "
				
			TextInput:
				id: userEmail
				multiline: False
		Button:
            text: 'Submit'
            #on_press:       send to function
		
		Button:
            text: 'Back'
            on_press: root.manager.current = 'profile'                
			
			
<SetupEditNotification>                                               
	BoxLayout:
        orientation: 'vertical'

		Button:
            text: 'Back'
            on_press: root.manager.current = 'profile'                



<Recipes>:
	BoxLayout:
        orientation: 'vertical'
		
		Button:
            text: 'Add Recipes'
            on_press: root.manager.current = 'addrecipe'
		
		Button:
            text: 'Get Recipes'
            on_press: root.manager.current = 'getrecipes'
		
		Button:
            text: 'Back To Home'
            on_press: root.manager.current = 'homescreen'		
		
		
<AddRecipe>

	recipeName:recipeName                #for python code : for kivy code
	ingredients:ingredients        		 #for python code : for kivy code
	cookDirections:cookDirections        #for python code : for kivy code
	
	GridLayout:
		cols:1
		size: root.width, root.height
		GridLayout:
			cols:2
			
			Label:
				text: "Name: "
					
			TextInput:
				id: recipeName
				multiline: False
					
			Label:
				text: "Ingredients: "
					
			TextInput:
				id: ingredients
				multiline: True
					
			Label:
				text: "Cooking Directions: "
					
			TextInput:
				id: cookDirections
				multiline: True
					
		Button:
			text:"Enter"
			#on_press: root.manager.current = 'homescreen' 
			#on_press: root.userLogin()    send data to a function
			
		Button:
            text: 'Back To Home'
            on_press: root.manager.current = 'recipes'
		

<GetRecipe>
		# go to to function and pull recipes


<Inventory>:
	BoxLayout:
        orientation: 'vertical'
		
		Button:
            text: 'Add Item'
            on_press: root.manager.current = 'additem'
			
		Button:
            text: 'Delete Item'
            on_press: root.manager.current = 'deleteitem'
			
		Button:
            text: 'View Inventory'
            on_press: root.manager.current = 'viewinventory'
			
		Button:
            text: 'Search'
            on_press: root.manager.current = 'searchitem'
			
		Button:
            text: 'Your Perfect Larder'
            on_press: root.manager.current = 'theperfectlarder'
			
		Button:
            text: 'Back To Home'
            on_press: root.manager.current = 'homescreen'

<AddItem>

	itemName:itemName                #for python code : for kivy code
	quantity:quantity        		 #for python code : for kivy code
	expirationDate:expirationDate    #for python code : for kivy code
	storageLocation:storageLocation  #for python code : for kivy code
	
	GridLayout:
		cols:1
		size: root.width, root.height
		GridLayout:
			cols:2
			
			Label:
				text: "Item Name: "
					
			TextInput:
				id: itemName
				multiline: False
					
			Label:
				text: "Quantity: "
					
			TextInput:
				id: quantity
				multiline: False
					
			Label:
				text: "Expiration Date: "
					
			TextInput:
				id: expirationDate
				multiline: False
			
			Label:
				text: "Storage Location: "
					
			TextInput:
				id: storageLocation
				multiline: False

		Button:
			text:"Submit"
			#on_press: root.function call()
		Button:
			text:"Back"
			on_press: root.manager.current = 'inventory' 
	
	
<DeleteItem>
	
	itemName:itemName                #for python code : for kivy code
	quantity:quantity        		 #for python code : for kivy code
	storageLocation:storageLocation  #for python code : for kivy code

	GridLayout:
		cols:1
		size: root.width, root.height
		GridLayout:
			cols:2
			
			Label:
				text: "Item Name: "
					
			TextInput:
				id: itemName
				multiline: False
					
			Label:
				text: "Quantity: "
					
			TextInput:
				id: quantity
				multiline: False
			
			Label:
				text: "Storage Location: "
					
			TextInput:
				id: storageLocation
				multiline: False
				
		Button:
			text:"Submit"
			#on_press: root.function call()
		Button:
			text:"Back"
			on_press: root.manager.current = 'inventory' 			
				
				
<ViewInventory>
	#function call to get inventory
	#back button
	
	Button:
		text:"Back"
		on_press: root.manager.current = 'inventory'

<SearchItem>
	itemName:itemName                #for python code : for kivy code
	GridLayout:
		cols:1
		size: root.width, root.height
		GridLayout:
			cols:2
			
			Label:
				text: "Item Name: "
					
			TextInput:
				id: itemName
				multiline: False

		Button:
			text:"Submit"
			#on_press: root.function call()
		Button:
			text:"Back"
			on_press: root.manager.current = 'inventory'

<ThePerfectLarder>
	BoxLayout:
        orientation: 'vertical'
	
		Button:
			text:"Back"
			on_press: root.manager.current = 'inventory'


<Trends>:
	GridLayout:
		cols:1
		size: root.width, root.height
		
			
		Spinner:
			size_hint: None, None
			size: 100, 44
			pos_hint: {'center': (.5, .5)}
			text: 'January'
			values: 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'

		Button:
			text: 'Back To Home'
			on_press: root.manager.current = 'homescreen'
	
		
<ShoppingList>:
	BoxLayout:
        orientation: 'vertical'
		
		Button:
            text: 'Back To Home'
            on_press: root.manager.current = 'homescreen'
		
	#function call
	
<ShareItems>:

	itemName:itemName                #for python code : for kivy code
	shareWith:shareWith        		 #for python code : for kivy code

	GridLayout:
		cols:1
		size: root.width, root.height
		GridLayout:
			cols:2
			
			Label:
				text: "Item Name: "
					
			TextInput:
				id: itemName
				multiline: False
					
			Label:
				text: "Share With: "
					
			TextInput:
				id: shareWith
				multiline: False
		
		Button:
            text: 'Send Notification'
            on_press: root.manager.current = 'homescreen'
			#function call to notifications
		
		Button:
            text: 'Back To Home'
            on_press: root.manager.current = 'homescreen'
""")

class HomeScreen(Screen):    # Main screen after login
    pass
	
class Profile(Screen):	#part of main menu	
    pass
	
class Recipes(Screen):  #part of main menu	
    pass
	
class Inventory(Screen):  #part of main menu	
    pass
	
class Trends(Screen):  #part of main menu	
    pass
	
class ShoppingList(Screen):  #part of main menu	
    pass

class ShareItems(Screen):  #part of main menu	
    pass
	
class ManagePL(Screen):     #part of the user profile
    pass

class EditCreateProfile(Screen):      #part of the user profile
    pass

class SetupEditNotification(Screen):   #part of the user profile
    pass
	
class AddRecipe(Screen):         #part of recipes
    pass
	
class GetRecipe(Screen):          #part of recipes
    pass
	
class AddItem(Screen):            #part of inventory
    pass
	
class DeleteItem(Screen):        #part of inventory
    pass

class ViewInventory(Screen):      #part of inventory
    pass

class SearchItem(Screen):         #part of inventory
    pass

class ThePerfectLarder(Screen):   #part of inventory
	pass	
	
screenManager = ScreenManager()
screenManager.add_widget(UserLogin(name="userlogin"))
screenManager.add_widget(HomeScreen(name="homescreen"))
screenManager.add_widget(Profile(name="profile"))
screenManager.add_widget(Recipes(name="recipes"))
screenManager.add_widget(Inventory(name="inventory"))
screenManager.add_widget(Trends(name="trends"))
screenManager.add_widget(ShoppingList(name="shoppinglist"))
screenManager.add_widget(ShareItems(name="shareitems"))

screenManager.add_widget(ManagePL(name="managepl"))
screenManager.add_widget(EditCreateProfile(name="editcreateprofile"))
screenManager.add_widget(SetupEditNotification(name="setupeditnotification"))

screenManager.add_widget(AddRecipe(name="addrecipe"))
screenManager.add_widget(GetRecipe(name="getrecipe"))

screenManager.add_widget(AddItem(name="additem"))
screenManager.add_widget(DeleteItem(name="deleteitem"))
screenManager.add_widget(ViewInventory(name="viewinventory"))
screenManager.add_widget(SearchItem(name="searchitem"))
screenManager.add_widget(ThePerfectLarder(name="theperfectlarder"))

#must have on start and build
class testApp (App):
    def on_start(self):
        pass
    
    def build(self):
        return screenManager
		
if __name__ == "__main__":
    testApp().run()