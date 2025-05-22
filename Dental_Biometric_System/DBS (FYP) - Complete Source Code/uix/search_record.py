import sys
sys.path.append('/home/hammad/FYP/Kivy/Testing')
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import re
from kivy.uix.popup import Popup
from database import delete_db_records


Builder.load_file('uix/search_record.kv')



class Record_Popup(Popup):
    search_record_instance = None
    
    def __init__(self, records, **kwargs):
        
        super(Record_Popup, self).__init__(**kwargs)
        self.ids.name.text = records['name']
        self.ids.age.text = str(records['age'])
        self.ids.gender.text = records['gender']
        self.ids.state.text = records['state']
        self.ids.img_address.source = records['picture_address']
        
            
# -----------------------------------------------------------------------------------------------
class SearchRecord(Screen):
   
   

    def btn_event_handler(self):
        
        name = self.ids.name.text
        # to empty after displaying message
        self.ids.show_message.text = ''
        
        if not name:
            self.ids.show_message.text = "Name field can not be empty"
            return
        
        existence = delete_db_records.check_record_exist(name)
        if(existence):
            Record_Popup(existence).open()
            # self.ids.show_message.text = str(existence)

        else:
            self.ids.show_message.text = f"There's no record of {name} in database."
       

     

    def back_to_admin_Panel(self):
        self.ids.name.text = ''
        self.ids.show_message.text =''
        # change screen
        self.manager.current = 'admin_panel_screen'
        self.manager.transition.direction = 'right'

class DBS(App):
    def build(self):
        Window.clearcolor = (46/255,43/255,43/255,1)
        
        return SearchRecord()


if __name__ =='__main__':
    DBS().run()
