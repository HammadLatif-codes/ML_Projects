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


Builder.load_file('uix/delete_record.kv')



class MyPopup(Popup):
    # delete_record_instance = None
    
    def __init__(self, records, **kwargs):
        # self.delete_record_instance = delete_record_instance
        super(MyPopup, self).__init__(**kwargs)
        
        self.ids.name.text = records['name']
        self.ids.age.text = str(records['age'])
        self.ids.gender.text = records['gender']
        self.ids.state.text = records['state']
        self.ids.img_address.source = records['picture_address']
        
    # def delete(self):
    #     self.delete_record_instance.delete_record()
    #     self.dismiss()
        
    def delete_record(self):      
        status = delete_db_records.delete_record(self.ids.name.text)
        if status:
            self.ids.name.text = ''
            self.ids.age.text = ''
            self.ids.gender.text = ''
            self.ids.state.text = ''
            self.ids.img_address.source = ''
            self.ids.delete_btn.opacity = 0
            self.ids.show_message.text = "Record deleted successfully"
        else:
            self.ids.show_message.text = "Unable to delete record"      
  
  
  
            
# -----------------------------------------------------------------------------------------------
class DeleteRecord(Screen):
   
   

    def btn_event_handler(self):
        
        name = self.ids.name.text
        # to empty after displaying message
        self.ids.show_message.text = ''
        
        if not name:
            self.ids.show_message.text = "Name field can not be empty"
            return
        
        existence = delete_db_records.check_record_exist(name)
        if(existence):
            # self.name = existence['name']
            # self.age = str(existence['age'])
            # self.gender = existence['gender']
            # self.state = existence['state']
            # self.pic_address = existence['picture_address']

            MyPopup(existence).open()

        else:
            self.ids.show_message.text = f"There's no record of {name} in database."
       

     

 
    # def delete_record(self):
    #     print(f"Name {self.name}")

        
    #     status = delete_db_records.delete_record(self.name)
    #     if status:
    #         self.ids.show_message.text = "Record deleted successfully"
    #     else:
    #         self.ids.show_message.text = "Unable to delete record"    
            

    def back_to_admin_pannel(self):
        # change screen
        self.ids.name.text = ''
        self.manager.current = 'admin_panel_screen'
        self.manager.transition.direction = 'right'

class DBS(App):
    def build(self):
        Window.clearcolor = (46/255,43/255,43/255,1)
        
        return DeleteRecord()


if __name__ =='__main__':
    DBS().run()
