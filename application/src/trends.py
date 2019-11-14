# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 


import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.garden.graph import Graph, MeshLinePlot, LinePlot
from kivy.uix.togglebutton import ToggleButton
import json
import requests

class Trends(Screen):

    items = []
    used = []
    wasted = []
    largest = 0

    def on_pre_enter(self):
    
        self.ids.graph.clear_widgets()
        self.ids.itemTrend.clear_widgets()

        headers = {'Content-Type' : 'application/json'}
           
        payload = {
            'userID' : App.get_running_app().userID   
        }
            
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getTrends', headers=headers, data=json.dumps(payload)).json()

        self.items = response['items']
        self.used = response['used']
        self.wasted = response['wasted']
        self.largest = response['largest']
        
        graph = Graph(xlabel='Time', ylabel='Use/Wasted', x_ticks_minor=1, x_ticks_major=3, y_ticks_minor=1, y_ticks_major=3, y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=0, xmax=12, ymin=-1, ymax=response['largest'] + 1)

        plot = LinePlot(line_width=4, color = [0,1,0,1])
        plot.points = response['used']
        graph.add_plot(plot)

        plot = LinePlot(line_width=4, color = [1,0,0,1])
        plot.points = response['wasted']
        graph.add_plot(plot)

        self.ids.graph.add_widget(graph)
        
        n = 0
        
        button = ToggleButton(text = 'Overall', group = 'trends', state = 'down', on_press = lambda n:self.graph_redraw(n))
        button.itemtoview = 0
        self.ids.itemTrend.add_widget(button)
        
        for index, x in enumerate(response['items'], 1):
            button = ToggleButton(text = x['itemname'], group = 'trends', on_press = lambda index:self.graph_redraw(index))
            button.itemtoview = index
            self.ids.itemTrend.add_widget(button)
            
            
    def graph_redraw(self, index):
    
        self.ids.graph.clear_widgets()
        
        if index.itemtoview == 0:
            graph = Graph(xlabel='Time', ylabel='Use/Wasted', x_ticks_minor=1, x_ticks_major=3, y_ticks_minor=1, y_ticks_major=3, y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=0, xmax=12, ymin=-1, ymax=self.largest + 1)

            plot = LinePlot(line_width=4, color = [0,1,0,1])
            plot.points = self.used
            graph.add_plot(plot)

            plot = LinePlot(line_width=4, color = [1,0,0,1])
            plot.points = self.wasted
            graph.add_plot(plot)

            self.ids.graph.add_widget(graph)
        else:
            item = self.items[index.itemtoview - 1]
            
            graph = Graph(xlabel='Time', ylabel='Use/Wasted', x_ticks_minor=1, x_ticks_major=3, y_ticks_minor=1, y_ticks_major=3, y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=0, xmax=12, ymin=-1, ymax=item['largest'] + 1)
            
            plot = LinePlot(line_width=4, color = [0,1,0,1])
            plot.points = item['used']
            graph.add_plot(plot)
            
            plot = LinePlot(line_width=4, color = [1,0,0,1])
            plot.points = item['wasted']
            graph.add_plot(plot)
            
            self.ids.graph.add_widget(graph)