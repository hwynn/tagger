from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.factory import Factory
from kivy.uix.textinput import TextInput
from DynamicButtonList import DynamicTagList

"""
We want to see how to make buttons actually do something.
This should be a good way to show off how to bind buttons to functions and make them
effect specific widgets.
"""

#https://www.reddit.com/r/kivy/comments/86603w/assigning_functions_to_custom_widgets_outside_of/


Builder.load_string('''
<HBoxWidget>:
	BoxLayout:
		size: root.size
		pos: root.pos
		id: boxlayout_h
		orientation: 'vertical'
		DynamicTagList:
        thisText:
            pos: (100, 20)
            on_text_validate: print(self.parent.children[1].addNewTag(self.giveText()))

<RootWidget>:
    BoxLayout:
        orientation: 'vertical'
        Widget:
        Widget:
        HBoxWidget:

''')




class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

class HBoxWidget(Widget):
    def __init__(self, **kwargs):
        super(HBoxWidget, self).__init__(**kwargs)

class thisText(TextInput):
    def __init__(self, **kwargs):
        super(thisText, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (100, 30)
        self.multiline = False

    def showUs(self):
        print(self.text)
        self.text = ""

    def giveText(self):
        f_text = self.text
        self.text = ""
        return f_text

class TestApp(App):
    def build(self):
        return RootWidget()

if __name__ == '__main__':
    TestApp().run()