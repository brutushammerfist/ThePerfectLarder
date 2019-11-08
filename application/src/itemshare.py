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
import json
import requests

class ItemShare(Screen):
	itemName = ObjectProperty(None)
	quantity = ObjectProperty(None)
	shareWith = ObjectProperty(None)
	
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

		headers = {'Content-Type' : 'application/json'}
		#API_ENDPOINT = 'http://411orangef19-mgmt.cs.odu.edu:8000/getItemsAboutToExpire'
		payload = {
			'userID' : App.get_running_app().userID,
			'currentDate' : stringCurrent,
			'currentWeekAhead' : string_weekAhead
		}
		response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getItemsAboutToExpire', headers=headers, data=json.dumps(payload)).json()
		
		if(response['data'] == "empty"):
			print("There is nothing currently about to expire")
		else:		
			print(response['data'])

	#Gather items from the user's inventory to put onto the spinner. This will require a database request.
	def populateItemSpinner(self):
		return 'Fake', 'Items', 'Haha'

	# Gather users/groups from the user's profile to put onto the spinner. This will require a database request.
	def populateGroupSpinner(self):
		return 'Fun Group', 'Unfun group', 'Cool kids'

	#Send (self.itemName.text, self.shareWith.text) to database
	def shareItems(self):

		#If successful, with whatever validation or logic will be implemented later on
		if (True):
			self.notiPopup.open()
			self.itemName.text = ""
			self.quantity.text = ""
			self.shareWith.text = ""
		else:
			print('Notification failed!')