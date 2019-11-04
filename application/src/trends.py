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
import json
import requests

class Trends(Screen):

    def on_pre_enter(self):


        headers = {'Content-Type' : 'application/json'}
           
        payload = {
            'userID' : App.get_running_app().userID   
        }
            
        response = requests.post('http://411orangef19-mgmt.cs.odu.edu:8000/getTrends', headers=headers, data=json.dumps(payload)).json()


        graph = Graph(xlabel='Time', ylabel='Use/Wasted', x_ticks_minor=1, x_ticks_major=3, y_ticks_minor=1, y_ticks_major=3, y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=0, xmax=12, ymin=-1, ymax=20)

        plot = MeshLinePlot(color = [0,1,0,1])
        plot.points = response['used']
        graph.add_plot(plot)

        plot = MeshLinePlot(color = [1,0,0,1])
        plot.points = response['wasted']
        graph.add_plot(plot)

        self.ids.graph.add_widget(graph)