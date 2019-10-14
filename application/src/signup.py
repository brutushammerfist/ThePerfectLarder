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
#Config.set('kivy', 'keyboard_mode','systemandmulti')

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
    EMAIL_REGEX = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    LE = Label()
    LPM = Label()
    LPE = Label()
    LUE = Label()
    def checkEmailValidity(self,email):
        if(re.search(self.EMAIL_REGEX, email)):
            return True
        else:
            return False
    def createAccount(self):
        
        #Validate inputs   
        userName = self.ids.userName.text
        userEmail = self.ids.userEmail.text
        userPassword = self.ids.userPassword.text
        userPasswordConfirm = self.ids.userPasswordConfirm.text
        self.remove_widget(self.LE)
        self.remove_widget(self.LPM)
        self.remove_widget(self.LPE)
        if (self.checkEmailValidity(userEmail) != False):
            if(userName != ""):
                if(userPassword != "" and userPasswordConfirm != ""):
                    if(userPassword != userPasswordConfirm):
                        print("Password does not match")
                        self.remove_widget(self.LE)
                        self.remove_widget(self.LPE)
                        self.LPM = Label(text='Password does not match')
                        self.LPM.font_size = 14
                        self.LPM.color = (1,0,1,1)    
                        self.add_widget(self.LPM)
                    else:
                        print('Sending data to backe end')
                elif(userPassword == ""):
                    print("password can not remain empty")
                    self.remove_widget(self.LE)
                    self.remove_widget(self.LUE)
                    self.LPE = Label(text='password can not remain empty')
                    self.LPE.font_size = 14
                    self.LPE.color = (1,0,1,1)    
                    self.add_widget(self.LPE)
                else:
                    print("confirm password can not remain empty")
                    self.remove_widget(self.LE)
                    self.remove_widget(self.LUE)
                    self.LPE = Label(text='confirm password can not remain empty')
                    self.LPE.font_size = 14
                    self.LPE.color = (1,0,1,1)    
                    self.add_widget(self.LPE)
            else:
                print("Username can not remain empty")
                self.remove_widget(self.LE)
                self.LUE = Label(text='Username can not remain empty')
                self.LUE.font_size = 14
                self.LUE.color = (1,0,1,1)    
                self.add_widget(self.LUE)
                
        else:
            print("This is an invalid Email")
            self.LE = Label(text='This is an invalid Email')
            self.LE.font_size = 14
            self.LE.color = (1,0,1,1)    
            self.add_widget(self.LE) 