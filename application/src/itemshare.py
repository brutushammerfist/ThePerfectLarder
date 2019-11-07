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
from kivy.properties import ObjectProperty
import json
import requests

class ItemShare(Screen):
	#itemName = ObjectProperty(None)
	#shareWith = ObjectProperty(None)
	
	#def shareItems(self):
		#Send (self.itemName.text, self.shareWith.text) to database
		#Do popup to show sent
		
		#clearing data field
		#self.itemName.text = ""
		#self.shareWith.text = ""
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
		
		payload = {
			'userID' : App.get_running_app().userID, 
			'currentDate': stringCurrent,
			'currentWeekAhead': string_weekAhead
		}
		response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getItemsAboutToExpire', headers=headers, data=json.dumps(payload)).json()	