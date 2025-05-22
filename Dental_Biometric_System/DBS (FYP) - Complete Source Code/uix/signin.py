import sys
sys.path.append('/home/hammad/FYP/Kivy/Testing')
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import re
from database import register


Builder.load_file('uix/signin.kv')

class SignIn(Screen):
   
    # username = ObjectProperty(None)
    # password = ObjectProperty(None)
    role = None
    
    def get_role():
        return role
    
    def btn_event_handler(self):
        username = self.ids.name.text
        password = self.ids.input_password.text
        # to empty after displaying message
        self.ids.show_message.text = ''
        # to avoid empty input fields
        if not username or not password:
            self.ids.show_message.text = "Please enter correct username and password"
            return
        global role
        role = register.validate_user(username, password)
        if(role == "admin"):
            self.manager.current = 'welcome_screen'
            self.manager.transition.direction = 'left' 
        elif(role == "Forensic officer"):

            self.manager.current = 'biometric_screen'
            self.manager.transition.direction = 'left' 
        else:
            self.ids.show_message.text = "Please enter correct username and password"
       
        
        # print("Username: ", self.ids.name.text, "Password: ", self.ids.input_password.text)
        
        
        self.ids.name.text = ""
        self.ids.input_password.text= ""   

class DBS(App):
    def build(self):
        Window.clearcolor = (46/255,43/255,43/255,1)
        
        return SignIn()


if __name__ =='__main__':
    DBS().run()
