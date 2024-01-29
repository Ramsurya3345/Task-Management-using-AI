from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, SlideTransition, RiseInTransition
from kivy.lang import Builder
from kivy.core.window import Window

from addtasks import AtasksScreen
from feedback import FeedbackScreen
from home import HomeScreen
from pstasks import PstasksScreen
from register import RegisterScreen
from runningtasks import RtasksScreen
from setting import SettingScreen
from splash import SplashScreen
from main_screen import MainScreen
from getstarted1 import Getscreen1
from getstarted2 import GetScreen2
from stasks import StasksScreen
from thanks import ThanksScreen
from wtasks import WtasksScreen
from about import AboutusScreen
from ai_funtions import AiScreen

Window.size=(300,600)

Builder.load_file("splash.kv")  # Load the splash.kv file
Builder.load_file("main_screen.kv")  # Load the main_screen.kv file
Builder.load_file("home.kv")
Builder.load_file("getstarted1.kv")
Builder.load_file("getstarted2.kv")
Builder.load_file("pstasks.kv")
Builder.load_file("wtasks.kv")
Builder.load_file("stasks.kv")
Builder.load_file("setting.kv")
Builder.load_file("runningtasks.kv")
Builder.load_file("feedback.kv")
Builder.load_file("addtasks.kv")
Builder.load_file("register.kv")
Builder.load_file("thanks.kv")
Builder.load_file("about.kv")
Builder.load_file("ai_funtions.kv")



class MyApp(App):
    def build(self):
        sm = ScreenManager(transition=RiseInTransition())
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(Getscreen1(name="gets1"))
        sm.add_widget(GetScreen2(name="gets2"))
        sm.add_widget(PstasksScreen(name="pstasks"))
        sm.add_widget(WtasksScreen(name="wtasks"))
        sm.add_widget(StasksScreen(name="stasks"))
        sm.add_widget(SettingScreen(name="setting"))
        sm.add_widget(RtasksScreen(name="rtasks"))
        sm.add_widget(FeedbackScreen(name="feeds"))
        sm.add_widget(AtasksScreen(name="addtasks"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(ThanksScreen(name="thanks"))
        sm.add_widget(AboutusScreen(name="aboutus"))
        sm.add_widget(AiScreen(name="ai"))
        return sm

if __name__ == "__main__":
    MyApp().run()
