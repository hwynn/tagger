from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, DictProperty, ListProperty
import SimulateOutside

"""
This is a custom class for dynamically creating buttons and closing them.
This is for tag lists in our program.
"""

Builder.load_string('''
<DynamicTag>:
    size_hint: (None, None)
    text: self.ourText
    width: self.texture_size[0] + 69
    height: 29
    pos: (50, 300)
    background_normal: ''
    ArtistLayout:
        size: (root.width, root.height)
        pos: self.parent.pos
        Label:
            size_hint: (None, 1)
            width: self.texture_size[0] + 40
            pos: (0, 0)
            canvas.before:
                Color:
                    rgba: .5, .5, .5, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            text: root.ourText
            background_normal: '..\pics\BlankUpTiny.png'
            background_down: '..\pics\BlankDownTiny.png'
            group: 'test'
        Button:
            size_hint: (None, 1)
            width: 29
            pos: (root.texture_size[0] + 40, 0)
            background_normal: '..\pics\closeUpTiny.png'
            background_down: '..\pics\closeDownTiny.png'
            group: 'test'

<ReadWriteArtistList>:
	spacing: 5, 5
''')

class ReadWriteArtistList(StackLayout):
    c_taglist = ['cat', 'funny', 'jump', 'fail', 'animals']
    dynamic_ids = DictProperty({})  # declare class attribute, dynamic_ids

    def __init__(self, **kwargs):
        super(ReadWriteArtistList, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.populateList(), timeout=0.1)

    def getTarget(self, p_arg):
        # gets the id of the last custom button. Used to accessing it.
        return [x for x in self.children if str(x.__class__.__name__) == p_arg]

    def populateList(self):
        #this adds all the tags to our tag list
        f_taglist = SimulateOutside.getArtists(SimulateOutside.getActiveFilePath())
        for i_tag in f_taglist:
            #similar to addNewArtist() but doesn't just includes pre-existing artists in the gui
            i_id = "Tag:" + i_tag
            i_newArtist = DynamicTag(id=i_id,
                                     ourText=i_tag)
            self.add_widget(i_newArtist)
            self.dynamic_ids[i_id] = i_newArtist
            i_newArtist.children[0].children[0].bind(on_release=self.delayedClose)

    def wipeArtistList(self):
        #this just cleans the gui of artists. It doesn't actually edit any data
        for item in self.dynamic_ids:
            print("wipeArtistList():", item)

    def addNewArtist(self, p_arg):
        f_id = "Tag:"+p_arg
        f_newArtist = DynamicTag(id=f_id,
                              ourText=p_arg)

        #this adds the tag to the file before we add it to our gui
        #this should theoretically stop the function if we tried adding a duplicate tag
        try:
            if SimulateOutside.addArtist(SimulateOutside.getActiveFilePath(), p_arg)==False:
                print("ReadWriteArtistList.addNewArtist(): could not add tag \"", p_arg, "\"", sep='')
                return False
            #TODO: remove this part once the outside function can reliably test if we're adding a duplicate tag
            if f_id in self.dynamic_ids:
                # We don't want duplicate tags
                print("ReadWriteArtistList.addNewArtist(): We already have this tag")
                return False
        except:
            print("ReadWriteArtistList.addNewArtist(): error adding tag")
            return False

        self.add_widget(f_newArtist)
        self.dynamic_ids[f_id] = f_newArtist
        f_newArtist.children[0].children[0].bind(on_release=self.delayedClose)
        return True

    def closeTarget(self, p_targetID):
        #removes a tag from the file and our user interface
        try:
            # this first tries to remove the tag from the file using out metadata library
            if SimulateOutside.removeArtist(SimulateOutside.getActiveFilePath(), p_targetID[4:]):
                # if that succeeds, we try removing it from the list of dynamic tags displayed
                f_target = self.dynamic_ids[p_targetID]
                #print("ReadWriteArtistList.closeTarget(): closing", p_targetID)
                if f_target != None:
                    self.remove_widget(f_target)
                    del self.dynamic_ids[p_targetID]
        except KeyError:
            print("ReadWriteArtistList.closeTarget(): key not in dictionary. Weird")
            print("\tIDs:", self.dynamic_ids)
            print("\ttried:", p_targetID)
        return True

    def delayedClose(self, arg):
        #print("ReadWriteArtistList.delayedClose() arg:\t", arg)
        #print("ReadWriteArtistList.delayedClose() type:\t", type(arg))
        #without lambda here, this would pass the timeout arguement to our function.
        Clock.schedule_once(lambda dt: self.closeTarget(arg.parent.parent.id), timeout=0.01)

    def getArtistList(self):
        f_entrys = []
        for entry in self.dynamic_ids:
            f_entrys.append(self.dynamic_ids[entry].ourText)
        return f_entrys

class DynamicTag(Label):
    ourText = StringProperty("")

    def __init__(self, **kwargs):
        super(DynamicTag, self).__init__(**kwargs)

    def debugSize(self):
        f_textBtn= self.children[0].children[1]
        f_closeBtn = self.children[0].children[0]
        print("FrameStartX:", self.pos[0], end="\t\t\t")
        print("FrameEndX:", self.pos[0] + self.width)
        print("\tTextBtnStartX:", f_textBtn.pos[0], end="\t")
        print("\tTextBtnEndX:", f_textBtn.pos[0]+f_textBtn.width)
        print("\tCloseBtnStartX:", f_closeBtn.pos[0], end="\t")
        print("\tCloseBtnEndX:", f_closeBtn.pos[0]+f_closeBtn.width)
        print()
        print("TextBtnWidthX:", f_textBtn.width, end="\t\t")
        print("TextBtnTextureX:", f_textBtn.texture_size[0], end="\t")
        print("TextBtnExtraX:", f_textBtn.width-f_textBtn.texture_size[0])
        print()
        print("FrameWidth:", self.width, end="\t\t")
        print("TotalButtonWidth:", f_textBtn.width + f_closeBtn.width)
        print("FrameBlackSpace:", self.width-(f_textBtn.width + f_closeBtn.width))

class ArtistLayout(RelativeLayout):
    def __init__(self, **kwargs):
        super(ArtistLayout, self).__init__(**kwargs)

Factory.register('ReadWriteArtistList', cls=ReadWriteArtistList)