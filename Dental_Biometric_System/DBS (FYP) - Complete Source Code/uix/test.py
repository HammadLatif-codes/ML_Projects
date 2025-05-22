# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from update import UpdateScreen, Tabs_class

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        
        # Create a screen for UpdateScreen and add UpdateTabbedPanel to it
        update_screen = UpdateScreen(name='update')
        update_tabbed_panel = Tabs_class()
        update_screen.add_widget(update_tabbed_panel)
        
        sm.add_widget(update_screen)
        sm.current = 'update'
        
        return sm

if __name__ == '__main__':
    MainApp().run()
