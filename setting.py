import sqlite3

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.switch import Switch

class SettingScreen(Screen):
    def update_user_id(self, user_id):
        self.user_id = user_id
    def delete_all_data(self, switch_state):
        if not switch_state:
            # The switch is off, do not proceed with deletion
            return

        if self.user_id:
            conn = sqlite3.connect('tasks.db')  # Replace with your actual database name
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE user_id = ?', (self.user_id,))
            conn.commit()
            conn.close()



