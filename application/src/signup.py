import kivy
kivy.require('1.11.1')
from kivy.config import Config

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.properties import ObjectProperty
Config.set('kivy', 'keyboard_mode','systemandmulti')

class SignUp(Screen):
    
    def validateInput(self):
            
        userName = self.ids.userName.text
        userEmail = self.ids.userEmail.text
        userPassword = self.ids.userPassword.text.toString()
        userPasswordConfirm = self.ids.userPasswordConfirm.text.toString()
        
        passContent = GridLayout(cols=1)
        passContent.add_widget(Label(text='Passwords do not match.'))
        passButton = Button(text='OK')
        passContent.add_widget(passButton)
        userPassPopup = Popup(title='Check your Password', content=passContent, auto_dismiss=False)
        passButton.bind(on_press=userPassPopup.dismiss)
        
        if (userPassword != userPasswordConfirm):
            self.userPassPopup.show()
            #working here
            pass
        #elif
        #    pass
        else:
            pass
        pass
    pass