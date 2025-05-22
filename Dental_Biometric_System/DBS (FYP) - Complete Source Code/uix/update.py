import sys
sys.path.append('/home/hammad/FYP/Kivy/Testing')
from kivy.uix.screenmanager import Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder
import re
from database import delete_db_records
import os
import imghdr
from kivy.uix.popup import Popup
from feature_extraction import data_preprocessing
from database import updateRecord
from kivy.properties import ObjectProperty

Builder.load_file('uix/update.kv')


class UpdateScreen(Screen):
    pass


class Update_PicturePopup(Popup):
    add_details_instance = None  # Reference to the AddDetails instance

    def __init__(self, add_details_instance, **kwargs):
        self.add_details_instance = add_details_instance
        super(Update_PicturePopup, self).__init__(**kwargs)

    def select_picture_file(self, selection):
        if selection:
            self.file_path = selection[0]
            self.add_details_instance.get_picture_file_path(self.file_path)
            
            
class Update_RadiographPopup(Popup):
    add_details_instance = None  # Reference to the AddDetails instance

    def __init__(self, add_details_instance, **kwargs):
        self.add_details_instance = add_details_instance
        super(Update_RadiographPopup, self).__init__(**kwargs)

    def select_radiograph_file(self, selection):
        if selection:
            self.file_path = selection[0]
            self.add_details_instance.get_radiograph_file_path(self.file_path)



class Tabs_class(TabbedPanel):
    manager = ObjectProperty(None)  # Declare manager as an ObjectProperty

    def __init__(self, manager=None, **kwargs):
        super(Tabs_class, self).__init__(**kwargs)
        self.manager = manager
    
    def clear_msg_label(self):
        self.ids.show_message_in_tab1.text = ''

    
    def call_search_method(self) :
        searched_name = self.ids.search_name.text
        self.ids.show_message_in_tab1.text = ''
        self.ids.update_tab.opacity = 0
        
        if not searched_name:
            self.ids.show_message_in_tab1.text = "Name field can not be empty"
            return
        self.records = delete_db_records.check_record_exist(searched_name)
        if not self.records:
            self.ids.show_message_in_tab1.text = f"No record is found for {self.ids.search_name.text}"
            self.ids.record_tab.opacity = 0
            return
        
        self.ids.record_tab.opacity = 1
        self.show_found_record(self.records)
        
        #  showing in tab-2
    def show_found_record(self, records):
        self.ids.name.text = records['name']
        self.ids.age.text = str(records['age'])
        self.ids.gender.text = records['gender']
        self.ids.state.text = records['state']
        self.ids.radiograph.text = records['radiograph_address'] 
        self.ids.img_address.source = records['picture_address']    
        
     
    def go_to_update_tab(self):
        self.ids.update_tab.opacity = 1   
    
    gender = ''
    def checkbox_click(self, instance, value, gender_value):
        if value == True:
            self.gender = gender_value
            
    state = ''
    #get state
    def spinner_click(self,state_value):
        self.state = state_value   
        self.ids.show_message_in_tab3.text = ''  
        
    def show_picture_popup(self):
        Update_PicturePopup(self).open()  
        
        
    # get picture file   
    picture_file_path = '' 
    def get_picture_file_path(self, path):
        self.picture_file_path = path
        picutre_name = os.path.basename(self.picture_file_path)
        self.ids.picture_button.text = picutre_name
        
    def show_radiograph_popup(self):
        Update_RadiographPopup(self).open()    
        
        
    # get radiograph file  
    radiograph_file_path = ''  
    def get_radiograph_file_path(self, path):
        self.radiograph_file_path = path
        radiograph_name = os.path.basename(self.radiograph_file_path)
        self.ids.radiograph_button.text = radiograph_name
        
    def remove_message(self):
        self.ids.show_message_in_tab3.text = ''
    
    # Validation checker
    def btn_event_handler(self):
        self.username = self.ids.updated_name.text.strip()
        age_str = self.ids.updated_age.text.strip()
        
        
        
         #Validation for empty fields
        if not self.username and not age_str and not self.gender and not self.state and not self.picture_file_path and not self.radiograph_file_path:
            self.ids.show_message_in_tab3.text = "Update atleast one field"
            return
       
        if not self.username:
            self.username = self.records['name']
            
        if not age_str:
            age_str = str(self.records['age'])
            
        if not self.gender:
            self.gender  = self.records['gender']
            
        if not self.state:
            self.state = self.records['state']
            
        if not self.picture_file_path:
            self.picture_file_path = self.records['picture_address']  
            
        if not self.radiograph_file_path:
            self.radiograph_file_path = self.records['radiograph_address'] 
        
        
        # Validation for name format
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
        

        #extract features from radiograph
        extracted_features = data_preprocessing.extract_features(self.radiograph_file_path)
        
        # save changes in database
        updateRecord.db_operations(self.records['id'], self, extracted_features)
        
        
        # Clear input fields
        self.ids.name.text = ""
        self.ids.age.text = ""



        # Clear file paths
        self.picture_file_path = ''
        self.radiograph_file_path = ''

        # Clear file buttons' text
        self.ids.picture_button.text = "Select Picture"
        self.ids.radiograph_button.text = "Select Radiograph"
        # to empty after displaying message
        self.ids.show_message_in_tab3.text = 'Details updated in database successfully!' 
        
        
        
        
        
        
    
    def back_to_Admin_panel(self):
        self.ids.name.text = ''
        self.ids.show_message_in_tab3.text = ''
        self.ids.show_message_in_tab1.text = ''
        self.ids.update_tab.opacity = 0
        self.ids.record_tab.opacity = 0 
        if self.manager:
            self.manager.current = 'admin_panel_screen'
            self.manager.transition.direction = 'right'
        else:
            print("Manager is not set properly!")
