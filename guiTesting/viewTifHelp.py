from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.image import Image

class ContainerBox(BoxLayout):
    def __init__(self, **kwargs):
        super(ContainerBox, self).__init__(**kwargs)
        self.orientation = 'vertical'
        #self.picture = Image(allow_stretch=True, source='..\pics\lugia.png')
        self.picture = Image(allow_stretch=True, source='..\pics\snorlax.tif')
        Clock.schedule_once(lambda dt: self.add_widget(self.picture), timeout=0.1)


class SimpleImage(App):
    def build(self):
        return ContainerBox()

if __name__ == '__main__':
    SimpleImage().run()