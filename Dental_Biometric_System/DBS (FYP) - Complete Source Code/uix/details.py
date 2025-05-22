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

from feature_extraction import data_preprocessing

Builder.load_file('uix/details.kv')


class PicturePopup(Popup):
    add_details_instance = None  # Reference to the AddDetails instance

    def __init__(self, add_details_instance, **kwargs):
        self.add_details_instance = add_details_instance
        super(PicturePopup, self).__init__(**kwargs)

    def select_picture_file(self, selection):
        if selection:
            self.file_path = selection[0]
            self.add_details_instance.get_picture_file_path(self.file_path)




class RadiographPopup(Popup):
    add_details_instance = None  # Reference to the AddDetails instance

    def __init__(self, add_details_instance, **kwargs):
        self.add_details_instance = add_details_instance
        super(RadiographPopup, self).__init__(**kwargs)

    def select_radiograph_file(self, selection):
        if selection:
            self.file_path = selection[0]
            self.add_details_instance.get_radiograph_file_path(self.file_path)





class AddDetails(Screen):
    # get gender 
    def checkbox_click(self, instance, value, gender_value):
        if value == True:
            self.gender = gender_value
            
    
    #get state
    def spinner_click(self,state_value):
        self.state = state_value   
        self.ids.show_message.text = ''     


    # get radiograph

    def show_picture_popup(self):
        PicturePopup(self).open()  
    # get picture file    
    def get_picture_file_path(self, path):
        self.picture_file_path = path
        picutre_name = os.path.basename(self.picture_file_path)
        self.ids.picture_button.text = picutre_name
  
        
    def show_radiograph_popup(self):
        RadiographPopup(self).open()    
    # get radiograph file    
    def get_radiograph_file_path(self, path):
        self.radiograph_file_path = path
        radiograph_name = os.path.basename(self.radiograph_file_path)
        self.ids.radiograph_button.text = radiograph_name
  
        
    def remove_message(self):
        self.ids.show_message.text = ''
    
    # Validation checker
    def btn_event_handler(self):
        self.username = self.ids.name.text.strip()
        age_str = self.ids.age.text.strip()
        
        
        #Validation for empty fields
        if not self.username or not age_str or not self.gender or not self.state or not self.picture_file_path or not self.radiograph_file_path:
            self.ids.show_message.text = "Please fill in all the fields"
            return

        
        #Validation for name format
        name_pattern = re.compile(r'^[A-Za-z\s]+$')
        if not name_pattern.match(self.username) or len(self.username) < 3:
            self.ids.show_message.text = "Please enter a valid name"
            return

            
        # Validation for age range
        try:
            self.age = int(age_str)
            if not (10 <= self.age <= 130):
                self.ids.show_message.text = "Please enter a valid age between 10 and 130"
                return
        except ValueError:
            self.ids.show_message.text = "Please enter a valid age"
            return
        
        if imghdr.what(self.picture_file_path) is None:
            self.ids.show_message.text = "Please select a valid image file"
            return
        
        if imghdr.what(self.radiograph_file_path) is None:
            self.ids.show_message.text = "Please select a valid image file"
            return
        

        #send AddDetails object for data preprocessing
        data_preprocessing.process_data(self)
        
        # Clear input fields
        self.ids.name.text = ""
        self.ids.age.text = ""

        # Clear class variables
        # self.gender = ''
        # self.state = ''

        # Clear file paths
        self.picture_file_path = ''
        self.radiograph_file_path = ''

        # Clear file buttons' text
        self.ids.picture_button.text = "Select Picture"
        self.ids.radiograph_button.text = "Select Radiograph"
        # to empty after displaying message
        self.ids.show_message.text = 'Details stored in database successfully!' 
        
        

    def back_to_admin_pannel(self):
        # change screen
        self.manager.current = 'admin_panel_screen'
        self.manager.transition.direction = 'right'
        
        
        
class DBS(App):     
    def build(self):
        Window.clearcolor = (46/255,43/255,43/255,1) 
        return AddDetails()

        


if __name__ =='__main__':
    DBS().run()
