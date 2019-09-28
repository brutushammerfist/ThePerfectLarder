# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 


#setup GUI(kivy)

import kivy
kivy.require('1.11.1')
from kivy.uix.screenmanager import Screen

class Inventory(Screen):
	pass

	#def addItems (item, quantity, userInventory, storageLocation, expiration date)
		#update the users inventory with the item (attributes)
		#if item is already in the inventory update the quantity
	
	
	#def deleteItems(item, quantity, userInventory, storageLocation)
		# update the users inventory with the item
		# if the items quantity to be deleted is less than the quantity in the 
		# inventory update the quantity 
	
	
	#def viewInventory(userInventory)
		#display the inventory to the userInventory
		
		
	#def searchForItem(item, usersInventory)
		#serch the userInventory for the item
		#display to user


	#def thePerfectLarder(foodUseTrends)
		#display to user what items, based on trends that 
		#they should keep on hand at all times
		
	#server side	
	#def checkItemExpiration(date, usersInventory)
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