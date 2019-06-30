from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
#from DynamicButtonList import DynamicTagList
from MetadataManagerL0 import getTags
from TestingManager import tryAddData
import os


Builder.load_string('''
<ContainerBox>:
    orientation: 'vertical'
''')

class ContainerBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)
        c_image = Image(source="pics/psyduck.jpg", allow_stretch=True)
        self.add_widget(c_image)
        c_cb = customButtom()
        self.add_widget(c_cb)

#at sometime after building, try TestingManager.tryAddData('../pics/psyduck.jpg')
class customButtom(Button):
    def __init__(self, **kwargs):
        super(customButtom, self).__init__(**kwargs)

    def on_press(self):
        print(self.parent.children[-1].source)
        #print(getTags("pics/psyduck.jpg"))
        #print(tryAddData("pics/psyduck.jpg"))
        print(getTags("pics/psyduck.jpg"))


class Nested2App(App):
    def build(self):
        return ContainerBox()

    def on_start(self):
            print("Nested2App.on_start: starting")
            print(self.root)
            print("Nested2App.on_start: finishing")
            print()



if __name__ == '__main__':
    Nested2App().run()