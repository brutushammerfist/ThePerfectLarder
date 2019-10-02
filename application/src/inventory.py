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
            'itemName' : self.ids.itemName.text,
            'quantity' : self.ids.quantity.text,
            'storage' : self.ids.storageLocation.text
        }
		
		response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/delItem', headers=headers, data=json.dumps(payload)).json()
		
		if response['data'] == 'Item Deleted.':
			self.delItemPopup.open()
			self.itemName.text = ""
			self.quantity.text = ""
			self.storageLocation.text = ""
		else:
			self.itemNotdelPopup.open()
	
	#def viewInventory(self):
		#display the inventory to the userInventory
		
		
	#def searchForItem(self):
		#Send(self.itemName.text) to database
		#display item attributes
		#self.itemName.text = ""

	#def thePerfectLarder(self):
		#display to user what items, based on trends that 
		#they should keep on hand at all times
		
	#server side	
	#def checkItemExpiration(self):
	 #check item expiration dates
	 # if within (#) days send item to notifications (expiringItems)
	 
	
class AddItem(Screen):            #part of inventory
    pass
	
class DeleteItem(Screen):        #part of inventory
    pass

class ViewInventory(Screen):      #part of inventory
    pass

class SearchItem(Screen):         #part of inventory
    pass