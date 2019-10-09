import kivy
import re
kivy.require('1.11.1')
from kivy.config import Config

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.properties import ObjectProperty
Config.set('kivy', 'keyboard_mode','systemandmulti')

class SignUp(Screen):
    
    #Popup to prompt for password re-input
    passContent = GridLayout(cols=1)
    passContent.add_widget(Label(text='Passwords do not match.'))
    passButton = Button(text='OK')
    passContent.add_widget(passButton)
    userPassPopup = Popup(title='Check your Password', content=passContent, auto_dismiss=False)
    passButton.bind(on_press=userPassPopup.dismiss)
    
    #Popup to prompt for email re-input
    emailContent = GridLayout(cols=1)
    emailContent.add_widget(Label(text='Specified email address is not valid.'))
    emailButton = Button(text='OK')
    emailContent.add_widget(emailButton)
    userEmailPopup = Popup(title='Check your Email Address', content=emailContent, auto_dismiss=False)
    emailButton.bind(on_press=userEmailPopup.dismiss)
    
    def createAccount(self):
        
        #Validate inputs   
        userName = self.ids.userName.text
        userEmail = self.ids.userEmail.text
        userPassword = self.ids.userPassword.text
        userPasswordConfirm = self.ids.userPasswordConfirm.text
        emailRegex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        
        if (userPassword != userPasswordConfirm):
            self.userPassPopup.open()
            self.ids.userPassword.text = ""
            self.ids.userPasswordConfirm.text = ""
            break
            
        if (not re.search(emailRegex, userEmail)):
            self.userEmailPopup.open()
            self.ids.userEmail.text = ""
            break
        
        #Check for userName already in database
        
        #Create user account