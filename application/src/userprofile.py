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
        self.manager.transition.direction = 'left'

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
        self.ids.locations.clear_widgets()
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
            if i.text == location.text:
                self.ids.locations.children.pop(num)
                break
            else:
                num += 1

    def updateProfilePreferences(self):

        updateMeasurementResult = self.updateMeasurement()
        updateStorageLocationsResult = self.updateStorageLocations()

        if(updateMeasurementResult == False or updateStorageLocationsResult == False):
            text = "Unable to update user preferences"
            title = "Error"

        else:
            text = "User preferences have been updated!"
            title = "Success!"


        updateProfile = GridLayout(cols=1)
        updateProfile.add_widget(Label(text=text))
        updateProfileButton = Button(text='OK')
        updateProfile.add_widget(updateProfileButton)
        updateProfilePopup = Popup(title=title, content=updateProfile, auto_dismiss=False, size_hint=(.8, .2))
        updateProfileButton.bind(on_press=updateProfilePopup.dismiss)

        updateProfilePopup.open()

    def updateStorageLocations(self):
        payload = {
            'userID' : App.get_running_app().userID,
            'locations' : []
        }

        for i in self.ids.locations.children:
            payload['locations'].append(i.text)

        headers = {'Content-Type': 'application/json'}

        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/updateStorageLocations', headers=headers, data=json.dumps(payload)).json()
        if response['data'] == 'Successfully Updated.':
            App.get_running_app().storageLocations = payload['locations']
            return True
        else:
            return False

    
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
            App.get_running_app().userMeasurement = payload['measureType']
            return True
        else:
            return False


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
        r = None
        try:
            r = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/displayAllSharedUser',
                              headers={'Content-Type':'application/json'}, data=json.dumps(payload)).json()
        except Exception as e:
            App.get_running_app().server_error(e)
            self.manager.current = 'profile'
        if r is not None and r['data'] == "empty":
            self.ids.shareList.add_widget(Button(text='No users in share list.'))
            print("No other user is currently in your share List")
        else:
            for a in range(0, len(r['data'])):
                button = Button(text=r['data'][a]['name'] + '\n(' + r['data'][a]['username'] + ')', halign='center')
                callback = lambda n: self.delShareUserPopup(n)
                button.nameOfUser = r['data'][a]['name']
                button.username = r['data'][a]['username']
                button.bind(on_press=callback)
                self.ids.shareList.add_widget(button)
            print(r['data'])

    def submitUser(self):
        usersName = self.ids.usernameReceived.text

        passAContent = GridLayout(cols=1)
        passAContent.add_widget(Label(text="Successfully Added " + usersName + " to your shared List"))
        psButton = Button(text='OK')
        passAContent.add_widget(psButton)
        userAPassPopup = Popup(title="User Added Successfully", content=passAContent, auto_dismiss=False,
                               size_hint=(.8, .2))
        psButton.bind(on_press=userAPassPopup.dismiss)

        fail3AContent = GridLayout(cols=1)
        fail3AContent.add_widget(Label(text="The username " + usersName + " has already been added to the shared List"))
        fail3AButton = Button(text='OK')
        fail3AContent.add_widget(fail3AButton)
        userAfail3Popup = Popup(title="Not logical to do", content=fail3AContent, auto_dismiss=False,
                                size_hint=(.8, .2))
        fail3AButton.bind(on_press=userAfail3Popup.dismiss)

        fail2AContent = GridLayout(cols=1)
        fail2AContent.add_widget(Label(text="You can not add yourself to the shared List"))
        fail2AButton = Button(text='OK')
        fail2AContent.add_widget(fail2AButton)
        userAfail2Popup = Popup(title="Not logical to do", content=fail2AContent, auto_dismiss=False,
                                size_hint=(.8, .2))
        fail2AButton.bind(on_press=userAfail2Popup.dismiss)

        fail1AContent = GridLayout(cols=1)
        fail1AContent.add_widget(Label(text="The username " + usersName + " does not exist in the database"))
        fail1AButton = Button(text='OK')
        fail1AContent.add_widget(fail1AButton)
        userAfail1Popup = Popup(title="Not logical to do", content=fail1AContent, auto_dismiss=False,
                                size_hint=(.8, .2))
        fail1AButton.bind(on_press=userAfail1Popup.dismiss)

        if (usersName != ""):
            payload = {
                'userID': App.get_running_app().userID,
                'userName': usersName
            }
            r = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/addToShareList',
                              headers={'Content-Type': 'application/json'}, data=json.dumps(payload)).json()
            print(r['data'])
            if (r['data'] == "1"):
                userAfail1Popup.open()
                self.ids.usernameReceived.text = ""
            elif (r['data'] == "2"):
                userAfail2Popup.open()
                self.ids.usernameReceived.text = ""
            elif (r['data'] == "3"):
                userAfail3Popup.open()
                self.ids.usernameReceived.text = ""
            else:
                userAPassPopup.open()
                self.ids.usernameReceived.text = ""
                self.ids.shareList.clear_widgets()
                self.on_pre_enter()
        else:
            nameEmptyPopup.open()


    def delShareUserPopup(self, btn):
        itemContent = GridLayout(cols=1, spacing=[0, 20])
        itemContent.add_widget(Label(text='Are you sure you want to delete ' + btn.nameOfUser + '(' + btn.username +
                                     ')?'))
        buttonContent = GridLayout(cols=2, spacing=[10, 0])
        delButton = Button(text='Delete User')
        delButton.username = btn.username
        cancelButton = Button(text='Cancel')
        buttonContent.add_widget(cancelButton)
        buttonContent.add_widget(delButton)
        itemContent.add_widget(buttonContent)
        delPopup = Popup(title='Delete User', content=itemContent, auto_dismiss=False, size_hint=(.6, .4))
        cancelButton.bind(on_press=delPopup.dismiss)
        delButton.bind(on_press=self.delShareUser)
        delPopup.open()
        return

    def delShareUser(self, btn):
        passDContent = GridLayout(cols=1)
        passDContent.add_widget(Label(text="Successfully deleted " + btn.username + " from your shared List"))
        passDButton = Button(text='OK')
        passDContent.add_widget(passDButton)
        userDPassPopup = Popup(title="User Deleted Successfully", content=passDContent, auto_dismiss=False, size_hint=(.8, .2))
        passDButton.bind(on_press=userDPassPopup.dismiss)

        payload = {
            'userID': App.get_running_app().userID,
            'userName': btn.username
        }
        r = None
        try:
            r = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/removeFromShareList',
                              headers={'Content-Type': 'application/json'}, data=json.dumps(payload)).json()
        except Exception as e:
            App.get_running_app().server_error(e)

        if r is not None:
            btn.parent.parent.parent.parent.parent.dismiss()
            userDPassPopup.open()
            self.ids.shareList.clear_widgets()
            self.on_pre_enter()
        return

'''class AddUserToShareList(Screen):
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
        fail3AContent.add_widget(fail3AButton)
        userAfail3Popup = Popup(title="Not logical to do", content=fail3AContent, auto_dismiss=False, size_hint=(.8, .2))
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
            r = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/removeFromShareList',
                              headers={'Content-Type':'application/json'}, data=json.dumps(payload)).json()
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
            nameEmptyPopup.open()'''
