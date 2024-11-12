from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from landing_page import LandingPage
from lowercase_letter_screen import LowercaseLetterScreen
from menu_page import MenuPage
from AbcAlpha import FlashCardScreen
from learn_number import LearnNumber
from number import NumberScreen
from dragDropAbc import DragDropScreen
# from dragDrop123 import NumbersScreen

class SupernovaApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(LandingPage(name='landing'))
        sm.add_widget(MenuPage(name='menu'))
        sm.add_widget(LowercaseLetterScreen(name='lowercase_letter_screen'))
        sm.add_widget(FlashCardScreen(name='Flashcard'))
        sm.add_widget(LearnNumber(name='LearnNumber'))
        sm.add_widget(NumberScreen(name='number'))
        sm.add_widget(DragDropScreen(name='dragdrop'))
        # sm.add_widget(NumbersScreen(name='dragdrop123'))
        

        return sm

if __name__ == '__main__':
    SupernovaApp().run()
