#!/usr/bin/env python3

#https://media.readthedocs.org/pdf/kivy/latest/kivy.pdf
#https://kivy.org/doc/stable/api-kivy.html

from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        return Button(text='Hello World')

TestApp().run()