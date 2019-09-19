from datetime import datetime
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, NumericProperty, ListProperty
import SimulateOutside

Builder.load_string('''
<DateEditButton>:
    on_press: self.fire_popup()
<DatePopup>:
    id:pop
    size_hint: .4, .6
    pos_hint: {'x': .6, 'y': .2}
    pos: 200, 0
    auto_dismiss: False
    title: 'When was this created/posted?'
''')

class DatePopup(Popup):
    def __init__(self, **kwargs):
        super(DatePopup, self).__init__(**kwargs)
    # the widget we add in here actually does everything. so this is empty

# this button is reuasable
class DateEditButton(Button):
    # this is the button that triggers the popup being created
    hasDate = SimulateOutside.containsOrgDate(SimulateOutside.g_file)
    sampledate = SimulateOutside.getOriginalDate(SimulateOutside.g_file)
    ISODateString = StringProperty(sampledate.isoformat())
    timeChunk1 = NumericProperty(sampledate.timetuple()[0])
    timeChunk2 = NumericProperty(sampledate.timetuple()[1])
    timeChunk3 = NumericProperty(sampledate.timetuple()[2])
    timeChunk4 = NumericProperty(sampledate.timetuple()[3])
    timeChunk5 = NumericProperty(sampledate.timetuple()[4])
    timeChunk6 = NumericProperty(sampledate.timetuple()[5])
    pops = DatePopup()

    def __init__(self, **kwargs):
        super(DateEditButton, self).__init__(**kwargs)
        self.c_debug = 0
        self.text = "change date"

    def isNumberBlank(self, p_str):
        # decides if string is useable number
        # we will count '' as a number because we'll replace those with 0 or 1
        return ((p_str.isnumeric()) or (p_str == ""))

    def getNumberBlank0(self, p_str):
        # gives us a useable number from a string
        # p_str must be tested by isNumberBlank() before being passed to this function
        if (p_str == ""):
            return 0
        return int(p_str)

    def getNumberBlank1(self, p_str):
        # gives us a useable number from a string
        # p_str must be tested by isNumberBlank() before being passed to this function
        if (p_str == ""):
            return 1
        return int(p_str)

    def setDateValue(self, p_ins):
        # this calls an outside script to set the series value in a picture file
        # then the new value is passed back to us for the user interface to display
        # It should not be possible to call this function with bad input
        # pop_submit() should check the input for this
        if self.c_debug > 0: print("DateEditButton.setDateValue:", p_ins)
        f_success = SimulateOutside.setOriginalDate(SimulateOutside.g_file, p_ins)
        if f_success:
            self.sampledate = SimulateOutside.getOriginalDate(SimulateOutside.g_file)
            self.hasDate = True
            self.ISODateString = self.sampledate.isoformat()
            self.timeChunk1 = self.sampledate.timetuple()[0]
            self.timeChunk2 = self.sampledate.timetuple()[1]
            self.timeChunk3 = self.sampledate.timetuple()[2]
            self.timeChunk4 = self.sampledate.timetuple()[3]
            self.timeChunk5 = self.sampledate.timetuple()[4]
            self.timeChunk6 = self.sampledate.timetuple()[5]
            if self.c_debug > 0: print("DateEditButton.setDateValue:", self.ISODateString)
        else:
            if self.c_debug > 0: print("setDateValue.setValue() operation not successful")

    def pop_cancel(self, instance):
        # any input from the user is discarded and the popup is closed
        if self.c_debug > 0: print("DateEditButton.pop_cancel.instance:", instance)
        self.pops.dismiss()

    def pop_submit(self, instance):
        # this happens when the submit button on the popup is pressed.
        # this checks input, tells the program the input is ready, then closes the popup
        if self.c_debug > 1: print("DateEditButton.pop_submit.instance.parent.children:", instance.parent.children)
        if self.c_debug > 1: print("DateEditButton.pop_submit.instance.parent.children:",
                                   instance.parent.children[3].children)
        f_timeInput1 = instance.parent.children[3].children[6]  # these are the text inputs with the values we will check
        f_timeInput2 = instance.parent.children[3].children[5]
        f_timeInput3 = instance.parent.children[3].children[4]
        f_timeInput4 = instance.parent.children[3].children[2]
        f_timeInput5 = instance.parent.children[3].children[1]
        f_timeInput6 = instance.parent.children[3].children[0]
        if self.c_debug > 0: print("DateEditButton.pop_submit.children[8]:", f_timeInput1.text)
        if self.c_debug > 0: print("DateEditButton.pop_submit.children[7]:", f_timeInput2.text)
        if self.c_debug > 0: print("DateEditButton.pop_submit.children[6]:", f_timeInput3.text)
        if self.c_debug > 0: print("DateEditButton.pop_submit.children[5]:", f_timeInput4.text)
        if self.c_debug > 0: print("DateEditButton.pop_submit.children[4]:", f_timeInput5.text)
        if self.c_debug > 0: print("DateEditButton.pop_submit.children[3]:", f_timeInput6.text)
        # if the input is invalid, the button shouldn't work.
        # This lets the user know a mistake happened before their work is lost when the popup closes
        if self.areDateStringsValid(f_timeInput1.text, f_timeInput2.text, f_timeInput3.text, f_timeInput4.text, f_timeInput5.text, f_timeInput6.text):
            f_datetime = datetime(int(f_timeInput1.text),
                                  self.getNumberBlank1(f_timeInput2.text),
                                  self.getNumberBlank1(f_timeInput3.text),
                                  self.getNumberBlank0(f_timeInput4.text),
                                  self.getNumberBlank0(f_timeInput5.text),
                                  self.getNumberBlank0(f_timeInput6.text))
            self.setDateValue(f_datetime)
            self.pops.dismiss()
        # TODO: add feedback for bad inputs

    def areDateStringsValid(self, p_year, p_month, p_day, p_hour, p_minute, p_second):
        # before we accept this date time input, we have to check if it's valid
        # and we just have a bunch of strings at this point
        if p_year == "" or (p_year.isnumeric()==False): #year cannot be blank
            return False
        if (self.isNumberBlank(p_month) and self.isNumberBlank(p_day) and self.isNumberBlank(p_hour)
                and self.isNumberBlank(p_minute) and self.isNumberBlank(p_second))==False:
            return False
        try:
            #we'll try to create a datatime. its constructor will find any problems for us
            if self.c_debug > 0: print('DateEditButton.areDateStringsValid() create date:', int(p_year),
                                       self.getNumberBlank1(p_month), self.getNumberBlank1(p_day),
                                       self.getNumberBlank0(p_hour), self.getNumberBlank0(p_minute),
                                       self.getNumberBlank0(p_second))
            dt_obj = datetime(int(p_year), self.getNumberBlank1(p_month), self.getNumberBlank1(p_day),
                              self.getNumberBlank0(p_hour), self.getNumberBlank0(p_minute),
                              self.getNumberBlank0(p_second))
            return True
        except:
            # TODO: add exception saying that number isn't valid
            print('DateEditButton.areDateStringsValid(): not valid')
            return False

    def fire_popup(self):
        # this builds the interface inside the popup, then makes it appear on the screen
        f_widget = BoxLayout(orientation='vertical')
        self.pops.content = f_widget
        timeblock = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        insInput1 = TextInput(multiline=False, size_hint=(None,None), height=30, width=50,
                              input_filter='int', hint_text='YYYY')
        insInput2 = TextInput(multiline=False, size_hint=(None,None), height=30, width=30,
                              input_filter='int', hint_text='M')
        insInput3 = TextInput(multiline=False, size_hint=(None,None), height=30, width=30,
                              input_filter='int', hint_text='D')
        insInput4 = TextInput(multiline=False, size_hint=(None,None), height=30, width=30,
                              input_filter='int', hint_text='h')
        insInput5 = TextInput(multiline=False, size_hint=(None,None), height=30, width=30,
                              input_filter='int', hint_text='m')
        insInput6 = TextInput(multiline=False, size_hint=(None,None), height=30, width=30,
                              input_filter='int', hint_text='s')
        if self.hasDate:
            insInput1.text = str(self.timeChunk1)
            insInput2.text = str(self.timeChunk2)
            insInput3.text = str(self.timeChunk3)
            insInput4.text = str(self.timeChunk4)
            insInput5.text = str(self.timeChunk5)
            insInput6.text = str(self.timeChunk6)
        else:
            insInput1.text = ""
            insInput2.text = ""
            insInput3.text = ""
            insInput4.text = ""
            insInput5.text = ""
            insInput6.text = ""
        cuteLabel1 = Label(text="Date", height=30)
        cuteLabel2 = Label(text="Time", height=30)

        timeblock.add_widget(cuteLabel1)
        timeblock.add_widget(insInput1)
        timeblock.add_widget(insInput2)
        timeblock.add_widget(insInput3)
        timeblock.add_widget(cuteLabel2)
        timeblock.add_widget(insInput4)
        timeblock.add_widget(insInput5)
        timeblock.add_widget(insInput6)
        f_widget.add_widget(Label())
        f_widget.add_widget(timeblock)
        f_widget.add_widget(Label())
        f_button1 = Button(text='submit button', on_press=self.pop_submit)
        f_button2 = Button(text='cancel button', on_press=self.pop_cancel)
        f_widget.add_widget(f_button1)
        f_widget.add_widget(f_button2)
        self.pops.open()

Factory.register('DateEditButton', cls=DateEditButton)
Factory.register('DatePopup', cls=DatePopup)