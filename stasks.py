from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
import sqlite3

class StasksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None
        self._popup = None  # Initialize _popup attribute
        self.current_popup = None  # Track the currently open popup
        self.load_data()
        # Schedule the automatic data update every 2 seconds
        Clock.schedule_interval(lambda dt: self.load_data(), 2)

    def update_user_id(self, user_id):
        self.user_id = user_id
        self.load_data()

    def load_data(self):
        if not self.user_id:
            return

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT title, description, date, time FROM tasks WHERE user_id = ? AND category = "Social"', (self.user_id,))
        data = cursor.fetchall()
        conn.close()

        layout = self.ids.data_buttons_container
        layout.clear_widgets()

        for record in data:
            title, description, date, time = record[:4]
            task_button = Button(
                text=title,
                size_hint_y=None,
                height=50,
                font_size=16,
                font_name='Poppins-SemiBold.ttf',
                text_size=(None, None),
                halign='left',
                background_color=(0.8, 0.8, 0.8, 0.7),
            )
            task_button.bind(on_release=partial(self.show_description_popup, title, description, date, time))
            layout.add_widget(task_button)

    def update_data(self, title, new_description, new_date, new_time):
        # Update the data in the show_description_popup
        for widget in self._popup.content.children:
            if isinstance(widget, Label):
                if f'Task Description: {title}' in widget.text:
                    widget.text = f'Task Description: {new_description}'
                elif f'Date: {title}\nTime: {title}' in widget.text:
                    widget.text = f'Date: {new_date}\nTime: {new_time}'

    def dismiss_popup(self, *args):
        if self.current_popup:
            self.current_popup.dismiss()

    def show_description_popup(self, title, description, date, time, *args):
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        description_text = Label(
            text=f'Task Description: {description}',
            size_hint=(1, None),
            height=dp(50),
            text_size=(None, None),
            valign='top',
        )
        date_time_label = Label(text=f'Date: {date}\nTime: {time}')

        use_ai_button = Button(text='Use AI', on_release=partial(self.go_to_ai_screen, title, description))
        edit_button = Button(text='Edit', on_release=partial(self.show_edit_popup, title, description, date, time))
        delete_button = Button(text='Delete', on_release=partial(self.delete_task, title))

        popup_content.add_widget(description_text)
        popup_content.add_widget(date_time_label)
        popup_content.add_widget(use_ai_button)
        popup_content.add_widget(edit_button)
        popup_content.add_widget(delete_button)

        self._popup = Popup(title=title, content=popup_content, size_hint=(None, None), size=(300, 400))
        self._popup.open()

        # Set text_size after the popup is opened
        description_text.text_size = (self._popup.width - dp(20), None)
    def go_to_ai_screen(self, title, description, *args):
        # Switch to the 'ai' screen and pass task details

        self.manager.get_screen('ai').update_task_details(title, description)
        self.dismiss_popup()
        self.manager.current = 'ai'
    def delete_task(self, title, *args):
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE title = ? AND user_id = ?', (title, self.user_id))
        conn.commit()
        conn.close()

        self.load_data()
        self.dismiss_popup()

    def show_edit_popup(self, title, description, date, time, *args):
        self.dismiss_popup()  # Close the current popup
        edit_popup = EditPopup(title, description, date, time, self.dismiss_popup)
        popup = Popup(title=f'Edit Task: {title}', content=edit_popup, size_hint=(None, None), size=(300, 400))
        popup.open()
        self.current_popup = popup

class EditPopup(Popup):
    def __init__(self, title, description, date, time, dismiss_popup, **kwargs):
        super().__init__(**kwargs)
        self.dismiss_popup_callback = dismiss_popup  # Store the dismiss_popup callback
        self.original_title = title

        self.title_input = TextInput(text=title, hint_text='New Task Title')
        self.description_input = TextInput(text=description, hint_text='New Task Description')
        self.date_input = TextInput(text=date, hint_text='New Date (YYYY-MM-DD)')
        self.time_input = TextInput(text=time, hint_text='New Time (HH:MM)')

        submit_button = Button(text='Save Changes', size_hint=(None, None), size=(225, 30))

        # New label for displaying the message
        self.message_label = Label(text='', color=(0, 1, 0, 1))  # Green color for success message

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(self.title_input)
        layout.add_widget(self.description_input)
        layout.add_widget(self.date_input)
        layout.add_widget(self.time_input)
        layout.add_widget(submit_button)
        layout.add_widget(self.message_label)  # Add the message label to the layout

        self.title = f'Edit Task: {title}'
        self.content = layout

        submit_button.bind(on_release=self.save_changes)

    def save_changes(self, *args):
        new_title = self.title_input.text
        new_description = self.description_input.text
        new_date = self.date_input.text
        new_time = self.time_input.text

        if not new_title:
            return

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET title=?, description=?, date=?, time=? WHERE title=?', (new_title, new_description, new_date, new_time, self.original_title))
        conn.commit()
        conn.close()

        # Update the message label with the success message
        self.message_label.text = 'Task updated successfully. Refresh the page to update the tasks.'

        # Close the popup after a brief delay (you can adjust the duration)
        Clock.schedule_once(partial(self.dismiss_popup_callback, self.dismiss), 0.1)
