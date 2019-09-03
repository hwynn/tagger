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
from ReadWriteTagList import ReadWriteTagList
from ReadWriteArtistList import ReadWriteArtistList
from TitleBox import TitleBox
from PrevNext import NextPrevBar
import SimulateOutside
from lib.modules.adaptive_grid_layout import Adaptive_GridLayout

# We figured out how to make a scrollview work with a child that changes size in PosScrollTest3
# Now we want to slowly build the user interface from DescriptionBox into this

Builder.load_string('''
<TagListBox>:
	BoxLayout:
		size: root.size
		pos: root.pos
		id: boxlayout_h
		orientation: 'vertical'
		ReadWriteTagList:
		    size_hint_y: None
		    height: 70
        thisText:
            pos: (900, 20)
            hint_text: 'add new tag'
            on_text_validate: print(self.parent.children[1].addNewTag(self.giveText()))
<ArtistListBox>:
	BoxLayout:
		size: root.size
		pos: root.pos
		id: boxlayout_h
		orientation: 'vertical'
		ReadWriteArtistList:
		    size_hint_y: None
		    height: 70
        thisText:
            pos: (900, 20)
            hint_text: 'add new artist'
            on_text_validate: print(self.parent.children[1].addNewTag(self.giveText()))
            
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
        Label:
            id: TagBanner
            text: 'Tags'
            size_hint_y: None
            height: 30
            bold: True
            canvas.before:
                Color:
                    rgba: .3, .7, .5, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
        TagListBox:
        Label:
            id: TagBanner
            text: 'Artist'
            size_hint_y: None
            height: 30
            bold: True
            canvas.before:
                Color:
                    rgba: .3, .7, .5, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
        ArtistListBox:
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
''')

#--------------Debugging functions---------------------

def showMaybeText(p_widget):
    #prints text of widget if widget has text
    try: print(p_widget.text)
    except: print()

def heightScan(p_widget, p_level):
    #prints height of all widgets in the tree. used for debugging
    for i_child in reversed(list(p_widget.children)):
        print('\t' * p_level, i_child, end='')
        showMaybeText(i_child)
        print('\t' * p_level, "height: ", i_child.height)
        heightScan(i_child, p_level + 1)

def assess_widget(p_widget):
    #this is a function that will determine the total size and position of items INSIDE a widget
    #this is used for debugging
    #Note: this has a bug with calculating absolute positions in nested wigdets
    #return: ((x position, y position),(x size/width, y size/height))
    f_max_x = None
    f_max_y = None
    f_min_x = None
    f_min_y = None
    try:
        for i_child in reversed(list(p_widget.children)):
            if f_max_x==None:
                f_max_x = i_child.pos[0]+i_child.width
            elif (i_child.pos[0]+i_child.width) > f_max_x:
                f_max_x = i_child.pos[0] + i_child.width
            if f_max_y==None:
                f_max_y = i_child.pos[1]+i_child.height
            elif (i_child.pos[1]+i_child.height) > f_max_y:
                f_max_y = i_child.pos[1]+i_child.height
            if f_min_x==None:
                f_min_x = i_child.pos[0]
            elif i_child.pos[0] < f_min_x:
                f_min_x = i_child.pos[0]
            if f_min_y==None:
                f_min_y = i_child.pos[1]
            elif i_child.pos[1] < f_min_y:
                f_min_y = i_child.pos[1]
        #return (position, size)
        return ((f_min_x,f_min_y),((f_max_x-f_min_x),(f_max_y-f_min_y)))
    except:
        return ((p_widget.pos[0],p_widget.pos[1]),(p_widget.width, p_widget.height))

def boundryScan(p_widget, p_level):
    #prints height of all widgets in the tree. used for debugging
    for i_child in reversed(list(p_widget.children)):
        print('\t' * p_level, i_child, end='')
        showMaybeText(i_child)
        print('\t' * p_level, assess_widget(i_child), end='')
        try:
            print(i_child.rows_minimum)
        except:
            print()
        boundryScan(i_child, p_level + 1)

#--------------kivy classes----------------------
class Side2Details(Adaptive_GridLayout):
    c_title_value = StringProperty('A Title goes here')
    c_description_value = StringProperty('A Description goes here')
    c_source_value = StringProperty('https://www.image.com/01234/samplefilename.jpg')

    def __init__(self, **kwargs):
        super(Side2Details, self).__init__(**kwargs)
        self.c_debug = 3
        if self.c_debug>0: print("Side2Details._init_()")
        Clock.schedule_once(lambda dt: self.makeTitle(), timeout=0.1)
        #self.title_widget = TitleBox()
        #Clock.schedule_once(lambda dt: self.add_widget(self.title_widget, len(self.children) - 1) , timeout=0.1)

        Clock.schedule_once(lambda dt: self.makeDescription(), timeout=0.1)
        self.rating_widget = RatingButtons()
        Clock.schedule_once(lambda dt: self.add_widget(self.rating_widget, len(self.children) - 5), timeout=0.1)
        if self.c_debug > 1: print("Side2Details._init_() finished")

    def on_rows_minimum(self, instance, value):
        if self.c_debug>0: print("Side2Details.on_rows_minimum()", instance, value)


    # ------------Title------------------
    def makeTitle(self):
        self.debug = 2
        if self.c_debug>0: print("Side2Details.makeTitle()")
        c_label = StretchingLabel()
        self.bind(pos=c_label.setter('pos'), width=c_label.setter('width'), c_title_value=c_label.setter('text'))
        c_label.bind(tempStr=self.setTitleValue)
        self.add_widget(c_label, len(self.children) - 1)
        Clock.schedule_once(lambda dt: self.chg_title_text(), 0.5)
        # self.trigger_refresh_y_dimension()

    def chg_title_text(self):
        # this forces a property event so the label's text will be changed
        if self.c_debug>0: print("Side2Details.chg_title_text()")
        self.property('c_title_value').dispatch(self)

    def setTitleValue(self, instance, p_val):
        if self.c_debug>0: print("Side2Details.setTitleValue() instance:", instance)
        f_success = SimulateOutside.setTitle(SimulateOutside.g_file, p_val)
        if f_success:
            self.c_title_value = SimulateOutside.getTitle(SimulateOutside.g_file)
        else:
            if self.c_debug>0: print("MyTitleFrame.setValue() operation not successful")

    # ------------Description------------------
    def makeDescription(self):
        self.debug = 2
        if self.c_debug>0: print("Side2Details.makeDescription()")
        c_label = StretchingLabel()
        self.bind(pos=c_label.setter('pos'), width=c_label.setter('width'), c_description_value=c_label.setter('text'))
        c_label.bind(tempStr=self.setDescriptionValue)
        self.add_widget(c_label, len(self.children) - 3)
        Clock.schedule_once(lambda dt: self.chg_description_text(), 0.5)
        # self.trigger_refresh_y_dimension()

    def chg_description_text(self):
        # this forces a property event so the label's text will be changed
        if self.c_debug>0: print("Side2Details.chg_description_text()")
        self.property('c_description_value').dispatch(self)

    def setDescriptionValue(self, instance, p_val):
        # if self.c_debug>0: print("Side2Details.setDescriptionValue() instance:", instance)
        f_success = SimulateOutside.setDesc(SimulateOutside.g_file, p_val)
        if f_success:
            self.c_description_value = SimulateOutside.getDesc(SimulateOutside.g_file)
        else:
            if self.c_debug>0: print("MyDescriptionFrame.setValue() operation not successful")

    # ------------Rating------------------
    #   outside file used
    # ------------Source------------------

    # ------------Original Date------------------
    # ------------Series------------------


class TagListBox(Widget):
    def __init__(self, **kwargs):
        super(TagListBox, self).__init__(**kwargs)

class ArtistListBox(Widget):
    def __init__(self, **kwargs):
        super(ArtistListBox, self).__init__(**kwargs)

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

#



"""
class ResizingFrame(Adaptive_GridLayout):
    c_value = StringProperty('SomeThing goes here')

    def __init__(self, **kwargs):
        super(ResizingFrame, self).__init__(**kwargs)
        self.debug = 2
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
        if self.c_debug>0: print("ResizingFrame.on_height()", self.height)
"""

class Controller(BoxLayout):
    layout_content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        #this helps with the positioning as the layout scales
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))
        #Clock.schedule_once(lambda dt: boundryScan(self, 0), timeout=4)


class Nested2App(App):
    def build(self):
        return Controller()


if __name__ == '__main__':
    Nested2App().run()
