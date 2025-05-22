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


Builder.load_file('uix/delete_all_records.kv')



class Warning_Popup(Popup):
    delete_records_instance = None
    
    def __init__(self, delete_records_instance, **kwargs):
        self.delete_records_instance = delete_records_instance
        super(Warning_Popup, self).__init__(**kwargs)
        

        
    def delete(self):
        self.delete_records_instance.delete_all_records()
        self.dismiss()
            
# -----------------------------------------------------------------------------------------------


class DeleteAllRecords(Screen):   
   

    def btn_event_handler(self):
        
        # to empty after displaying message
        self.ids.show_message.text = ''      
        Warning_Popup(self).open() 

     
    def delete_all_records(self):        
        status = delete_db_records.delete_all_records()
        if status:
            self.ids.show_message.text = "All Records deleted successfully"
        else:
            self.ids.show_message.text = "Unable to delete record"    
            

    def back_to_admin_pannel(self):
        # change screen
        self.manager.current = 'admin_panel_screen'
        self.manager.transition.direction = 'right'

class DBS(App):
    def build(self):
        Window.clearcolor = (46/255,43/255,43/255,1)
        
        return DeleteAllRecords()


if __name__ =='__main__':
    DBS().run()
