import sys
sys.path.append('/home/hammad/FYP/Kivy/Testing')
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
import re
from database import register
from kivy.metrics import dp
from database import fetch_records


Builder.load_file('uix/Show_records.kv')

class ShowRecords(Screen):
    
    def show_records(self, records):
        
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
                name = record[0]
                age = record[1]
                gender = record[2]
                state = record[3]
                picture_address = record[4]
                
                label = Label(text=str(index), size_hint=(None, None), size=(dp(100) , dp(50) ))
                grid.add_widget(label)
                for i in range(5):                  
                    
                    if i == 1:
                        label = Label(text=str(record[i]), size_hint=(None, None),size=(dp(100) , dp(50) ))
                    elif i==4:
                        label = Image(source=record[i], size_hint=(None, None),size=(dp(100) , dp(50) ))
                    else:
                        label = Label(text=record[i], size_hint=(None, None),size=(dp(100) , dp(50) ))
                        
                    grid.add_widget(label)
        
        
        scroller_grid.add_widget(grid)      
        # making show records button invisible after showing records
        # self.ids.gender_picker.text= 'Gender'

        
                
                
    def call_show_records_method(self):
        self.set_default_genderspinner_value()
        self.set_default_statespinner_value()
        scrollview = self.ids.scroller
        # removing header grid's widgets
        self.ids.header_grid.clear_widgets()
        # removing all the widgets within the ScrollView first ..... removing records
        scrollview.clear_widgets()
        records = fetch_records.fetch_data()   # fetching data from db
        self.show_records(records)
        self.ids.show_record_btn.text = 'All Records'
    

    #get state
    def state_spinner_click(self,state_value):
        self.set_default_genderspinner_value()
        self.set_default_AllRecords_btn_value()
        # removing header grid's widgets
        self.ids.header_grid.clear_widgets()
        scrollview = self.ids.scroller
        # removing all the widgets within the ScrollView first ..... removing records
        scrollview.clear_widgets()
        state = state_value   
        records = fetch_records.fetch_data_by_state(state)   # fetching data from db 
        self.show_records(records)
   
    def set_default_AllRecords_btn_value(self):
        self.ids.show_record_btn.text = 'Show All Records'
    # set default value for other options while choosing other filters
    def set_default_statespinner_value(self):
        self.ids.state_picker.text = 'State'
    
    # set default value for other options while choosing other filters
    def set_default_genderspinner_value(self):
        self.ids.gender_picker.text = 'Gender'
   
    #  get gender
    def gender_spinner_click(self,state_value):
        self.set_default_statespinner_value()
        self.set_default_AllRecords_btn_value()
        # removing header grid's widgets
        self.ids.header_grid.clear_widgets()
        scrollview = self.ids.scroller
        # removing all the widgets within the ScrollView first ..... removing records
        scrollview.clear_widgets()
        gender = state_value   
        records = fetch_records.fetch_data_by_gender(gender)       # fetching data from db
        self.show_records(records)  
        

    
    def back_to_admin_pannel(self):
        self.ids.header_grid.clear_widgets()
        scrollview = self.ids.scroller
        # removing all the widgets within the ScrollView ..... removing records
        scrollview.clear_widgets()
        self.ids.show_record_btn.text = 'Show All Records'
        self.manager.current = 'admin_panel_screen'
        self.manager.transition.direction = 'right'
       
  

class DBS(App):
    def build(self):
        Window.clearcolor = (46/255,43/255,43/255,1)
        
        return ShowRecords()


if __name__ =='__main__':
    DBS().run()
