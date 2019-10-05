# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 



#setup GUI (kivy)

import kivy
kivy.require('1.11.1')
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class Profile(Screen):
	pass

	#userName = ObjectProperty(None) 
	#userPassword = ObjectProperty(None)
	#userEmail = ObjectProperty(None)


	#def createUserProfile(self):
		#send (self.userName.text, self.userPassword.text, self.userEmail.text) to database
		#self.userName.text = ""
		#self.userPassword.text = ""
		#self.userEmail.text = ""
		
	
	#def editUserProfile(self):
		#send (self.userName.text, self.userPassword.text, self.userEmail.text) to database
		#self.userName.text = ""
		#self.userPassword.text = ""
		#self.userEmail.text = ""
		
	#def deleteUserProfile(self):
		#send (self.userName.text, self.userPassword.text, self.userEmail.text) to database
		#self.userName.text = ""
		#self.userPassword.text = ""
		#self.userEmail.text = ""

class ManagePL(Screen):     #part of the user profile
    pass
    
    
class EditCreateProfile(Screen):      #part of the user profile
    pass
    

class SetupEditNotification(Screen):   #part of the user profile
    pass