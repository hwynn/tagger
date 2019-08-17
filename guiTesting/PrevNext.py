from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

Builder.load_string('''
<NextPrevBar>:
    size: root.size
    pos: root.pos
    id: boxlayout_h
    orientation: 'horizontal'
    Button:
        text: '<<<'
        group: 'test'
    Button:
        text: '>>>'
        group: 'test'
''')


class NextPrevBar(BoxLayout):
    def __init__(self, **kwargs):
        super(NextPrevBar, self).__init__(**kwargs)
