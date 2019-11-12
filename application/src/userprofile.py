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
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

import requests
import json


nameEmptyContent = GridLayout(cols=1)
nameEmptyContent.add_widget(Label(text='The username field  cannot be empty.'))
nameEmptyButton = Button(text='OK')
nameEmptyContent.add_widget(nameEmptyButton)
nameEmptyPopup = Popup(title='Empty input in Username', content=nameEmptyContent, auto_dismiss=False, size_hint=(.8, .2))
nameEmptyButton.bind(on_press=nameEmptyPopup.dismiss)


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

#class StorageLocation(GridLayout):
#    def deleteSelf(self):
#        self.parent.remove_widget(self)
    
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
            button.bind(on_press=lambda i:self.removeLocation(i))
            
    def addLocation(self):
        if self.ids.newLoc.text != "":
            loc = self.ids.newLoc.text
            button = Button(text=loc)
            self.ids.locations.add_widget(button)
            button.bind(on_press=lambda loc:self.removeLocation(loc))
            
    def removeLocation(self, location):
        #self.ids.locations.children.pop(0)
        num = 0
        for i in self.ids.locations.children:
            if i.text == location:
                self.ids.locations.children.pop(num)
                break
            else:
                num += 1
    
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

class SharedUser(Screen):
    def on_pre_enter(self):
    
        payload = {
        'userID': App.get_running_app().userID
        }
        r = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/displayAllSharedUser', headers={'Content-Type':'application/json'}, data=json.dumps(payload)).json()
        if(r['data'] =="empty"):
            print("No other user is currently in your share List")
        else:
            print(r['data'])
class AddUserToShareList(Screen):
    def submitUser(self):
        usersName = self.ids.usernameRecieved.text
        
        passAContent = GridLayout(cols=1)
        passAContent.add_widget(Label(text="Successfully Added " + usersName +" to your shared List"))
        psButton = Button(text='OK')
        passAContent.add_widget(psButton)
        userAPassPopup = Popup(title="User Added Successfully", content=passAContent, auto_dismiss=False, size_hint=(.8, .2))
        psButton.bind(on_press=userAPassPopup.dismiss) 
        
        fail3AContent = GridLayout(cols=1)
        fail3AContent.add_widget(Label(text="The username " + usersName +" has already been added to the shared List"))
        fail3AButton = Button(text='OK')
        fail3AContent.add_widget(fail3DButton)
        userAfail3Popup = Popup(title="Not logical to do", content=fail3DContent, auto_dismiss=False, size_hint=(.8, .2))
        fail3AButton.bind(on_press=userAfail3Popup.dismiss)
        
        fail2AContent = GridLayout(cols=1)
        fail2AContent.add_widget(Label(text="You can not add yourself to the shared List"))
        fail2AButton = Button(text='OK')
        fail2AContent.add_widget(fail2AButton)
        userAfail2Popup = Popup(title="Not logical to do", content=fail2AContent, auto_dismiss=False, size_hint=(.8, .2))
        fail2AButton.bind(on_press=userAfail2Popup.dismiss)
        
        fail1AContent = GridLayout(cols=1)
        fail1AContent.add_widget(Label(text="The username " + usersName +" does not exist in the database"))
        fail1AButton = Button(text='OK')
        fail1AContent.add_widget(fail1AButton)
        userAfail1Popup = Popup(title="Not logical to do", content=fail1AContent, auto_dismiss=False, size_hint=(.8, .2))
        fail1AButton.bind(on_press=userAfail1Popup.dismiss)
        
        if(usersName != ""):
            payload ={
            'userID': App.get_running_app().userID,
            'userName': usersName
            }
            r = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/addToShareList', headers={'Content-Type':'application/json'}, data=json.dumps(payload)).json()
            print(r['data'])
            if(r['data'] == "1"):
                userAfail1Popup.open()
                self.ids.usernameRecieved.text =""
            elif(r['data'] == "2"):
                userAfail2Popup.open()
                self.ids.usernameRecieved.text =""
            elif(r['data'] == "3"):
                userAfail3Popup.open()
                self.ids.usernameRecieved.text =""
            else:
                userAPassPopup.open()
                self.ids.usernameRecieved.text =""
        else:
            nameEmptyPopup.open()
class DeleteSharedUser(Screen):
    def deleteUser(self):
        usersName = self.ids.usernameRecieved.text
        
        passDContent = GridLayout(cols=1)
        passDContent.add_widget(Label(text="Successfully deleted " + usersName +" from your shared List"))
        passDButton = Button(text='OK')
        passDContent.add_widget(passDButton)
        userDPassPopup = Popup(title="User Deleted Successfully", content=passDContent, auto_dismiss=False, size_hint=(.8, .2))
        passDButton.bind(on_press=userDPassPopup.dismiss)    
        
        fail3DContent = GridLayout(cols=1)
        fail3DContent.add_widget(Label(text="User name " + usersName + " is  not on the list. Why delete nothing?!"))
        fail3DButton = Button(text='OK')
        fail3DContent.add_widget(fail3DButton)
        userDfail3Popup = Popup(title="Not logical to do", content=fail3DContent, auto_dismiss=False, size_hint=(.8, .2))
        fail3DButton.bind(on_press=userDfail3Popup.dismiss)
        
        
        fail2DContent = GridLayout(cols=1)
        fail2DContent.add_widget(Label(text="Invalid input your username " + usersName +" can not be in the shared list. Why delete nothing ?!"))
        fail2DButton = Button(text='OK')
        fail2DContent.add_widget(fail2DButton)
        userDfail2Popup = Popup(title="Not logical to do", content=fail2DContent, auto_dismiss=False, size_hint=(.8, .2))
        fail2DButton.bind(on_press=userDfail2Popup.dismiss)
        
        fail1DContent = GridLayout(cols=1)
        fail1DContent.add_widget(Label(text="The username " + usersName +" does not exist in the database"))
        fail1DButton = Button(text='OK')
        fail1DContent.add_widget(fail1DButton)
        userDfail2Popup = Popup(title="Not logical to do", content=fail1DContent, auto_dismiss=False, size_hint=(.8, .2))
        fail1DButton.bind(on_press=userDfail2Popup.dismiss)
        
        if(usersName != ""):
            payload ={
            'userID': App.get_running_app().userID,
            'userName': usersName
            }
            r = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/removeFromShareList', headers={'Content-Type':'application/json'}, data=json.dumps(payload)).json()
            print(r['data'])
            if(r['data'] =="1"):
                userDfail2Popup.open()
                self.ids.usernameRecieved.text =""
            elif(r['data'] =="2"):
                userDfail2Popup.open()
                self.ids.usernameRecieved.text =""
            elif(r['data'] =="3" ):
                userDfail3Popup.open()
                self.ids.usernameRecieved.text =""
            else:
                userDPassPopup.open()
                self.ids.usernameRecieved.text =""
        else:
            nameEmptyPopup.open()