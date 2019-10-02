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

class Inventory(Screen):
	pass
	
	itemName = ObjectProperty(None)
	quantity = ObjectProperty(None)
	expirationDate = ObjectProperty(None)
	storageLocation = ObjectProperty(None)
	
	def addItems (self):
	
		headers = {'Content-Type' : 'application/json'}
        
		payload = {
            'itemName' : self.ids.itemName.text,
            'quantity' : self.ids.quantity.text,
			'expiration' : self.ids.expirationDate.text,
            'storage' : self.ids.storageLocation.text
        }
        
		response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/addItem', headers=headers, data=json.dumps(payload)).json()
        
		#clearing input text feild
		self.itemName.text = ""
		self.quantity.text = ""
		self.expirationDate.text = ""
		self.storageLocation.text = ""
	
	
	def deleteItems(self):
		
		headers = {'Content-Type' : 'application/json'}
        
		payload = {
            'itemName' : self.ids.itemName.text,
            'quantity' : self.ids.quantity.text,
            'storage' : self.ids.storageLocation.text
        }
		
		response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/delItem', headers=headers, data=json.dumps(payload)).json()
		
		#clearing input text feild
		self.itemName.text = ""
		self.quantity.text = ""
		self.storageLocation.text = ""
	
	
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