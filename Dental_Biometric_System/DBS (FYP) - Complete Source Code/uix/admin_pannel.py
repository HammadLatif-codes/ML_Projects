from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import re
from kivy.uix.popup import Popup
import os
import imghdr
import sys
sys.path.append('/home/hammad/FYP/Kivy/Testing')



Builder.load_file('uix/admin_pannel.kv')



class AdminPanel(Screen):
    
    def add_details(self):
        self.manager.current = 'add_details_screen'
        self.manager.transition.direction = 'left'
   
    def go_to_welcome_screen(self):
        self.manager.current = 'welcome_screen'
        self.manager.transition.direction = 'right'
        
    def add_forensic_officer(self):
        self.manager.current = 'signup_screen'
        self.manager.transition.direction = 'left'
    
    def delete_record(self):
        self.manager.current = 'delete_record_screen'
        self.manager.transition.direction = 'left'
            
    def search_screen(self):
        self.manager.current = 'search_record_screen'
        self.manager.transition.direction = 'left'
        
    def go_to_delete_all_records_screen(self):
        self.manager.current = 'delete_all_records_screen'
        self.manager.transition.direction = 'left' 
        
    def go_to_update_record_screen(self):
        self.manager.current = 'update_screen' 
        self.manager.transition.direction = 'left'   
    
    def go_to_show_records_screen(self):  
        self.manager.current = 'show_records_screen'
        self.manager.transition.direction = 'left'  
        
    def go_to_biometric_screen(self):
        self.manager.current = 'biometric_screen'
        self.manager.transition.direction = 'left' 
            
                  
           
class DBS(App):     
    def build(self):
        Window.clearcolor = (46/255,43/255,43/255,1) 
        return AdminPanel()

        


if __name__ =='__main__':
    DBS().run()
