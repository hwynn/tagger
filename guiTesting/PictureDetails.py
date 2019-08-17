from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty
from DescriptionBox import StretchingLabel, MyDescriptionFrame
from PrevNext import NextPrevBar
import SimulateOutside
from lib.modules.adaptive_grid_layout import Adaptive_GridLayout

Builder.load_string('''
<ContainerBox>:
    orientation: 'horizontal'

    BoxLayout:
        orientation: 'vertical'
        Image:
            source: '..\imgs\shinyLobster.jpg'
            allow_stretch: True
        Button:
            on_press: print(self.parent.children[-1].source)
        NextPrevBar:

    BoxLayout:
        orientation: 'vertical'
        size: root.size
        pos: root.pos
        Label:
            id: TitleBanner
            text: 'Title'
            size_hint_y: None
            height: 30
            bold: True
            canvas.before:
                Color:
                    rgba: .3, .7, .5, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

        MyTitleFrame:
            id: TitleContent

        Label:
            id: DescriptionBanner
            text: 'Description'
            size_hint_y: None
            height: 30
            bold: True
            canvas.before:
                Color:
                    rgba: .3, .7, .5, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

        MyDescriptionFrame:
            id: DescriptionContent

        Label:
''')

g_filename = "exampleImg.jpg"


class MyTitleFrame(Widget):
    c_value = StringProperty('A Title goes here')

    def __init__(self, **kwargs):
        super(MyTitleFrame, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.makeLabel(), timeout=0.1)

    def makeLabel(self):
        c_label = StretchingLabel()
        self.bind(pos=c_label.setter('pos'), width=c_label.setter('width'), c_value=c_label.setter('text'))
        c_label.bind(tempStr=self.setValue)
        self.add_widget(c_label)
        Clock.schedule_once(lambda dt: self.chg_text(), 0.5)

    def chg_text(self):
        # this forces a property event so the label's text will be changed
        self.property('c_value').dispatch(self)

    def setValue(self, instance, p_val):
        # print("MyDescriptionFrame.setDescription() instance:", instance)
        f_success = SimulateOutside.setTitle("samplefilename.jpg", p_val)
        if f_success:
            self.c_value = SimulateOutside.getTitle("samplefilename.jpg")
        else:
            print("MyTitleFrame.setValue() operation not successful")


class ContainerBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)


class Nested2App(App):
    def build(self):
        return ContainerBox()

    def on_start(self):
        print("Nested2App.on_start: starting")
        print(self.root.children)
        print("Nested2App.on_start: finishing")
        print()


if __name__ == '__main__':
    Nested2App().run()
