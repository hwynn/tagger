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
import SimulateOutside

Builder.load_string('''
<StretchingLabel>:
    padding: 10, 5
    size_hint_y: None
    text_size: self.width, None
    height: self.texture_size[1]
    group: 'test'
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
''')

g_filename = "exampleImg.jpg"


class StretchingLabel(Label):
    bcolor = ListProperty([.7, .7, .7, 1])
    edit = BooleanProperty(False)
    tempStr = StringProperty("")
    textinput = ObjectProperty(None, allownone=True)
    #Sometimes a user defocusses the text box, or hits enter without making an actual change
    #This toggles when we get a legit change that isn't one of those false alarms

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.is_double_tap and not self.edit:
            self.edit = True
        return super(StretchingLabel, self).on_touch_down(touch)

    def on_edit(self, instance, value):
        if not value:
            if self.textinput:
                self.remove_widget(self.textinput)
            return
        self.textinput = t = TextInput(
            text=self.text, size_hint=(None, None),
            font_size=self.font_size, font_name=self.font_name,
            pos=self.pos, size=self.size, multiline=False)
        self.bind(pos=t.setter('pos'), size=t.setter('size'))
        self.add_widget(self.textinput)
        t.bind(on_text_validate=self.on_text_validate, focus=self.on_text_focus)

    def on_text_validate(self, instance):
        #print("StretchingLabel.on_text_validate() new text:", instance.text)
        #this makes user input go through an external function before becoming label text
        #In our case, it tries to write to a file, then the label will be what we read from the file
        self.tempStr = instance.text
        #if you use this instead, the label text will be directly set from the user input
        #self.text = instance.text
        self.edit = False

    def on_text_focus(self, instance, focus):
        if focus is False:
            #If a used defocusses the text input without hitting "enter", the changes are discarded
            #this allows the users to easily "back out" and revert their change if they accidentally messed it up
            #self.tempStr = instance.text #so this is commented out
            self.edit = False

    def neutralizeColor(self):
        print("StretchingLabel.neutralizeColor()")
        self.bcolor = (.7, .7, .7, 1)

    def agitateColor(self):
        print("StretchingLabel.agitateColor()")
        self.bcolor = (0.7, 0, 0, 1)



