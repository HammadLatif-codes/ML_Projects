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


Builder.load_file('uix/welcome.kv')

class WelcomeClass(Screen):
    def go_to_admin_panel(self):
        self.manager.current = 'admin_panel_screen'
        self.manager.transition.direction = 'left'
   
    def sign_out(self):
        self.manager.current = 'signin_screen'
        self.manager.transition.direction = 'right'
         


class DBS(App):
    def build(self):
        Window.clearcolor = (46/255,43/255,43/255,1)
        
        return WelcomeClass()


if __name__ =='__main__':
    DBS().run()
