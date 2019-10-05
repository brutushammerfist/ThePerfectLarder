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

class ItemShare(Screen):
	pass
	
	#itemName = ObjectProperty(None)
	#shareWith = ObjectProperty(None)
	
	#def shareItems(self):
		#Send (self.itemName.text, self.shareWith.text) to database
		#Do popup to show sent
		
		#clearing data field
		#self.itemName.text = ""
		#self.shareWith.text = ""