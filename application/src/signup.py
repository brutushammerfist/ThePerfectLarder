import kivy
import re

kivy.require('1.11.1')
from kivy.config import Config

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from enum import Enum
from kivy.app import App
from kivy.properties import ObjectProperty

import json
import requests


# Config.set('kivy', 'keyboard_mode','systemandmulti')

# `PasswordValidationResponse`: Defines a response from the password validator.
class PasswordValidationResponse(Enum):
    VALID = 0
    NOTENTERED = 1
    CONFIRMNOTENTERED = 2
    NOTMATCHING = 3


# `SignUp`: The sign up screen.
class SignUp(Screen):
    # Popup to prompt for password re-input
    passContent = GridLayout(cols=1)
    passContent.add_widget(Label(text='Passwords do not match.'))
    passButton = Button(text='OK')
    passContent.add_widget(passButton)
    userPassPopup = Popup(title='Check your Password', content=passContent, auto_dismiss=False)
    passButton.bind(on_press=userPassPopup.dismiss)
    
    shelfLifeContent = GridLayout(cols=1)
    shelfLifeContent.add_widget(Label(text='Shelf life recommendations may \nvary in accuracy depending on \nstorage location and environmental \nfactors.'))
    shelfLifeButton = Button(text='OK', size_hint=(.4, .2))
    shelfLifeContent.add_widget(shelfLifeButton)
    shelfLifePopup = Popup(title='Warning', content=shelfLifeContent, auto_dismiss=False, size_hint=(.85, .4))
    shelfLifeButton.bind(on_press=shelfLifePopup.dismiss)

    # Popup to notify the user the registration was successful and to redirect them to the login page
    regContent = GridLayout(cols=1)
    regContent.add_widget(Label(text='Registration successful!'))
    regButton = Button(text='OK')
    regContent.add_widget(regButton)
    regPopup = Popup(title='Registration Confirmation Status', content=regContent, auto_dismiss=False, size_hint=(.85, .2))
    regButton.bind(on_press=regPopup.dismiss)
    regButton.bind(on_press=shelfLifePopup.open)

    # Popup to prompt for email re-input
    emailContent = GridLayout(cols=1)
    emailContent.add_widget(Label(text='Specified email address is not valid.'))
    emailButton = Button(text='OK')
    emailContent.add_widget(emailButton)
    userEmailPopup = Popup(title='Check your Email Address', content=emailContent, auto_dismiss=False)
    emailButton.bind(on_press=userEmailPopup.dismiss)
    EMAIL_REGEX = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    LE = Label()
    LPM = Label()
    LPE = Label()
    LUE = Label()
    SRC = Label()
    ResponseErrorMessage = Label()
    

    # region Field Validation
    # `checkEmailValidity`: Verifies a given email.
    def checkEmailValidity(self, email):
        if re.search(self.EMAIL_REGEX, email):
            return True
        else:
            return False

    # `validatePasswords`: Validates values from a password and confirm password text field.
    @staticmethod
    def validatePasswords(password, confirmPassword):
        if password == "":
            return PasswordValidationResponse.NOTENTERED
        if confirmPassword == "":
            return PasswordValidationResponse.CONFIRMNOTENTERED
        if password != confirmPassword:
            return PasswordValidationResponse.NOTMATCHING
        return PasswordValidationResponse.VALID

    # endregion
    def validatePhonenumber(self,phoneTemp):
        if phoneTemp.isdigit():
            return True
        else:
            return False

    # region Widgets
    @staticmethod
    def widgetWithMessage(message):
        widget = Label(text=message)
        widget.font_size = 45
        widget.bold = True
        widget.color = (1, 0, 0,0.75)
        widget.pos_hint = {"top":.66}
        return widget

    # endregion
    @staticmethod
    def widgetWithSuccessMessage(message):
        widget = Label(text=message)
        widget.font_size = 45
        widget.bold = True
        widget.color = (0, 1, 0,0.75)
        widget.pos_hint = {"top":.66}
        return widget
    # region Widgets
    # region Account Creation

    # `createAccount`: Validates the user entered account data. Alerts user if invalid, sends to server if valid.
    def createAccount(self):

        # Validate user inputs from text fields.
        name = self.ids.name.text
        userName = self.ids.userName.text
        userEmail = self.ids.userEmail.text
        phone = self.ids.phone.text
        userPassword = self.ids.userPassword.text
        userPasswordConfirm = self.ids.userPasswordConfirm.text
        self.remove_widget(self.LE)
        self.remove_widget(self.LPM)
        self.remove_widget(self.LPE)

        #Validate name
        if name != "":
        # Validate email.
            if self.checkEmailValidity(userEmail):
    
                if phone != "":
                    # Validate username.
                    passwordValidation = self.validatePasswords(userPassword, userPasswordConfirm)
                    phoneNumMustBeInt = self.validatePhonenumber(phone)
                    if(phoneNumMustBeInt != False):
                            # Validate password fields.
                    
                        if userName != "":
                            if passwordValidation == PasswordValidationResponse.VALID:
                                # Password combo was valid, send to server.
                                print("All account data valid, sending payload to server.")
            
                                headers = {'Content-Type' : 'application/json'}
            
                                payload = {
                                    'name' : name,
                                    'useremail' : userEmail,
                                    'phone' : phone,
                                    'username' : userName,
                                    'password' : userPassword
                                 }
                                response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/signUp', headers=headers, data=json.dumps(payload)).json()
                                self.remove_widget(self.LE)
                                self.remove_widget(self.LPE)
                                self.remove_widget(self.LUE)
                                self.remove_widget(self.LPM)
                                self.remove_widget(self.ResponseErrorMessage)
                                self.remove_widget(self.SRC)
                                if(response['data'] == '0'):
                                    # data successfully registered
                                    self.SRC = self.widgetWithSuccessMessage("successfully registered")
                                    self.add_widget(self.SRC)
                                    self.regPopup.open()                                    
                                    self.manager.current = 'userlogin'
                                    #sm = ScreenManager()
                                    #sm.add_widget(Screen(name = ''))
                                    #print("successfully registered")
                                elif(response['data'] == '1'):
                                    self.ResponseErrorMessage  = self.widgetWithMessage("That username is present in the database")
                                    self.add_widget(self.ResponseErrorMessage)
                                    # there is and username already in the database
                                    #print("That username is present in the database")
                                elif(response['data'] == '2'):
                                    # there is and email already in the database
                                    self.ResponseErrorMessage  = self.widgetWithMessage("That email is present in the database")
                                    self.add_widget(self.ResponseErrorMessage)
                                    #print("That email is present in the database")
                                else:
                                    # Both username and email already in the database
                                    self.ResponseErrorMessage  = self.widgetWithMessage("That username and email are present in the database")
                                    self.add_widget(self.ResponseErrorMessage)
                                    #print("That username and email are present in the database")

                                return
            
                            elif passwordValidation == PasswordValidationResponse.NOTMATCHING:
                                # Passwords did not match, alert user to try again.
                                print("Passwords do not match")
                                self.remove_widget(self.LE)
                                self.remove_widget(self.LPE)
                                self.remove_widget(self.LUE)
                                self.LPM = self.widgetWithMessage("Passwords do not match!")
                                self.add_widget(self.LPM)
                                return
            
                            elif passwordValidation == PasswordValidationResponse.CONFIRMNOTENTERED or passwordValidation == PasswordValidationResponse.NOTENTERED:
                                # Password or Confirm Password text field not entered, alert user to try again.
                                label = 'Password field' if passwordValidation == PasswordValidationResponse.NOTENTERED else 'Confirm Password field'
                                print("%s must not be blank." % label)
                                self.remove_widget(self.LE)
                                self.remove_widget(self.LUE)
                                self.LPE = self.widgetWithMessage("%s must not be blank." % label)
                                self.add_widget(self.LPE)
                                return
                            
                        else:
                            # Username field was empty, alert user to try again.
                            self.remove_widget(self.LUE)
                            print("Username can not remain empty")
                            self.remove_widget(self.LE)
                            self.remove_widget(self.LUE)
                            self.LUE = self.widgetWithMessage("Username can not remain empty.")
                            self.add_widget(self.LUE)
                    else:
                        print("Phone number must be an integer.")
                        self.remove_widget(self.LE)
                        self.LUE = self.widgetWithMessage("Phone number must be an integer.")
                        self.add_widget(self.LUE)
                else:
                    print("Phone number can  not remain empty")
                    self.remove_widget(self.LE)
                    self.LE = self.widgetWithMessage("Phone number can  not remain empty")
                    self.add_widget(self.LE)
                    
            else:
                # Email value was invalid, alert user to try again.
                print("This is an invalid Email")
                self.remove_widget(self.LE)
                self.LE = self.widgetWithMessage("This is an invalid email address.")
                self.add_widget(self.LE)
        else:
            print("Name can  not remain empty")
            self.LE = self.widgetWithMessage("Name can  not remain empty.")
            self.add_widget(self.LE)
    # endregion
