from datetime import datetime
import os
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
from PrevNext import NextPrevBar
import SimulateOutside
from DatePopupButton import DateEditButton, DatePopup
from SeriesPopupButton import SeriesButton, SeriesPopup
from lib.modules.adaptive_grid_layout import Adaptive_GridLayout

# Our user interface

Builder.load_string('''
<ColorLabel>:
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size

<TagListBox>:
	GridLayout:
		size: root.size
		pos: root.pos
		id: boxlayout_h
		orientation: 'vertical'
		cols: 1
		ReadWriteTagList:
		    size_hint_y: None
		    height: 70
        thisText:
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
		    height: 35
        thisText:
            hint_text: 'add new artist'
            on_text_validate: print(self.parent.children[1].addNewArtist(self.giveText()))
            
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
            allow_stretch: True
            size_hint_y: .5
        Side1Details:
            cols: 1
            grow_rows: True
            size_hint_y: .5
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
                height: 40

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
            Label:
                id: RatingBanner
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
                id: SourceBanner
                text: 'Source URL'
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
                id: DateBanner
                text: 'Date Created'
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
                id: SeriesBanner
                text: 'Series'
                size_hint_y: None
                height: 30
                bold: True
                canvas.before:
                    Color:
                        rgba: .3, .7, .5, 1
                    Rectangle:
                        pos: self.pos
                        size: self.size
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
class ColorLabel(Label):
    bcolor = ListProperty([.7, .7, .7, 1])
    def __init__(self, **kwargs):
        super(ColorLabel, self).__init__(**kwargs)
        pass
        # this is a label with color. I don't know if this custom class is needed
        # there's probably a way to not use this


class Side1Details(Adaptive_GridLayout):
    def __init__(self, **kwargs):
        super(Side1Details, self).__init__(**kwargs)
        self.c_debug = 0

class Side2Details(Adaptive_GridLayout):
    #calling these outside functions in the declarations seems to slow us down a bit.
    #perhaps I should declae them as blank values then call an update function after the gui is built
    c_title_value = StringProperty(SimulateOutside.getTitle(SimulateOutside.getActiveFilePath()))
    c_description_value = StringProperty(SimulateOutside.getDesc(SimulateOutside.getActiveFilePath()))
    c_source_value = StringProperty(SimulateOutside.getSource(SimulateOutside.getActiveFilePath()))

    def __init__(self, **kwargs):
        super(Side2Details, self).__init__(**kwargs)
        self.c_debug = 0
        if self.c_debug>0: print("Side2Details._init_()")
        self.title_label = StretchingLabel()
        Clock.schedule_once(lambda dt: self.makeTitle(), timeout=0.1)
        self.desc_label = StretchingLabel()
        Clock.schedule_once(lambda dt: self.makeDescription(), timeout=0.1)
        self.rating_widget = RatingButtons()
        Clock.schedule_once(lambda dt: self.add_widget(self.rating_widget, len(self.children) - 5), timeout=0.1)
        self.source_label = StretchingLabel()
        Clock.schedule_once(lambda dt: self.makeSource(), timeout=0.1)
        self.date_popup_trigger = DateEditButton(height=25)
        self.date_label0 = ColorLabel(size_hint_y=None, height=30,
                                     bcolor=[.7, .7, .7, 1])
        Clock.schedule_once(lambda dt: self.makeOriginalDate(), timeout=0.1)
        self.series_popup_trigger = SeriesButton(height=25)
        self.series_label1 = ColorLabel(size_hint_y=None, height=30, text=self.series_popup_trigger.seriesName, bcolor=[.7, .7, .7, 1])
        self.series_label2 = ColorLabel(size_hint_y=None, height=30, bcolor=[.7, .7, .7, 1])
        Clock.schedule_once(lambda dt: self.makeSeries(), timeout=0.1)
        if self.c_debug > 1: print("Side2Details._init_() finished")

    def on_rows_minimum(self, instance, value):
        if self.c_debug>0: print("Side2Details.on_rows_minimum()", instance, value)


    # ------------Title------------------
    def makeTitle(self):
        self.debug = 0
        if self.c_debug>0: print("Side2Details.makeTitle()")
        self.bind(pos=self.title_label.setter('pos'), width=self.title_label.setter('width'), c_title_value=self.title_label.setter('text'))
        self.title_label.bind(tempStr=self.setTitleValue) #when the tempStr in StretchingLabel changes, setTitleValue is called
        self.add_widget(self.title_label, len(self.children) - 1)
        Clock.schedule_once(lambda dt: self.chg_title_text(), 0.5)
        # self.trigger_refresh_y_dimension()

    def chg_title_text(self):
        # this forces a property event so the label's text will be changed
        if self.c_debug>0: print("Side2Details.chg_title_text()")
        self.property('c_title_value').dispatch(self)

    def setTitleValue(self, instance, p_val):
        #this triggers a change in the value of the title via an outside script,
        # then updates the GUI to show that value
        if self.c_debug>0: print("Side2Details.setTitleValue() instance:", instance)
        f_success = SimulateOutside.setTitle(SimulateOutside.getActiveFilePath(), p_val.strip())
        if f_success:
            f_val = SimulateOutside.getTitle(SimulateOutside.getActiveFilePath())
            if f_val == "":
                f_val = " "
            self.c_title_value = f_val
        else:
            if self.c_debug>0: print("MyTitleFrame.setValue() operation not successful")

    def refreshTitleValue(self):
        print("Side2Details.refreshTitleValue()")
        f_val = SimulateOutside.getTitle(SimulateOutside.getActiveFilePath())
        if f_val == "":
            f_val = " "
        self.c_title_value = f_val
        self.c_title_value = SimulateOutside.getTitle(SimulateOutside.getActiveFilePath())

    # ------------Description------------------
    def makeDescription(self):
        self.debug = 0
        if self.c_debug>0: print("Side2Details.makeDescription()")
        self.bind(pos=self.desc_label.setter('pos'), width=self.desc_label.setter('width'), c_description_value=self.desc_label.setter('text'))
        self.desc_label.bind(tempStr=self.setDescriptionValue)
        self.add_widget(self.desc_label, len(self.children) - 3)
        Clock.schedule_once(lambda dt: self.chg_description_text(), 0.5)
        # self.trigger_refresh_y_dimension()

    def chg_description_text(self):
        # this forces a property event so the label's text will be changed
        if self.c_debug>0: print("Side2Details.chg_description_text()")
        self.property('c_description_value').dispatch(self)

    def setDescriptionValue(self, instance, p_val):
        #this triggers a change in the value of the description via an outside script,
        # then updates the GUI to show that value
        if self.c_debug>0: print("Side2Details.setDescriptionValue() instance:", instance)
        f_success = SimulateOutside.setDesc(SimulateOutside.getActiveFilePath(), p_val.strip())
        if f_success:
            f_val = SimulateOutside.getDesc(SimulateOutside.getActiveFilePath())
            if f_val == "":
                f_val = " "
            self.c_description_value = f_val
        else:
            if self.c_debug>0: print("MyDescriptionFrame.setValue() operation not successful")

    def refreshDescriptionValue(self):
        print("Side2Details.refreshDescriptionValue()")
        f_val = SimulateOutside.getDesc(SimulateOutside.getActiveFilePath())
        if f_val == "":
            f_val = " "
        self.c_description_value = f_val
        self.c_description_value = SimulateOutside.getDesc(SimulateOutside.getActiveFilePath())

    # ------------Rating------------------
    #   outside file used
    # ------------Source------------------
    def makeSource(self):
        self.debug = 2
        if self.c_debug>0: print("Side2Details.makeSource()")
        self.bind(pos=self.source_label.setter('pos'), width=self.source_label.setter('width'), c_source_value=self.source_label.setter('text'))
        self.source_label.bind(tempStr=self.setSourceValue)
        self.add_widget(self.source_label, len(self.children) - 7)
        Clock.schedule_once(lambda dt: self.chg_source_text(), 0.5)
        # self.trigger_refresh_y_dimension()

    def chg_source_text(self):
        # this forces a property event so the label's text will be changed
        if self.c_debug>0: print("Side2Details.chg_source_text()")
        self.property('c_source_value').dispatch(self)

    def setSourceValue(self, instance, p_val):
        #this triggers a change in the value of the source via an outside script,
        # then updates the GUI to show that value
        if self.c_debug>0: print("Side2Details.setSourceValue() instance:", instance)
        f_success = SimulateOutside.setSource(SimulateOutside.getActiveFilePath(), p_val.strip())
        if f_success:
            f_val = SimulateOutside.getSource(SimulateOutside.getActiveFilePath())
            if f_val == "":
                f_val = " "
            self.c_source_value = f_val
        else:
            if self.c_debug>0: print("MySourceFrame.setValue() operation not successful")

    def refreshSourceValue(self):
        print("Side2Details.refreshSourceValue()")
        f_val = SimulateOutside.getSource(SimulateOutside.getActiveFilePath())
        if f_val == "":
            f_val = " "
        self.c_source_value = f_val
        self.c_source_value = SimulateOutside.getSource(SimulateOutside.getActiveFilePath())

    # ------------Original Date------------------
    def makeOriginalDate(self):

        if self.date_popup_trigger.hasDate:
            self.date_label0.text = str(datetime.strptime(self.date_popup_trigger.ISODateString, "%Y-%m-%dT%H:%M:%S"))
        else:
            self.date_label0.text = "No date given"
        # this detects changes in the series values and calls changes to the user interface be made
        self.date_popup_trigger.bind(ISODateString=self.update_date)
        self.add_widget(self.date_label0, len(self.children) - 9)
        self.add_widget(self.date_popup_trigger, len(self.children) - 10)

    def update_date(self, instance, value):
        # this function updates the installment number shown on the user interface whenever the value changes
        self.date_label0.text = str(datetime.strptime(value, "%Y-%m-%dT%H:%M:%S"))
    # ------------Series------------------
    def makeSeries(self):
        # this is for series data, in case someone has pictures that are viewed in a sequence like comics

        if self.series_popup_trigger.seriesIns==-1:
            self.series_label2.text = ""
        else:
            self.series_label2.text='# '+str(self.series_popup_trigger.seriesIns)
        # this detects changes in the series values and calls changes to the user interface be made
        self.series_popup_trigger.bind(seriesName=self.series_label1.setter('text'))
        self.series_popup_trigger.bind(seriesIns=self.update_installment)
        self.add_widget(self.series_label1, len(self.children) - 12)
        self.add_widget(self.series_label2, len(self.children) - 13)
        self.add_widget(self.series_popup_trigger, len(self.children) - 14)

    def update_installment(self, instance, value):
        # this function updates the installment number shown on the user interface whenever the value changes
        if value == -1: #this implies no series exists, thus no number should be displayed
            self.series_label2.text = ""
        else:
            self.series_label2.text = '# '+str(value)


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

class Controller(BoxLayout):
    layout_content = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        #this helps with the positioning as the layout scales
        self.layout_content.bind(minimum_height=self.layout_content.setter('height'))
        
        self.picture = self.children[1].children[1]
        self.prevButton = self.children[1].children[0].children[0].children[1]
        self.nextButton = self.children[1].children[0].children[0].children[0]
        self.sidepanel2 = self.children[0].children[0]
        print(self.sidepanel2)
        print(self.sidepanel2.rating_widget)

        print(self.sidepanel2.title_label)
        print(self.sidepanel2.desc_label)
        print(self.sidepanel2.rating_widget)
        print(self.sidepanel2.source_label)
        print(self.sidepanel2.date_popup_trigger)
        print(self.sidepanel2.date_label0)
        print(self.sidepanel2.series_popup_trigger)
        print(self.sidepanel2.series_label1)
        print(self.sidepanel2.series_label2)

        self.artistlist = self.children[1].children[0].children[1]
        self.taglist = self.children[1].children[0].children[3]

        SimulateOutside.makeActiveFile(SimulateOutside.g_picFile)
        #print("filename:", SimulateOutside.g_picFile)
        #print("path:", SimulateOutside.g_path)
        #print("prev:", SimulateOutside.g_prevFile)
        #print("next:", SimulateOutside.g_nextFile)
        #print("exists:", os.path.isfile(SimulateOutside.g_path + SimulateOutside.g_picFile))


        self.picture.source = SimulateOutside.g_path + SimulateOutside.g_picFile
        #print(self.picture.source)
        #print(self.prevButton.text)
        #print(self.nextButton.text)
        self.prevButton.bind(on_release=self.goToPrevImage)
        self.nextButton.bind(on_release=self.goToNextImage)
        Clock.schedule_once(lambda dt: self.sidepanel2.refreshTitleValue(), timeout=4)
        Clock.schedule_once(lambda dt: self.sidepanel2.refreshDescriptionValue(), timeout=4)



        #Clock.schedule_once(lambda dt: boundryScan(self, 0), timeout=4)

    def goToPrevImage(self, arg):
        if SimulateOutside.getNext() != '':
            SimulateOutside.makeActiveFile(SimulateOutside.getPrev())
            self.picture.source = SimulateOutside.g_path + SimulateOutside.g_picFile

    def goToNextImage(self, arg):
        if SimulateOutside.getNext() != '':
            SimulateOutside.makeActiveFile(SimulateOutside.getNext())
            self.picture.source = SimulateOutside.g_path + SimulateOutside.g_picFile

class Nested2App(App):
    def build(self):
        return Controller()

if __name__ == '__main__':
    Nested2App().run()