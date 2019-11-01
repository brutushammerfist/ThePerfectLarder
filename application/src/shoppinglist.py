# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 


import kivy
kivy.require('1.11.1')
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.button import Button
import requests
import json

class ShoppingList(Screen):
	
    def DelItem(self):
        pass
        
    def EditItem(self):
        
        editcontent = GridLayout(col = 1)
        editcontent.add_widget(Label(text = self.items[self.selectedItem]['itemname']))
        editcontent2 = GridLayout(col = 2)
        editcontent2.add_widget(TextInput(text = self.items[self.selectedItem]['quantity'], id = 'quantity'))
        
        editcontent2.add_widget(Spinner(text = self.items[self.selectedItem]['measurement'], values = ('teaspoon', 'tablespoon', 'fluid ounce(fl oz)', 'cup', 'pint', 'quart', 'gallon', 'ounce(oz)', 'pounds(lbs)', 'mL', 'liter(L)', 'gram(g)'), id = 'measurement'))
        buttonA = Button(text = 'Cancel')
        buttonB = Button(text = 'Submit')
        
        editcontent2.add_widget(buttonA)
        editcontent2.add_widget(buttonB)
        buttonA.bind(on_press = self.CancelUpdate)
        buttonB.bind(on_press = self.UpdateItem)
        
        editcontent.add_widget(editcontent2)
        self.editpopup = Popup(title = 'Edit Item', content = editcontent, auto_dismiss = False)
        self.editpopup.open()
    
    items = []
    selectedItem = -1
    delcontent = GridLayout(cols = 1)
    button1 = Button(text = "Edit")
    button2 = Button(text = "Delete")
    delcontent.add_widget(button1)
    delcontent.add_widget(button2)
    popup = Popup(title = "Edit Item", content = delcontent, auto_dismiss = False, id = 'popup')
    button1.bind(on_press = EditItem)
    button2.bind(on_press = DelItem)
    editpopup = None
    
    def on_pre_enter(self):
        
        self.ids.inventoryID.clear_widgets()
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getShoppingList', headers={'Content-Type': 'application/json'}, data=json.dumps(dict(userID=App.get_running_app().userID))).json()
        
        print(response['data'])
        
        if response['data'] != 'Shopping List Empty.':
            self.items = response['data']
            for n in range(0, len(response['data'])):
                if response['data'][n]['need'] > 0:
                    button = Button(text = response['data'][n]['itemname'] + " - " + str(response['data'][n]['need']) + " " + response['data'][n]['measurement'])
                    callback = lambda n:self.EditOrRemoveItem(n)
                    button.itemToDel = n
                    button.bind(on_press = callback)
                    self.ids.inventoryID.add_widget(button)
        else:
            self.ids.inventoryID.add_widget(Button(text = 'Shopping List currently empty.'))
            
    def EditOrRemoveItem(self, index):
        
        self.selectedItem = index
        self.popup.open()

    def UpdateItem(self):
        
        self.items[self.selectedItem]['quantity'] = self.quantity
        self.items[self.selectedItem]['measurement'] = self.measurement
        self.popup.close()
    
    def CancelUpdate(self):
        
        self.popup.close()
        
    def AddItem(self):
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    