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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import json
import requests

acceptContent = GridLayout(cols=1)
acceptContent.add_widget(Label(text='Item accepted!'))
acceptButton = Button(text='OK')
acceptContent.add_widget(acceptButton)
acceptPopup = Popup(title='Notification alert', content=acceptContent, auto_dismiss=False, size_hint=(.8, .2))
acceptButton.bind(on_press=acceptPopup.dismiss)

rejectContent = GridLayout(cols=1)
rejectContent.add_widget(Label(text='Item rejected!'))
rejectButton = Button(text='OK')
rejectContent.add_widget(rejectButton)
rejectPopup = Popup(title='Notification alert', content=rejectContent, auto_dismiss=False, size_hint=(.8, .2))
rejectButton.bind(on_press=rejectPopup.dismiss)

class Notification(Screen):
	
	def on_pre_enter(self):
		self.ids.notifications.clear_widgets()
		headers = {'Content-Type' : 'application/json'}
		#API_ENDPOINT = 'http://411orangef19-mgmt.cs.odu.edu:8000/getItemsAboutToExpire'
		print( App.get_running_app().userID)
		payload = {
			'userID' : App.get_running_app().userID,
		}
		response = None
		try:
			response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/viewAllNotification', headers=headers, data=json.dumps(payload)).json()
		except Exception as e:
			App.get_running_app().server_error(e)
			self.manager.current = 'homescreen'
		if response is not None and response['data'] != 'empty':
			for i in response['data']:
				if i['response'] is None:
					button = Button(text=i['username'] + ' would like to share ' + str(i['quantity']) + ' of ' +
									i['itemname'] + ' with you!\nPress to reply', halign='center')
					callback = lambda n: self.notificationPopup(n)
					button.notify = i
					button.bind(on_press=callback)
					self.ids.notifications.add_widget(button)
				else:
					if i['response'] == 'yes':
						button = Button(text='Someone has accepted your item!\nPress here to dismiss')
					elif i['response'] == 'no':
						button = Button(text='Someone has rejected your item!\nPress here to dismiss')
					button.response = i
					button.bind(on_press=self.removeNotification)
					self.ids.notifications.add_widget(button)
		elif response['data'] == 'empty':
			button = Button(text='No current notifications')
			self.ids.notifications.add_widget(button)

		print(response['data'])

	def removeNotification(self, btn):
		#Remove the notification from the database
		#btn.response is identical to i in the on_pre_enter function
		self.on_pre_enter()	#Refresh the list

	def notificationPopup(self, btn):
		acceptButton = Button(text='Accept Item')
		rejectButton = Button(text='Reject Item')
		cancelButton = Button(text='Cancel')
		itemContent = GridLayout(cols=1)
		buttonContent = GridLayout(cols=3)

		itemContent.add_widget(Label(text='Would you like to accept ' + str(btn.notify['quantity']) + ' of '
									 + btn.notify['itemname'] + ' from ' + btn.notify['username'] + '?'))

		rejectButton.notify = btn.notify
		rejectButton.bind(on_press=self.rejectItem)
		acceptButton.notify = btn.notify
		acceptButton.bind(on_press=self.acceptItem)
		buttonContent.add_widget(cancelButton)
		buttonContent.add_widget(rejectButton)
		buttonContent.add_widget(acceptButton)
		itemContent.add_widget(buttonContent)
		notificationPopup = Popup(title='Notification', content=itemContent, auto_dismiss=False, size_hint=(.6, .4))
		cancelButton.bind(on_press=notificationPopup.dismiss)
		notificationPopup.open()
		return

	def acceptItem(self, btn):
		#btn.notify is identical to the dict i in on_pre_enter; i.e. btn.notify['itemname'] is the name of the item
		#backend stuff here
		def on_pre_enter(self):
			payload1 = {
			'userID' : App.get_running_app().userID,
			}
			pass
		if True:
			acceptPopup.open()
			btn.parent.parent.parent.parent.parent.dismiss()	#Dismiss previous popup
			self.on_pre_enter()	#Refresh list
		else:
			return
			#Failed to accept
		return

	def rejectItem(self, btn):
		# btn.notify is identical to the dict i in on_pre_enter; i.e. btn.notify['itemname'] is the name of the item
		# backend stuff here
		def on_pre_enter(self):
		payload2 = {
			'userID' : App.get_running_app().userID,
			'itemId': btn.notify['itemId']
			}
			response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/rejectItem', headers=headers, data=json.dumps(payload2)).json()
			print(reponse['data'])
		if True:
			rejectPopup.open()
			btn.parent.parent.parent.parent.parent.dismiss()	#Dismiss previous popup
			self.on_pre_enter()	#Refresh list
		else:
			return
			#Failed to reject
		return