# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 


#setup GUI(kivy)

import kivy
kivy.require('1.11.1')
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class Inventory(Screen):
	pass
	
	itemName = ObjectProperty(None)
	quantity = ObjectProperty(None)
	expirationDate = ObjectProperty(None)
	storageLocation = ObjectProperty(None)
	#userID = ObjectProperty(None) 
	
class AddItem(Screen):            #part of inventory
		
		def addItems (self):
	
			#popup to confirm item was added
			nameContent = GridLayout(cols=1)
			nameContent.add_widget(Label(text= self.itemName.text + ' added to your inventory'))
			nameButton = Button(text='OK')
			nameContent.add_widget(nameButton)
			addItemPopup = Popup(title='Added Item', content=nameContent, auto_dismiss=False)
			nameButton.bind(on_press=addItemPopup.dismiss)
			
			#popup to let the user know the item was not added 
			nameContent = GridLayout(cols=1)
			nameContent.add_widget(Label(text= self.itemName.text + ' not added to your inventory'))
			nameButton = Button(text='OK')
			nameContent.add_widget(nameButton)
			itemNotaddedPopup = Popup(title='Item Not Added', content=nameContent, auto_dismiss=False)
			nameButton.bind(on_press=itemNotaddedPopup.dismiss)
			
			headers = {'Content-Type' : 'application/json'}
			
			payload = {
				'itemName' : self.ids.itemName.text,
				'quantity' : self.ids.quantity.text,
				'expiration' : self.ids.expirationDate.text,
				'storage' : self.ids.storageLocation.text
			}
			
			response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/addItem', headers=headers, data=json.dumps(payload)).json()
			
			if response['data'] == 'Item added.':
				self.addItemPopup.open()
				self.itemName.text = ""
				self.quantity.text = ""
				self.expirationDate.text = ""
				self.storageLocation.text = ""
			else:
				self.itemNotaddedPopup.open()
	
class DeleteItem(Screen):        #part of inventory
    
		def deleteItems(self):
	
			#popup to confirm item was deleted
			nameContent = GridLayout(cols=1)
			nameContent.add_widget(Label(text= self.itemName.text + ' was deleted from your inventory'))
			nameButton = Button(text='OK')
			nameContent.add_widget(nameButton)
			delItemPopup = Popup(title='Deleted Item', content=nameContent, auto_dismiss=False)
			nameButton.bind(on_press=delItemPopup.dismiss)
			
			#popup to let the user know the item was not deleted 
			nameContent = GridLayout(cols=1)
			nameContent.add_widget(Label(text= self.itemName.text + ' was not deleted from your inventory'))
			nameButton = Button(text='OK')
			nameContent.add_widget(nameButton)
			itemNotdelPopup = Popup(title='Item Not Deleted', content=nameContent, auto_dismiss=False)
			nameButton.bind(on_press=itemNotdelPopup.dismiss)
			
			headers = {'Content-Type' : 'application/json'}
			
			payload = {
				'itemname' : self.ids.itemName.text,
				'quantity' : self.ids.quantity.text,
                'measurement' : self.ids.measurement.text,
				'location' : self.ids.storageLocation.text
			}
			
			response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/delItem', headers=headers, data=json.dumps(payload)).json()
			
			if response['data'] == 'Item Deleted.':
				self.delItemPopup.open()
				self.itemName.text = ""
				self.quantity.text = ""
				self.storageLocation.text = ""
			else:
				self.itemNotdelPopup.open()

class ViewInventory(Screen):      #part of inventory
    
		def viewInventory(self):   #need to pass in the user id after login
	
			
			#user inventory popup to show inventory (needs to be scrollable)
			nameContent = GridLayout(cols=1)
			nameContent.add_widget(Label(text= 'Display the user inventory'))
			nameButton = Button(text='OK')
			nameContent.add_widget(nameButton)
			inventoryPopup = Popup(title='Inventory', content=nameContent, auto_dismiss=False)
			nameButton.bind(on_press=inventoryPopup.dismiss)
			
			#user inventory popup to show inventory (needs to be scrollable)
			nameContent = GridLayout(cols=1)
			nameContent.add_widget(Label(text= 'Inventory Empty'))
			nameButton = Button(text='OK')
			nameContent.add_widget(nameButton)
			errorPopup = Popup(title='Inventory Empty', content=nameContent, auto_dismiss=False)
			nameButton.bind(on_press=errorPopup.dismiss)
			
			headers = {'Content-Type' : 'application/json'}
			
			payload = {
				'userid' : userID
			}
			
			response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getInventory', headers=headers, data=json.dumps(payload)).json()
			
			if response['data'] == 'Found inventory.':
				self.inventoryPopup.open()
			elif response['data'] == 'Inventory Empty.':
				self.error.popup.open()  #if inventory is empty
			

class SearchItem(Screen):         #part of inventory
    
		def searchForItem(self):
	
			#popup to confirm item was found
			nameContent = GridLayout(cols=1)
			nameContent.add_widget(Label(text= self.itemName.text)) #need to display attributes
			nameButton = Button(text='OK')
			nameContent.add_widget(nameButton)
			searchItemPopup = Popup(title='Search Item', content=nameContent, auto_dismiss=False)
			nameButton.bind(on_press=searchItemPopup.dismiss)
			
			#popup to let the user know the item was not found 
			nameContent = GridLayout(cols=1)
			nameContent.add_widget(Label(text= self.itemName.text + ' is not in your inventory'))
			nameButton = Button(text='OK')
			nameContent.add_widget(nameButton)
			itemNotFoundPopup = Popup(title='Item Not Found', content=nameContent, auto_dismiss=False)
			nameButton.bind(on_press=itemNotFoundPopup.dismiss)
			
			headers = {'Content-Type' : 'application/json'}
			
			payload = {
				'itemName' : self.ids.itemName.text
			}
			
			response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/searchItem', headers=headers, data=json.dumps(payload)).json()
			
			if response['data'] == 'Item found.':
				self.searchItemPopup.open()
				#display attributes to kivy 
			else:
				self.itemNotFoundPopup.open()
	
class PerfectLarder(Screen):

		def thePerfectLarder(self):
		
			
			#users perfect larder popup to show items to keep on hand (needs to be scrollable)
			nameContent = GridLayout(cols=1)
			nameContent.add_widget(Label(text= 'Display the user perfect larder inventory'))
			nameButton = Button(text='OK')
			nameContent.add_widget(nameButton)
			plPopup = Popup(title='Inventory', content=nameContent, auto_dismiss=False)
			nameButton.bind(on_press=plPopup.dismiss)
			
			#user inventory popup to show inventory (needs to be scrollable)
			nameContent = GridLayout(cols=1)
			nameContent.add_widget(Label(text= 'Not Enough Data'))
			nameButton = Button(text='OK')
			nameContent.add_widget(nameButton)
			errorPopup = Popup(title='Inventory Empty', content=nameContent, auto_dismiss=False)
			nameButton.bind(on_press=errorPopup.dismiss)
			
			headers = {'Content-Type' : 'application/json'}
			
			payload = {
				'userid' : userID
			}
			
			response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/perfectLarder', headers=headers, data=json.dumps(payload)).json()
			
			if response['data'] == 'PL Found.':
				self.plPopup.open()
			elif response['data'] == 'PL Empty.':
				self.error.popup.open()  #if inventory is empty
			