from kivy.app import App
from kivy.lang import Builder
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from PrevNext import NextPrevBar
import os


Builder.load_string('''
<ContainerBox>:
	orientation: 'vertical'
	Image:
        source: '../pics/psyduck.jpg'
        allow_stretch: True
	NextPrevBar:
''')

class ContainerBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)

class Nested2App(App):
    def build(self):
        return ContainerBox()

if __name__ == '__main__':
    Nested2App().run()