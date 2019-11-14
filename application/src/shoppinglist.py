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
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import requests
import json

class ShoppingList(Screen):
	
    def OpenAdd(self):
        self.addpopup.open()
    
    def DelItem(self):

        screen = App.get_running_app().sm.get_screen('shoppinglist')
        item = screen.items[screen.selectedItem.itemToDel]
        screen.items.pop(screen.selectedItem.itemToDel)
        for x in (screen.ids.inventoryID.children):
            name = x.text.split('-')[0][:-1]
            if name == item['itemname']: 
                screen.ids.inventoryID.remove_widget(x)
        screen.popup.dismiss()
        
    def CancelUpdate(self):
        
        self.parent.parent.parent.parent.dismiss()
    
    def UpdateItem(self, popup):
        
        for x in (popup.children[0].children[0].children[0].children[0].children):
            if "TextInput" in str(type(x)):
                quantity = float(x.text)
            if "Spinner" in str(type(x)):
                measurement = x.text
        for x in (popup.children[0].children[0].children[0].children):
            if "Label" in str(type(x)):
                label = x.text
        
        self.items[self.selectedItem.itemToDel]['quantity'] = quantity
        self.items[self.selectedItem.itemToDel]['measurement'] = measurement
        self.ids.inventoryID.children
        for x in (self.ids.inventoryID.children):
            name = x.text.split('-')[0][:-1]
            if name == label: 
                x.text = name + " - " + str(quantity) + " " + measurement
            
        self.popup.dismiss()
        popup.dismiss()
        
    def CancelAdd(self):
        
        screen = App.get_running_app().sm.get_screen('shoppinglist')
        screen.addpopup.dismiss()
        
    def AddItem(self):
        
        screen = App.get_running_app().sm.get_screen('shoppinglist')
        for index, x in enumerate(screen.addpopup.children[0].children[0].children[0].children):
            if x.text == "Item Name":
                name = screen.addpopup.children[0].children[0].children[0].children[index - 1].text
            if x.text == "Quantity":
                quantity = screen.addpopup.children[0].children[0].children[0].children[index - 1].text
            if x.text == "Measurement":
                measurement = screen.addpopup.children[0].children[0].children[0].children[index - 1].text
        screen.items.append({
            'itemname' : name,
            'need' : quantity,
            'measurement' : measurement
        })
        button = Button(text = name + " - " + quantity + " " + measurement)
        n = len(screen.ids.inventoryID.children)
        callback = lambda n:screen.EditOrRemoveItem(n)
        button.itemToDel = n
        button.bind(on_press = callback)

        screen.ids.inventoryID.add_widget(button)
        screen.addpopup.dismiss()
        
    def EditItem(self):
        
        screen = App.get_running_app().sm.get_screen('shoppinglist')
        editcontent = GridLayout(cols = 1)
        editcontent.add_widget(Label(text = screen.items[screen.selectedItem.itemToDel]['itemname']))
        editcontent2 = GridLayout(cols = 2)
        editcontent2.add_widget(TextInput(text = str(screen.items[screen.selectedItem.itemToDel]['need']), id = 'quantity'))
        
        editcontent2.add_widget(Spinner(text = screen.items[screen.selectedItem.itemToDel]['measurement'], values = ('teaspoon', 'tablespoon', 'fluid ounce(fl oz)', 'cup', 'pint', 'quart', 'gallon', 'ounce(oz)', 'pounds(lbs)', 'mL', 'liter(L)', 'gram(g)'), id = 'measurement'))
        buttonA = Button(text = 'Cancel')
        buttonB = Button(text = 'Submit')
        
        editcontent2.add_widget(buttonA)
        editcontent2.add_widget(buttonB)
        
        editcontent.add_widget(editcontent2)
        self.editpopup = Popup(title = 'Edit Item', content = editcontent, auto_dismiss = False)
        buttonA.bind(on_press = self.editpopup.dismiss)
        
        self.editpopup.open()
        buttonB.bind(on_press = lambda *args: screen.UpdateItem(self.editpopup))
    
    items = []
    selectedItem = -1
    delcontent = GridLayout(cols = 1)
    button1 = Button(text = "Edit")
    button2 = Button(text = "Delete")
    button3 = Button(text = "Cancel")
    delcontent.add_widget(button1)
    delcontent.add_widget(button2)
    delcontent.add_widget(button3)
    popup = Popup(title = "Edit Item", content = delcontent, auto_dismiss = False, id = 'popup')
    button1.bind(on_press = EditItem)
    button2.bind(on_press = DelItem)
    button3.bind(on_press = CancelUpdate)
    editpopup = None
    
    addcontent = GridLayout(cols = 2)
    label1 = Label(text = "Item Name")
    text1 = TextInput(multiline = False, id = 'itemName')
    label2 = Label(text = "Quantity")
    text2 = TextInput(multiline = False, id = 'quantity')
    label3 = Label(text = "Measurement")
    spinner3 = Spinner(values = ('teaspoon', 'tablespoon', 'fluid ounce(fl oz)', 'cup', 'pint', 'quart', 'gallon', 'ounce(oz)', 'pounds(lbs)', 'mL', 'liter(L)', 'gram(g)'), id = 'measurement')
    button4 = Button(text = "Cancel")
    button5 = Button(text = "Submit")
    addcontent.add_widget(label1)
    addcontent.add_widget(text1)
    addcontent.add_widget(label2)
    addcontent.add_widget(text2)
    addcontent.add_widget(label3)
    addcontent.add_widget(spinner3)
    addcontent.add_widget(button4)
    addcontent.add_widget(button5)
    addpopup = Popup(title = "Add Item", content = addcontent, auto_dismiss = False, id = 'addPopup')
    button4.bind(on_press = CancelAdd)
    button5.bind(on_press = AddItem)
    
    def on_pre_enter(self):
        
        self.ids.inventoryID.clear_widgets()
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getShoppingList', headers={'Content-Type': 'application/json'}, data=json.dumps(dict(userID=App.get_running_app().userID))).json()
        
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