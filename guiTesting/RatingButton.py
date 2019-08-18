from kivy.app import App
from kivy.lang import Builder
from functools import partial
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import OptionProperty, ListProperty, NumericProperty
from kivy.uix.behaviors import ToggleButtonBehavior
import SimulateOutside


Builder.load_string('''
<RatingButtons>:
    size_hint: None, None
    size: 250, 50
<StatusButton>:
    size_hint: None, None
    size: 50, 50
''')


class StatusButton(Button):
    status = OptionProperty('off', options=('off', 'on'))

    def __init__(self, p_val, **kwargs):
        super(StatusButton, self).__init__(**kwargs)
        self.c_val = p_val #each button has an int value that will be used in callbacks
        self.background_normal = '..\pics\starOff.png'
        self.background_down = '..\pics\starOffDown.png'

    def on_status(self, widget, value):
        #print("StatusButton.on_status()", widget, value)
        if value == 'on':
            self.background_normal = '..\pics\starOn.png'
            self.background_down = '..\pics\starOnDown.png'
        else:
            self.background_normal = '..\pics\starOff.png'
            self.background_down = '..\pics\starOffDown.png'

class RatingButtons(BoxLayout):
    rating = NumericProperty(0)
    buttonList = ListProperty()

    def __init__(self, **kwargs):
        super(RatingButtons, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        for i in range(5):
            i_button = StatusButton(p_val=i+1)
            self.add_widget(i_button)
            self.buttonList.append(i_button)
            i_callback = partial(self.set_rating)
            i_button.bind(on_press=i_callback)

    def set_rating(self, p_button):
        #print("RatingButtons.set_rating()", p_button, p_button.c_val)
        #each button has a different stored value.
        # So rating is set to the value of whatever button is pressed
        #self.rating = p_button.c_val
        #External functions used here
        # this is an indirect way to set the rating value
        # This is how RatingButton is able to communicate with the outside
        f_success = SimulateOutside.setRating(SimulateOutside.g_file, p_button.c_val)
        if f_success:
            self.rating = SimulateOutside.getRating(SimulateOutside.g_file)
        else:
            print("RatingButtons.set_rating() operation not successful")

    def on_rating(self, instance, value):
        #print("RatingButtons.on_rating()", instance, value)
        for i in range(value):
            self.buttonList[i].status = 'on'
        for i in range(value,5):
            self.buttonList[i].status = 'off'


Factory.register('StatusButton', cls=StatusButton)
Factory.register('RatingButtons', cls=RatingButtons)
