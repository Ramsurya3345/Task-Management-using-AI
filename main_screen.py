# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import sqlite3

class MainScreen(Screen):
    def update_message(self, message):
        self.ids.message_label.text = message

    def on_enter(self, *args):
        # This method is called when the screen is entered
        self.update_message('')  # Clear the message label

    def sign_in(self):
        # Get username and password from TextInput
        username = self.ids.username.text
        password = self.ids.password.text

        # Check if username or password is empty
        if not username or not password:
            self.update_message("Please enter both username and password.")
            return

        # Check if the username and password match
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        if user:
            user_id = user[0]
            self.ids.username.text = ''
            self.ids.password.text = ''

            # Correct credentials, handle further actions as needed
            self.update_message("User logged in successfully.")

            # Access the HomeScreen through the screen manager
            home_screen = self.manager.get_screen("home")  # Assuming 'home' is the name of your HomeScreen
            home_screen.update_username_label(username)
            home_screen.update_user_id(user_id)
            # Access the AtasksScreen through the screen manager
            atasks_screen = self.manager.get_screen("addtasks")  # "addtasks" is the name assigned to the AtasksScreen
            atasks_screen.update_user_id(user_id)
            # Access the PstasksScreen through the screen manager
            pstasks_screen = self.manager.get_screen("pstasks")
            pstasks_screen.update_user_id(user_id) # Call the method you want to update
            # Access the StasksScreen through the screen manager
            stasks_screen = self.manager.get_screen("stasks")
            stasks_screen.update_user_id(user_id) # Call the method you want to update
            # Access the WtasksScreen through the screen manager
            wtasks_screen = self.manager.get_screen("wtasks")
            wtasks_screen.update_user_id(user_id) # Call the method you want to update
            # Access the RtasksScreen through the screen manager
            rtasks_screen = self.manager.get_screen("rtasks")
            rtasks_screen.update_user_id(user_id) # Call the method you want to update
            # Access the SettingScreen through the screen manager
            setting_screen = self.manager.get_screen("setting")
            setting_screen.update_user_id(user_id) # Call the method you want to update


        else:
            # Incorrect credentials, display error message
            self.update_message("Incorrect username or password.")
        conn.close()

# Define other screens here...

