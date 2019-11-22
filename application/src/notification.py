# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 


#setup GUI(kivy)

import kivy
from kivy.app import App
kivy.require('1.11.1')
from kivy.uix.screenmanager import Screen
import json
import requests

class Notification(Screen):
	
	def on_pre_enter(self):
		headers = {'Content-Type' : 'application/json'}
		#API_ENDPOINT = 'http://411orangef19-mgmt.cs.odu.edu:8000/getItemsAboutToExpire'
		print( App.get_running_app().userID)
		payload = {
			'userID' : App.get_running_app().userID,
		}
		
		response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/viewAllNotification', headers=headers, data=json.dumps(payload)).json()
		print(reponse['data'])
class NewNotification(Screen):
	pass