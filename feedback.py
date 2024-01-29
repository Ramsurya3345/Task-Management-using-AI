from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class FeedbackScreen(Screen):
    email_input = ObjectProperty()
    feedback_input = ObjectProperty()

    def submit_feedback(self):
        email = self.email_input.text
        feedback = self.feedback_input.text

        # Your email sending logic here
        try:
            # Example: Send feedback email using Gmail SMTP
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = "ramsuryaagp18@gmail.com"
            smtp_password = "llfx qjgy slco agyr"

            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = smtp_username  # Send email to yourself
            msg['Subject'] = "Feedback Submission"
            msg.attach(MIMEText(f"Email: {email}\nFeedback: {feedback}", 'plain'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, smtp_username, msg.as_string())

            # If email sent successfully, switch to 'thanks' screen
            self.manager.current = 'thanks'
        except Exception as e:
            # If email sending fails, display an error message
            error_popup = Popup(title='Error', content=Label(text=f'Error: {str(e)}'), size_hint=(None, None), size=(400, 200))

            error_popup.open()



