from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty
from ChangeableLabel import StretchingLabel
from RatingButton import RatingButtons, StatusButton
from PrevNext import NextPrevBar
import SimulateOutside
from lib.modules.adaptive_grid_layout import Adaptive_GridLayout

# We figured out how to make a scrollview work with a child that changes size in PosScrollTest3
# Now we want to slowly build the user interface from DescriptionBox into this

Builder.load_string('''    
<Controller>:
    layout_content: layout_content
    orientation: 'horizontal'
    padding: 10, 10
    row_default_height: '48dp'
    row_force_default: True
    spacing: 10, 10

    BoxLayout:
        orientation: 'vertical'
        Image:
            source: '..\imgs\shinyLobster.jpg'
            allow_stretch: True
        Button:
            on_press: print(self.parent.children[-1].source)
        NextPrevBar:

    ScrollView:
        size: self.size
        Side2Details:
            id: layout_content
            cols: 1
            grow_rows: True
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
            Label:
                id: TitleBanner
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
            Label:
                id: TitleBanner
                text: 'Rating'
                size_hint_y: None
                height: 30
                bold: True
                canvas.before:
                    Color:
                        rgba: .3, .7, .5, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            StretchingLabel:
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dkdsjahf lkasjkat"
            Label:
                height: 20
                text: "Lorem ipsdodo dod dodo do dodt"
            Label:
                height: 20
                text: "Lorem ipsdkjwww  ww woij ksdsdf sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"
            Label:
                height: 20
                text: "Lorem ipsum dolor sit amet"



''')


class Side2Details(Adaptive_GridLayout):
    c_title_value = StringProperty('A Title goes here')
    c_description_value = StringProperty('A Description goes here')

    def __init__(self, **kwargs):
        super(Side2Details, self).__init__(**kwargs)
        print("Side2Details._init_()")
        Clock.schedule_once(lambda dt: self.makeTitle(), timeout=0.1)
        Clock.schedule_once(lambda dt: self.makeDescription(), timeout=0.1)
        Clock.schedule_once(lambda dt: self.add_widget(RatingButtons(), len(self.children) - 5), timeout=0.1)


    # ------------Title------------------
    def makeTitle(self):
        print("Side2Details.makeTitle()")
        c_label = StretchingLabel()
        self.bind(pos=c_label.setter('pos'), width=c_label.setter('width'), c_title_value=c_label.setter('text'))
        c_label.bind(tempStr=self.setTitleValue)
        self.add_widget(c_label, len(self.children) - 1)
        Clock.schedule_once(lambda dt: self.chg_title_text(), 0.5)
        # self.trigger_refresh_y_dimension()

    def chg_title_text(self):
        # this forces a property event so the label's text will be changed
        print("Side2Details.chg_title_text()")
        self.property('c_title_value').dispatch(self)

    def setTitleValue(self, instance, p_val):
        # print("Side2Details.setTitleValue() instance:", instance)
        f_success = SimulateOutside.setTitle(SimulateOutside.g_file, p_val)
        if f_success:
            self.c_title_value = SimulateOutside.getRating(SimulateOutside.g_file)
        else:
            print("MyTitleFrame.setValue() operation not successful")

    # ------------Description------------------
    def makeDescription(self):
        print("Side2Details.makeDescription()")
        c_label = StretchingLabel()
        self.bind(pos=c_label.setter('pos'), width=c_label.setter('width'), c_description_value=c_label.setter('text'))
        c_label.bind(tempStr=self.setDescriptionValue)
        self.add_widget(c_label, len(self.children) - 3)
        Clock.schedule_once(lambda dt: self.chg_description_text(), 0.5)
        # self.trigger_refresh_y_dimension()

    def chg_description_text(self):
        # this forces a property event so the label's text will be changed
        print("Side2Details.chg_description_text()")
        self.property('c_description_value').dispatch(self)

    def setDescriptionValue(self, instance, p_val):
        # print("Side2Details.setDescriptionValue() instance:", instance)
        f_success = SimulateOutside.setDesc(SimulateOutside.g_file, p_val)
        if f_success:
            self.c_description_value = SimulateOutside.getDesc(SimulateOutside.g_file)
        else:
            print("MyDescriptionFrame.setValue() operation not successful")

    # ------------Rating------------------
    #   outside file used
    # ------------Source------------------
    # ------------Original Date------------------
    # ------------Series------------------


class ResizingFrame(Adaptive_GridLayout):
    c_value = StringProperty('SomeThing goes here')

    def __init__(self, **kwargs):
        super(ResizingFrame, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.makeLabel(), timeout=0.1)

    def makeLabel(self):
        c_label = StretchingLabel()
        self.bind(pos=c_label.setter('pos'), width=c_label.setter('width'), c_value=c_label.setter('text'))
        self.add_widget(c_label)
        # this forces a property event so the label's text will be changed
        Clock.schedule_once(lambda dt: self.property('c_value').dispatch(self), 0.5)
        # this forces a property event so the label's pos will be changed
        Clock.schedule_once(lambda dt: self.chg_text(c_label), 1)
        Clock.schedule_once(lambda dt: self.trigger_refresh_y_dimension(), 1.5)

    def chg_text(self, p_widget):
        # this forces a property event so the label's text will be changed
        self.property('c_value').dispatch(self)
        # Note: This just seems to push the label down from the top of the screen without changing the layout's height
        self.trigger_refresh_y_dimension()
        # the same behaviour can be seen if you double click the stretching label and enter a change

    def on_height(self, instance, value):
        print("ResizingFrame.on_height()", self.height)


class Controller(BoxLayout):
    layout_content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))


class Nested2App(App):
    def build(self):
        return Controller()


if __name__ == '__main__':
    Nested2App().run()
