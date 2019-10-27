# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 


# setup GUI (kivy)

import kivy

kivy.require('1.11.1')
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.button import Button

import requests
import json

# `Profile`: Allows for account creation, editing, and deletion in the TPL server.
class Profile(Screen):
    def on_enter(self):
        pass

    # region Properties

    # The username of the authenticated user.
    username = ObjectProperty(None)

    # The authenticated user's password.
    password = ObjectProperty(None)

    # The email address of the authenticated user.
    email = ObjectProperty(None)

    # endregion

    # region Initialization

#     def __init__(self, username, password="", email=""):
#         self.username = username
#         self.password = password
#         self.email = email

    # endregion

    # TODO: Implement create user, edit user, delete user.

    # region Profile Operations

    # def createUserProfile(self):
    # send (self.userName.text, self.userPassword.text, self.userEmail.text) to database
    # self.userName.text = ""
    # self.userPassword.text = ""
    # self.userEmail.text = ""

    # def editUserProfile(self):
    # send (self.userName.text, self.userPassword.text, self.userEmail.text) to database
    # self.userName.text = ""
    # self.userPassword.text = ""
    # self.userEmail.text = ""

    # def deleteUserProfile(self):
    # send (self.userName.text, self.userPassword.text, self.userEmail.text) to database
    # self.userName.text = ""
    # self.userPassword.text = ""
    # self.userEmail.text = ""

    # endregion

class Settings(Screen):
    
    def on_pre_enter(self):
        measureType = App.get_running_app().userMeasurement
        if measureType == 0:
            self.ids.imperial.state = 'down'
        else:
            self.ids.metric.state = 'down'
            
        for i in App.get_running_app().storageLocations:
            button = Button(text=i)
            self.ids.locations.add_widget(button)
            button.bind(lambda button:self.ids.locations.remove_widget(button))
    
    def updateMeasurement(self):
        #button = 0
        #for i in ToggleButtonBehavior.get_widgets('measurements'):
        #    if i.state == 'down':
        #        button = i
        #        break
        payload = {
            'userID' : App.get_running_app().userID
        }
        if self.ids.imperial.state == 'down':
            payload['measureType'] = 0
        else:
            payload['measureType'] = 1
            
        r = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/updateMeasurementSetting', headers={'Content-Type':'application/json'}, data=json.dumps(payload)).json()
        
        if r['data'] == 'Successfully Updated.':
            self.manager.current = 'profile'
            App.get_running_app().userMeasurement = payload['measureType']


class ManagePL(Screen):  # part of the user profile
    pass


class EditCreateProfile(Screen):  # part of the user profile
    pass


class SetupEditNotification(Screen):  # part of the user profile
    pass
