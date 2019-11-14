# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 


#setup GUI(kivy)

import kivy
import datetime

kivy.require('1.11.1')
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import json
import requests

class ItemShare(Screen):
	itemName = ObjectProperty(None)
	quantity = ObjectProperty(None)
	shareWith = ObjectProperty(None)
	foodItems = []
	itemToShare = -1

	notiContent = GridLayout(cols=1)
	notiContent.add_widget(Label(text='Notification sent!'))
	notiButton = Button(text='OK')
	notiContent.add_widget(notiButton)
	notiPopup = Popup(title='Notification', content=notiContent, auto_dismiss=False, size_hint=(.8, .2))
	notiButton.bind(on_press=notiPopup.dismiss)

	def on_pre_enter(self):

		todaysDate = datetime.datetime.now()
		year = todaysDate.year
		day = todaysDate.strftime("%d")
		month = todaysDate.strftime("%m")
		current =  datetime.datetime(int(year),int(month),int(day))
		week_ahead = current + datetime.timedelta(days=7)
		stringCurrent = current.strftime("%Y") + "-" + current.strftime("%m") + "-" + current.strftime("%d")
		string_weekAhead =  week_ahead.strftime("%Y") + "-" + week_ahead.strftime("%m") + "-" + week_ahead.strftime("%d")
		self.foodItems = []

		headers = {'Content-Type' : 'application/json'}
		#API_ENDPOINT = 'http://411orangef19-mgmt.cs.odu.edu:8000/getItemsAboutToExpire'
		payload = {
			'userID' : App.get_running_app().userID,
			'currentDate' : stringCurrent,
			'currentWeekAhead' : string_weekAhead
		}
		response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getItemsAboutToExpire', headers=headers, data=json.dumps(payload)).json()
		print(response['data'])
		if response['data'] != 'empty':
			for i in response['data']:
				if i['quantity'] != 0:
					self.foodItems.append(i)
			if self.foodItems:
				for a in range(0, len(self.foodItems)):
					button = Button(text=self.foodItems[a]['itemname'] + " - " + str(self.foodItems[a]['quantity'])
										 + " " + self.foodItems[a]['measurement'] + "\n" + "Expires "
										 + self.foodItems[a]['expiration'], halign='center')
					callback = lambda n: self.setItemToShare(n)
					button.itemToShare = a
					button.bind(on_press=callback)
					self.ids.shareFoodItems.add_widget(button)
			else:
				self.ids.shareFoodItems.add_widget(Button(text='No items near expiration.'))
		else:
			self.ids.shareFoodItems.add_widget(Button(text='No items near expiration.'))
		#if(response['data'] == "empty"):
		#	print("There is nothing currently about to expire")
		#else:		
		#	print(response['data'])

	#Sets the global variable and calls the function to open the popup
	def setItemToShare(self, item):
		self.itemToShare = item.itemToShare
		self.itemPopupShow(self.itemToShare)

	#Creates a new popup and displays item information.
	#Cancel closes the popup
	#Share Item will share the item via the shareItem function
	def itemPopupShow(self, index):
		shareButton = Button(text='Share Item')
		itemContent = GridLayout(cols=2, spacing=[0, 20])
		itemContent.add_widget(Label(text='Item Name: '))
		
		shareButton.maxFoodQuantity = self.foodItems[index]['quantity']
		shareButton.foodName = self.foodItems[index]['itemname']
		shareButton.foodId = self.foodItems[index]['id']
		
		itemContent.add_widget(Label(text=shareButton.foodName))
		itemContent.add_widget(Label(text='Quantity (max ' + str(self.foodItems[index]['quantity']) + '): '))
		shareButton.quanTxt = TextInput(multiline=False, font_size=65)
		itemContent.add_widget(shareButton.quanTxt)
		cancelButton = Button(text='Cancel')
		itemContent.add_widget(cancelButton)
		itemContent.add_widget(shareButton)
		itemPopup = Popup(title='Share Item', content=itemContent, auto_dismiss=False, size_hint=(.6, .4))
		cancelButton.bind(on_press=itemPopup.dismiss)
		shareButton.bind(on_press=self.shareItem)
		itemPopup.open()
		return

	#Shares the specified item to users/groups; needs global variables foodItems and itemToShare
	def shareItem(self, btn):
		quantity = btn.quanTxt.text
		print("User ID: " + str(App.get_running_app().userID))
		print("Food Name: " + btn.foodName)
		print("Quantity: " + quantity)
		print("Item ID: " +str( btn.foodId))
		print("Max Food Quantity" + str(btn.maxFoodQuantity))
		intMaxQaun = float(str( btn.foodId))
		
		fquantity = float(quantity)
		
		if(intMaxQaun == quantity):
			max = "yes"
		elif(fquantity < intMaxQaun):
			max = "no"
		else:
			
			print("You can not enter a number greater than item quantity")
		headers = {'Content-Type' : 'application/json'}
		payload = {
			'userID': App.get_running_app().userID,
			'itemID': btn.foodId,
			'quantity':fquantity,
			'max': max
		}	
		response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/shareFoodItemToUser', headers=headers, data=json.dumps(payload)).json()
		print(response)
		
		return