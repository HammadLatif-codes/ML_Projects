import sys
sys.path.append('/home/hammad/FYP/Kivy/Testing')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
import re
import os
from database import identification
from feature_extraction import data_preprocessing
from uix.signin import SignIn

Builder.load_file('uix/biometric.kv')


class Results_Popup(Popup):

    
    def __init__(self, records, **kwargs):
        
        super(Results_Popup, self).__init__(**kwargs)
        
        header_grid = self.ids.header_grid
        # create header
        label_no = Label(text='No.', size_hint=(None, None), size=(dp(100) , dp(50) ), bold=True)
        header_grid.add_widget(label_no)
        

        label_name = Label(text="Name", size_hint=(None, None), size=(dp(100) , dp(50) ), bold=True)
        header_grid.add_widget(label_name)
        
        label_age = Label(text="Age", size_hint=(None, None), size=(dp(100) , dp(50) ), bold=True)
        header_grid.add_widget(label_age)
        
        label_gender = Label(text="Gender", size_hint=(None, None), size=(dp(100) , dp(50) ), bold=True)
        header_grid.add_widget(label_gender)
        
        label_state = Label(text="State", size_hint=(None, None), size=(dp(100) , dp(50) ), bold=True)
        header_grid.add_widget(label_state)
        
        label_pic = Label(text="Picture", size_hint=(None, None), size=(dp(100) , dp(50) ), bold=True)
        header_grid.add_widget(label_pic)
        
        # parent_grid = self.ids.parent_grid
        scroller_grid = self.ids.scroller
        
        # Create a GridLayout with 6 columns
        grid = GridLayout(cols=6, size_hint=(None, None), width=800, height=dp(50))       
        grid.bind(minimum_height=grid.setter('height'))
        
        
        
        if records is not None:
            for index, record in enumerate(records, start=1):
                name = record['name']
                age = record['age']
                gender = record['gender']
                state = record['state']
                picture_address = record['picture_address']
                
                print(f"{name} {age} {gender} {state} {picture_address}")
                
                
                label = Label(text=str(index), size_hint=(None, None), size=(dp(100) , dp(50) ))
                grid.add_widget(label)
                label = Label(text=record['name'], size_hint=(None, None),size=(dp(100) , dp(50) ))
                grid.add_widget(label)
                label = Label(text=str(record['age']), size_hint=(None, None),size=(dp(100) , dp(50) ))
                grid.add_widget(label)
                label = Label(text=record['gender'], size_hint=(None, None),size=(dp(100) , dp(50) ))
                grid.add_widget(label)
                label = Label(text=record['state'], size_hint=(None, None),size=(dp(100) , dp(50) ))
                grid.add_widget(label)
                label = Image(source=record['picture_address'], size_hint=(None, None),size=(dp(100) , dp(50) ))
                grid.add_widget(label)
        
        
        scroller_grid.add_widget(grid) 
 


class Result_Popup(Popup):

    
    def __init__(self, records, **kwargs):
        
        super(Result_Popup, self).__init__(**kwargs)
        self.ids.name.text = records['name']
        self.ids.age.text = str(records['age'])
        self.ids.gender.text = records['gender']
        self.ids.state.text = records['state']
        self.ids.img_address.source = records['picture_address']
        
 

class Radiograph_Popup(Popup):
    biometric_instance = None  # Reference to the AddDetails instance

    def __init__(self, biometric_instance, **kwargs):
        self.biometric_instance = biometric_instance
        super(Radiograph_Popup, self).__init__(**kwargs)

    def select_radiograph_file(self, selection):
        if selection:
            self.file_path = selection[0]
            self.biometric_instance.get_radiograph_file_path(self.file_path)




class Biometric(Screen):
    # fetch_radiographs_features() returns a list of dictionaries
    fetched_features_with_ids_from_db = identification.fetch_radiographs_features()
    

    
    def show_radiograph_popup(self):
        Radiograph_Popup(self).open()    
    
    
    # get radiograph file    
    def get_radiograph_file_path(self, path):
        self.ids.details_btn.opacity = 0
        self.ids.results_btn.opacity = 0 
        self.ids.show_message.text = ''
        self.radiograph_file_path = path
        self.radiograph_name = os.path.basename(self.radiograph_file_path)
        self.ids.radiograph_button.text = self.radiograph_name

    
    
    def run_similarity_search(self):
        
        # extract_features() returs a list
        self.uploaded_img_features = data_preprocessing.extract_features(self.radiograph_file_path)
        # print(f"Biometric features :  {self.uploaded_img_features}")
        # print("----------------------------------------------------------------------")
        # find_matching_ids() returns a list of matched ids
        self.ids_list = identification.find_matching_ids(self.fetched_features_with_ids_from_db , self.uploaded_img_features )
        
        if(len(self.ids_list) == 1):
            self.ids.show_message.text = "1 match is found"
            self.found_record = identification.fetch_data_by_id(self.ids_list[0]) 
            self.ids.details_btn.opacity = 1               
        elif(len(self.ids_list)>1):
            self.ids.show_message.text = f"{len(self.ids_list)} matches are found"
            # fetch_data_by_ids()
            self.found_records = identification.fetch_data_by_ids(self.ids_list) 
            self.ids.results_btn.opacity = 1  
        
        else:
            self.ids.show_message.text = 'No match found!'            
            

        
    def show_result(self):
        Result_Popup(self.found_record).open()   
    
    def show_results(self):
        Results_Popup(self.found_records).open()    
    
    def go_to_admin_panel(self):
        actor = SignIn.get_role()
        self.ids.radiograph_button.text = 'Select Radiograph'
        self.radiograph_file_path = ''
        self.ids.details_btn.opacity = 0
        self.ids.results_btn.opacity = 0 
        self.ids.show_message.text = ''
        if actor == 'Forensic officer':
            self.ids.upload_radiograph.text = 'Upload Radiograph'
            self.manager.current = 'signin_screen'
            self.manager.transition.direction = 'right'
        elif actor == 'admin':    
            self.ids.upload_radiograph.text = 'Upload Radiograph'
            self.manager.current = 'admin_panel_screen'
            self.manager.transition.direction = 'right'
        
        

class DBS(App):
    def build(self):
        Window.clearcolor = (46/255,43/255,43/255,1)
        
        return Biometric()


if __name__ =='__main__':
    DBS().run()
