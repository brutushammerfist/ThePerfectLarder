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
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

# Must have to do requests/work with json data
import json
import requests

class Login(Screen):
    userName = ObjectProperty(None)
    userPassword = ObjectProperty(None)
    
    #def __init__(self, name):
    #    super().__init__()
        
    nameContent = GridLayout(cols=1)
    nameContent.add_widget(Label(text='The username you entered is invalid.'))
    nameButton = Button(text='OK')
    nameContent.add_widget(nameButton)
    userNamePopup = Popup(title='Invalid Username', content=nameContent, auto_dismiss=False)
    nameButton.bind(on_press=userNamePopup.dismiss)
    
    passContent = GridLayout(cols=1)
    passContent.add_widget(Label(text='The password you entered was incorrect.'))
    passButton = Button(text='OK')
    passContent.add_widget(passButton)
    userPassPopup = Popup(title='Incorrect Password', content=passContent, auto_dismiss=False)
    passButton.bind(on_press=userPassPopup.dismiss)
    
    def userLogin(self):
        # Will most likely not change for most POST requests
        headers = {'Content-Type' : 'application/json'}
        
        payload = {
            'username' : self.ids.userName.text,
            'password' : hash(self.ids.userPassword.text)
        }
        
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/login', headers=headers, data=json.dumps(payload)).json()
        
        #response = {'data' : 'Incorrect password.'}
        
        # if incorrect, clear password and have them try again
        if response['data'] == 'Successful login.':
            #Move to next screen
            self.manager.current = 'homescreen'
        elif response['data'] == 'Invalid username.':
            self.ids.userPassword.text = ""
            self.userNamePopup.open()
        elif response['data'] == 'Incorrect password.':
            self.ids.userPassword.text = ""
            self.userPassPopup.open()
