# register.py
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import sqlite3

Builder.load_file('register.kv')

class RegisterScreen(Screen):
    def update_message(self, message):
        self.ids.message_label.text = message

    def on_enter(self, *args):
        # This method is called when the screen is entered
        self.update_message('')  # Clear the message label

    def sign_up(self):
        # Get username and password from TextInput
        username = self.ids.username.text
        password = self.ids.password.text

        # Check if username or password is empty
        if not username or not password:
            self.update_message("Please enter both username and password.")
            return

        # Check if the username already exists
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            self.update_message("Username already exists. Please choose a different one.")
            conn.close()
            return

        # Insert into the database
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        user_id = cursor.lastrowid  # Get the last inserted row ID (user ID)
        conn.close()

        self.ids.username.text = ''
        self.ids.password.text = ''
        # You can add additional logic here, e.g., show a success message or switch to another screen
        self.update_message("User registered successfully.")

        # Access the HomeScreen through the screen manager
        home_screen = self.manager.get_screen("home")  # Assuming 'home' is the name of your HomeScreen
        home_screen.update_username_label(username)
        home_screen.update_user_id(user_id)
        # Access the AtasksScreen through the screen manager
        atasks_screen = self.manager.get_screen("addtasks")  # "addtasks" is the name assigned to the AtasksScreen
        atasks_screen.update_user_id(user_id)
