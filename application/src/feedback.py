# The Perfect Larder 
# Team Orange
# CS411W ODU Fall 2019
# By: Adeniyi Adeniran, Chris Whitney, Collin DeWaters, Derek Tiller, Jonathan Schneider
#     Matthew Perry, Melanie Devoe, and Zachery Miller 

import kivy, smtplib, ssl, email
from _ast import Or
kivy.require('1.11.1')
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Feedback(Screen):
	
	errorMsg = Label()
	
	@staticmethod
	def errorWidget(message):
		widget = Label(text=message)
		widget.font_size = 45
		widget.bold = True
		widget.color = (1, 0, 0,0.75)
		widget.pos_hint = {"top":.66}
		return widget
	
	@staticmethod
	def successWidget(message):
		widget = Label(text=message)
		widget.font_size = 45
		widget.bold = True
		widget.color = (0, 1, 0,0.75)
		widget.pos_hint = {"top":.66}
		return widget
	
	@staticmethod
	def popUpMessage(header, message):
			content = GridLayout()
			content.cols = 1
			content.add_widget(
			    Label(text=message, halign='center', valign='top', font_size=60)
			)
			ok_button = Button(text='Ok', font_size=60)
			content.add_widget(ok_button)
			
			popup = Popup(
			    title=header,
			    content=content,
			    size_hint=(None, None),
			    size=(Window.width / 3, Window.height / 3),
			    auto_dismiss=True,
			)
			ok_button.bind(on_press=popup.dismiss)
			popup.open()
	
	def validateFeedback(self, message, rating):
		messageValid = 0
		ratingValid = 0
		self.remove_widget(self.errorMsg)
		
		#validate the message is not length 0
		messageValid = len(message) > 0
		
		#validate a radio button is depressed
		oneState = str(self.ids.one.state)
		twoState = str(self.ids.two.state)
		threeState = str(self.ids.three.state)
		fourState = str(self.ids.four.state)
		fiveState = str(self.ids.five.state)
		
		if( ( oneState.find('down') != -1 ) or ( twoState.find('down') != -1 ) or 
			( threeState.find('down') != -1 ) or ( fourState.find('down') != -1 ) or 
			( fiveState.find('down') != -1 ) ):
			ratingValid = 1
		else:
			ratingValid = 0
		
		if ( not messageValid and not ratingValid ):
			print ('invalid message and rating')
			self.errorMsg = self.errorWidget( 'Please leave a rating and a comment :-)' )
			self.add_widget( self.errorMsg )
		elif ( not messageValid ):
			print ('invalid message')
			self.errorMsg = self.errorWidget( 'Please leave a comment :-)' )
			self.add_widget( self.errorMsg )
		elif ( not ratingValid ):
			print ('invalid rating')
			self.errorMsg = self.errorWidget( 'Please leave a rating :-)' )
			self.add_widget( self.errorMsg )
			#self.popUpMessage("Error", "Please leave a rating :-)")


		else:
			print ('feedback valid')
			self.successMsg = self.successWidget( 'Thank you for submitting feedback :-)' )
			self.add_widget( self.successMsg )
		
		return ( messageValid and ratingValid )

	def submitFeedback(self):
		message = self.ids.message.text
		rating = int(self.ids.toggleValue.text)
		
		if ( self.validateFeedback(message, rating) ):
			password = 'plfeedback'
			sender_email = 'perfect.larder.feedback@gmail.com'
			receiver_email = "perfect.larder@gmail.com"
			body = "{}\n\n{}".format(rating, message)
			subject = "Feedback Received"
			
			message = MIMEMultipart()
			message["From"] = sender_email
			message["To"] = receiver_email
			message["Subject"] = subject
			message.attach( MIMEText( body, "plain" ) ) 
			
			text = message.as_string()
			context = ssl.create_default_context()
			with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
				server.login(sender_email, password)
				server.sendmail(sender_email, receiver_email, text)			

		else:
			print('feedback invalid')
