import sys
sys.path.append('/home/hammad/FYP/Kivy/Testing')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from uix.signup import SignUp
from uix.signin import SignIn
from uix.details import AddDetails
from uix.admin_pannel import AdminPanel
from uix.delete_record import DeleteRecord
from uix.search_record import SearchRecord
from uix.delete_all_records import DeleteAllRecords
from uix.Show_records import ShowRecords
from uix.update import UpdateScreen, Tabs_class
from uix.biometric import Biometric
from uix.welcome import WelcomeClass
import os


class DBSApp(App):
    def __init__(self, **kwargs):
        super(DBSApp, self).__init__(**kwargs)
        self.sm = ScreenManager()

        
    def build(self):
        Window.clearcolor = (46/255,43/255,43/255,1)
        # sm = ScreenManager()

        self.sm.add_widget(SignIn(name='signin_screen'))
        self.sm.add_widget(WelcomeClass(name='welcome_screen'))
        self.sm.add_widget(AddDetails(name='add_details_screen'))        
        self.sm.add_widget(SignUp(name='signup_screen'))      
        self.sm.add_widget(DeleteRecord(name='delete_record_screen'))
        self.sm.add_widget(SearchRecord(name='search_record_screen'))
        self.sm.add_widget(DeleteAllRecords(name='delete_all_records_screen'))
        self.sm.add_widget(ShowRecords(name='show_records_screen'))
        self.sm.add_widget(AdminPanel(name='admin_panel_screen'))
        self.sm.add_widget(Biometric(name="biometric_screen"))
        
        # Create a screen for UpdateScreen and add UpdateTabbedPanel to it
        update_screen = UpdateScreen(name='update_screen')
        update_tabbed_panel = Tabs_class(manager=self.sm)
        update_screen.add_widget(update_tabbed_panel)
        self.sm.add_widget(update_screen)
        
        self.sm.current = 'signin_screen'
              
        
        return self.sm

if __name__ == '__main__':
    DBSApp().run()
