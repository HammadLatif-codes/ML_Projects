import sys
sys.path.append('/home/hammad/FYP/Kivy/Testing')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import re
from database import register
Builder.load_file('uix/signup.kv')

class SignUp(Screen):
   

    def btn_event_handler(self):
        username = self.ids.name.text
        password = self.ids.input_password.text
        # to empty after displaying message
        self.ids.show_message.text = ''
        # to avoid empty input fields
        if not username or not password:
            self.ids.show_message.text = "Please enter correct username and password"
            return
       
        # validate username
        if not username or len(username) < 3 or len(username) > 30:
            self.ids.show_message.text = "Username should be at least 3 characters long."
            return

        # Validate password
        if not password or len(password) < 5:
            self.ids.show_message.text = "Password should be at least 5 characters long."
            return

        if not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password) or not re.search("[!@#$%^&*(),.?\":{}|<>]", password):
            self.ids.show_message.text = "Password should contain at least one letter, one digit, and one special character."
            return
        
        #change screen
        registered = register.sign_up(username, password)
        
        print(f"User registered : {registered}")
        
        if registered:
            self.ids.show_message.text = "Registered Successfully!"
        else:
            self.ids.show_message.text = "Not Registered!"   
        
        
        self.ids.name.text = ""
        self.ids.input_password.text= ""      
            
        
    def back_to_admin_panel(self):
       # change screen
       self.ids.show_message.text = "" 
       self.manager.current = 'admin_panel_screen'
       self.manager.transition.direction = 'right'
        
        # print("Username: ", self.ids.name.text, "Password: ", self.ids.input_password.text)
        
        
         

class DBS(App):
    def build(self):
        Window.clearcolor = (46/255,43/255,43/255,1)
        
        return SignUp()


if __name__ =='__main__':
    DBS().run()
