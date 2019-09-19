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
<SeriesButton>:
    on_press: self.fire_popup()
<SeriesPopup>:
    id:pop
    size_hint: .4, .6
    pos_hint: {'x': .6, 'y': .2}
    pos: 200, 0
    auto_dismiss: False
    title: 'Pictures in a sequence'

''')

class SeriesPopup(Popup):
    def __init__(self, **kwargs):
        super(SeriesPopup, self).__init__(**kwargs)
    # the widget we add in here actually does everything. so this is empty

# this button is reuasable
class SeriesButton(Button):
    # this is the button that triggers the popup being created

    # these are the two values that make up the series information
    seriesIns = NumericProperty(SimulateOutside.getSeries(SimulateOutside.g_file)[1])
    seriesName = StringProperty(SimulateOutside.getSeries(SimulateOutside.g_file)[0])
    pops = SeriesPopup()

    def __init__(self, **kwargs):
        super(SeriesButton, self).__init__(**kwargs)
        self.c_debug = 0
        self.text = "Edit"

    def setSeriesValue(self, p_name, p_ins):
        # this calls an outside script to set the series value in a picture file
        # then the new value is passed back to us for the user interface to display
        if self.c_debug > 0: print("SeriesButton.setSeriesValue:", p_name, p_ins)
        f_success = SimulateOutside.setSeries(SimulateOutside.g_file, p_name, p_ins)
        if f_success:
            self.seriesName, self.seriesIns = SimulateOutside.getSeries(SimulateOutside.g_file)
        else:
            if self.c_debug > 0: print("setSeriesValue.setValue() operation not successful")

    def pop_cancel(self, instance):
        # any input from the user is discarded and the popup is closed
        if self.c_debug > 0: print("SeriesButton.pop_cancel.instance:", instance)
        self.pops.dismiss()

    def pop_submit(self, instance):
        # this happens when the submit button on the popup is pressed.
        # this checks input, tells the program the input is ready, then closes the popup
        f_nameInput = instance.parent.children[4]  # I think this would be a pointer in c++
        f_insInput = instance.parent.children[2]  # these are the text inputs with the values we will check
        # if the input is invalid, the button shouldn't work.
        # This lets the user know a mistake happened before their work is lost when the popup closes
        if self.isNameValid(f_nameInput.text) and self.isInstallmentValid(f_insInput.text):
            f_name = f_nameInput.text
            f_installment = int(f_insInput.text)
            # to avoid unneeded calls to outside script, lets check if series is these values
            if self.seriesIns == f_installment and self.seriesName == f_name:
                self.pops.dismiss()
            else:
                self.setSeriesValue(f_name, f_installment)
                self.pops.dismiss()
        # special case for 2 empty inputs, implying the user wants to remove series metadata
        if f_nameInput.text=="" and f_insInput.text=="":
            #to avoid unneeded calls to outside script, lets check if series is already nonexistent
            if self.seriesIns==-1 and self.seriesName=="":
                self.pops.dismiss()
            else:
                if SimulateOutside.wipeSeries(SimulateOutside.g_file):
                    self.seriesName, self.seriesIns = ("", -1)
            self.pops.dismiss()
        # TODO: add feedback for bad inputs

    def isNameValid(self, p_name):
        # before we accept this name, we have to check if it's valid
        if p_name != "" and len(p_name) < 100:  # arbitrary name size limit
            return True
        return False

    def isInstallmentValid(self, p_ins):
        # before we accept this installment, we have to check if it's valid
        if p_ins == "":
            return False
        if p_ins.isnumeric():
            if int(p_ins) > (0):
                return True
            # TODO: add exception saying that number isn't valid
        return False

    def fire_popup(self):
        # this builds the interface inside the pupup, then makes it appear on the screen
        f_widget = BoxLayout(orientation='vertical')
        self.pops.content = f_widget

        nameInput = TextInput(multiline=False, size_hint_y=None, height=30, text=self.seriesName,
                              hint_text="series name")
        insInput = TextInput(multiline=False, size_hint_y=None, height=30, input_filter='int', hint_text="#")
        if SimulateOutside.containsSeries(SimulateOutside.g_file):
            insInput.text = str(self.seriesIns)
        else:
            insInput.text = ""

        #these are additional labels we don't need in the user interface
        nameLabel = Label(text="Name of this series")
        insLabel = Label(text="Installment # in series")

        f_widget.add_widget(nameLabel)
        f_widget.add_widget(nameInput)
        f_widget.add_widget(insLabel)
        f_widget.add_widget(insInput)
        #f_widget.add_widget(nameLabel)
        #f_widget.add_widget(insLabel)
        f_button1 = Button(text='Apply Changes', on_press=self.pop_submit)
        f_button2 = Button(text='Cancel', on_press=self.pop_cancel)
        f_widget.add_widget(f_button1)
        f_widget.add_widget(f_button2)
        self.pops.open()

Factory.register('SeriesButton', cls=SeriesButton)
Factory.register('SeriesPopup', cls=SeriesPopup)
