# ... Your existing imports ...
import sqlite3
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from plyer import notification

# Load the KV file
Builder.load_file('addtasks.kv')

class AtasksScreen(Screen):
    def __init__(self, user_id=None, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.task_manager_ui = TaskManagerUI(user_id=self.user_id)
        self.add_widget(self.task_manager_ui)

    def update_user_id(self, user_id):
        self.user_id = user_id
        self.task_manager_ui.update_user_id(user_id)
# ... Your existing imports ...

class TaskManagerUI(BoxLayout):
    user_id = None  # Initialize user_id as None

    def __init__(self, user_id, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id  # Set the user_id attribute
        self.orientation = "vertical"
        self.create_ui()
        self.create_database()
        self.setup_notification_scheduler()

        # Add a FloatLayout to hold the message label at the top
        self.message_layout = FloatLayout(size_hint_y=None, height='50dp')
        self.message_label = Label(text="", color=(0, 1, 0, 1), size_hint=(None, None), size=(300, 30))
        self.message_layout.add_widget(self.message_label)
        self.add_widget(self.message_layout)

    def update_user_id(self, user_id):
        self.user_id = user_id
        # Reload data with the updated user_id

    def setup_notification_scheduler(self):
        self.notification_scheduler = BackgroundScheduler()
        self.notification_scheduler.start()

    def schedule_notification(self, task_title, notification_datetime):
        # Schedule the notification with APScheduler
        self.notification_scheduler.add_job(
            self.show_notification,
            'date',
            run_date=notification_datetime,
            args=[task_title],
        )

    def show_notification(self, task_title):
        notification_title = "Task Reminder"
        notification.notify(
            title=notification_title,
            message=f"Don't forget: {task_title}",
            app_name="Task Manager",
        )

    def create_ui(self):
        # Add label for Add Tasks at the top
        self.add_widget(Label(text="[color=000000][font=Poppins-SemiBold]Add Tasks[/font][/color]",
                              font_size='25sp', markup=True, size_hint_y=None, height='60dp'))
        self.title_label = Label(text="Task Title:")
        self.title_input = TextInput(hint_text="Task Title",multiline=False, size_hint_y=None, height='40dp')
        self.description_label = Label(text="Task Description:")
        self.description_input = TextInput(hint_text="Task Description",multiline=False, size_hint_y=None, height='40dp')
        self.date_label = Label(text="Date:")
        self.date_input = TextInput(hint_text="Date in (YYYY-MM-DD)", multiline=False, size_hint_y=None, height='40dp')
        self.time_label = Label(text="Time:")
        self.time_input = TextInput(hint_text="Time in (HH:MM) 24hr format", multiline=False, size_hint_y=None, height='40dp')
        self.category_label = Label(text="Category:")
        self.category_spinner = Spinner(text="Select Category", size_hint_y=None, height='40dp')
        self.add_button = Button(text="Add Task", size_hint_y=None, height='40dp')
        self.task_list_layout = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None)

        self.add_category_options()

        self.add_button.bind(on_release=self.add_task)
        self.category_spinner.bind(on_text=self.update_category_dropdown)

        self.add_widget(self.title_label)
        self.add_widget(self.title_input)
        self.add_widget(self.description_label)
        self.add_widget(self.description_input)
        self.add_widget(self.date_label)
        self.add_widget(self.date_input)
        self.add_widget(self.time_label)
        self.add_widget(self.time_input)
        self.add_widget(self.category_label)
        self.add_widget(self.category_spinner)
        self.add_widget(self.add_button)
        self.add_widget(self.task_list_layout)

    def add_category_options(self):
        categories = ["Work", "Personal", "Social"]
        self.category_spinner.values = categories

    def update_category_dropdown(self, instance, value):
        self.category_spinner.text = value

    # Inside the add_task method
    def add_task(self, instance):
        title = self.title_input.text
        description = self.description_input.text
        date = self.date_input.text
        time = self.time_input.text
        category = self.category_spinner.text

        if not title:
            self.show_message("Error", "Please enter a task title.")
            return

        try:
            with sqlite3.connect("tasks.db") as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO tasks (user_id, title, description, date, time, category)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (self.user_id, title, description, date, time, category))
                conn.commit()

            task_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

            self.schedule_notification(title, task_datetime)

            # Clear input fields after adding task
            self.title_input.text = ""
            self.description_input.text = ""
            self.date_input.text = ""
            self.time_input.text = ""
            self.category_spinner.text = "Select Category"

            # Show success message
            self.show_message("Success", "Task added successfully.")

        except Exception as e:
            print(f"Error adding task: {e}")
            self.show_message("Error", "An error occurred while adding the task.")

    def show_message(self, title, message):
        # Set the message label text and position it at the top
        self.message_label.text = f"{title}: {message}"
        self.message_label.pos = (self.width / 2 - self.message_label.width / 2, self.height - self.message_label.height)
        # Schedule clearing the message after a brief delay (you can adjust the duration)
        Clock.schedule_once(self.clear_message, 3)

    def clear_message(self, dt):
        # Clear the message label text
        self.message_label.text = ""

    def create_database(self):
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT,
                description TEXT,
                date TEXT,
                time TEXT,
                category TEXT
            )
        """)
        self.conn.commit()

    def on_stop(self):
        self.notification_scheduler.shutdown()
        self.conn.close()
