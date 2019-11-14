# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 

# setup GUI (kivy)

import kivy

kivy.require('1.11.1')
from kivy.config import Config

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.app import App
# Config.set('kivy', 'keyboard_mode','systemandmulti')
# Must have to do requests/work with json data
import json
import requests
#import socketio


class Login(Screen):
    userName = ObjectProperty(None)
    userPassword = ObjectProperty(None)

    # def __init__(self, name):
    #    super().__init__()

    nameContent = GridLayout(cols=1)
    nameContent.add_widget(Label(text='The username you entered is invalid.'))
    nameButton = Button(text='OK')
    nameContent.add_widget(nameButton)
    userNamePopup = Popup(title='Invalid Username', content=nameContent, auto_dismiss=False, size_hint=(.8, .2))
    nameButton.bind(on_press=userNamePopup.dismiss)
    
    passContent = GridLayout(cols=1)
    passContent.add_widget(Label(text='The password you entered was incorrect.'))
    passButton = Button(text='OK')
    passContent.add_widget(passButton)
    userPassPopup = Popup(title='Incorrect Password', content=passContent, auto_dismiss=False, size_hint=(.85, .2))
    passButton.bind(on_press=userPassPopup.dismiss)

    svrContent = GridLayout(cols=1)
    svrContent.add_widget(Label(text='Cannot connect to Server'))
    svrButton = Button(text='OK')
    svrContent.add_widget(svrButton)
    svrPopup = Popup(title='Cannot Connect', content=svrContent, auto_dismiss=False, size_hint=(.85, .2))
    svrButton.bind(on_press=svrPopup.dismiss)
    
    nameEmptyContent = GridLayout(cols=1)
    nameEmptyContent.add_widget(Label(text='The username field  cannot be empty.'))
    nameEmptyButton = Button(text='OK')
    nameEmptyContent.add_widget(nameEmptyButton)
    nameEmptyPopup = Popup(title='Empty input in Username', content=nameEmptyContent, auto_dismiss=False, size_hint=(.8, .2))
    nameEmptyButton.bind(on_press=nameEmptyPopup.dismiss)
    
    passWordEmptyContent = GridLayout(cols=1)
    passWordEmptyContent.add_widget(Label(text='The password field cannot be empty.'))
    passWordEmptyButton = Button(text='OK')
    passWordEmptyContent.add_widget(passWordEmptyButton)
    passWordEmptyPopup = Popup(title='Empty input in Password', content=passWordEmptyContent, auto_dismiss=False, size_hint=(.8, .2))
    passWordEmptyButton.bind(on_press=passWordEmptyPopup.dismiss)

    def userLogin(self):
        usersName = self.ids.userName.text
        passWord = self.ids.userPassword.text
        
        if(usersName != ""):
            
            if(passWord != ""):
                # Will most likely not change for most POST requests
                headers = {'Content-Type': 'application/json'}
        
                payload = {
                    'username': usersName,
                    'password': passWord
                }
                response = None
                try:
                    response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/login', headers=headers,
                                             data=json.dumps(payload)).json()
                except Exception as e:
                    App.get_running_app().server_error(e)
        
                # response = {'data' : 'Incorrect password.'}

                # if incorrect, clear password and have them try again
                if response is not None:
                    if response['data'] == 'Successful login.':
                        App.get_running_app().userID = response['userID']
                        App.get_running_app().userMeasurement = response['measureType']
                        App.get_running_app().userNotif = response['notifPref']
                        App.get_running_app().storageLocations = json.loads(response['locations'])['locations']
                        self.ids.userName.text = ""
                        self.ids.userPassword.text = ""
                        self.manager.current = 'homescreen'

                        #sio = socketio.Client()

                    elif response['data'] == 'Invalid username.':
                        self.ids.userPassword.text = ""
                        self.userNamePopup.open()
                    elif response['data'] == 'Incorrect password.':
                        self.ids.userPassword.text = ""
                        self.userPassPopup.open()
                    elif response['data'] == 'Unable to Connect.':
                        self.svrPopup.open()
            else:
                self.passWordEmptyPopup.open()
        else:
            self.nameEmptyPopup.open()
