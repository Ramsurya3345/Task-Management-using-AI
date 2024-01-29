import openai
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen

class AiScreen(Screen):
    task_title = ""
    task_description = ""
    generated_output = ""

    def __init__(self, **kwargs):
        super(AiScreen, self).__init__(**kwargs)

    def update_task_details(self, title, description):
        self.task_title = title
        self.task_description = description
        # Update TextInput widgets with the new values
        self.ids.task_title_input.text = title
        self.ids.task_description_input.text = description
    def clear_text_inputs(self):
        # Clear text inputs
        self.ids.task_title_input.text = ''
        self.ids.task_description_input.text = ''
    def get_help(self):
        # You can implement the logic to get help from AI here
        # Use self.task_title and self.task_description as the input

        # Example GPT-3 API call
        openai.api_key = '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'  # Replace with your actual OpenAI API key
        title = self.ids.task_title_input.text
        description = self.ids.task_description_input.text
        prompt = f"{title}\n\n{description}\n\nGive help to solve this task with source website links. Include 10-20 lines content and provide relevant sources website links."

        response = openai.Completion.create(
            engine="text-davinci-003",  # You can choose the appropriate engine
            prompt=prompt,
            max_tokens=500  # Adjust the max_tokens as needed
        )

        # Set the generated output to GPT-3 response
        self.generated_output = response['choices'][0]['text']

        # Update the TextInput widget with the generated output
        self.ids.generated_output_input.text = self.generated_output

