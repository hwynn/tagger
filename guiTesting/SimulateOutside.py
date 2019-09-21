#!/usr/bin/env python3
import datetime
import os
"""
This just holds functions that simulate the behaviour of other functions
"""

lapras = {'title': "",
           'artists': [],
           'description': "",
           'tags': [],
           'rating': None,
           'source': "",
           'date': None,
           'series': None}
lugia = {'title': "",
           'artists': [],
           'description': "",
           'tags': [],
           'rating': None,
           'source': "",
           'date': None,
           'series': None}
onix = {'title': "",
           'artists': [],
           'description': "",
           'tags': [],
           'rating': None,
           'source': "",
           'date': None,
           'series': None}
paras = {'title': "",
           'artists': [],
           'description': "",
           'tags': [],
           'rating': None,
           'source': "",
           'date': None,
           'series': None}
psyduck = {'title': "A generic title",
           'artists': ["Artist: Jane Doe", "sample artist"],
           'description': "Sample test string. Look how long this is. This is supposed to be a description. I think it's pretty great so far.",
           'tags': ["sample", "example", "test", "this is a long tag"],
           'rating': 3,
           'source': "exampleurl/src/1832.jpg",
           'date': datetime.datetime(2002, 12, 25, 21, 43, 38),
           'series': ("Sample Quest", 12)}
shinyLobster = {'title': "",
           'artists': [],
           'description': "",
           'tags': [],
           'rating': None,
           'source': "",
           'date': None,
           'series': None}

g_files = {'C:/Users/H/RealDocs/programming.things/projects/scraps/tagger/pics/lapras.png': lapras,
'C:/Users/H/RealDocs/programming.things/projects/scraps/tagger/pics/lugia.png': lugia,
'C:/Users/H/RealDocs/programming.things/projects/scraps/tagger/pics/onix.png': onix,
'C:/Users/H/RealDocs/programming.things/projects/scraps/tagger/pics/paras.png': paras,
'C:/Users/H/RealDocs/programming.things/projects/scraps/tagger/pics/psyduck.jpg': psyduck,
'C:/Users/H/RealDocs/programming.things/projects/scraps/tagger/pics/shinyLobster.jpg': shinyLobster}

# ----- title
g_title = "A generic title"
def getTitle(p_filename):
    return g_files[p_filename]['title']

def setTitle(p_filename, p_val):
    """
    This is actually just a simulation
    :param p_filename: name/path of the file
    :type p_filename: string
    :param p_val: title value we will store
    :type p_val: string

    :return: True if operation was successful
    :rtype: bool
    """
    global g_files
    g_files[p_filename]['title'] = p_val
    return True

# ----- artist
g_artists = ["Artist: Jane Doe", "sample artist"]
def getArtists(p_filename):
    return g_files[p_filename]['artists']

def setArtists(p_filename, p_val):
    global g_files
    g_files[p_filename]['artists'] = p_val
    return True

def addArtist(p_filename, p_val):
    global g_files
    if p_val not in g_files[p_filename]['artists']:
        g_files[p_filename]['artists'].append(p_val)
        return True
    return False

def removeArtist(p_filename, p_val):
    global g_files
    if p_val in g_files[p_filename]['artists']:
        g_files[p_filename]['artists'].remove(p_val)
        return True
    return False

# ----- description
g_desc = "Sample test string. Look how long this is. This is supposed to be a description." \
           "I think it's pretty great so far."

def getDesc(p_filename):
    return g_files[p_filename]['description']

def setDesc(p_filename, p_value):
    global g_files
    if len(p_value)>10 or len(p_value)<3:
        g_files[p_filename]['description'] = p_value
        return True
    else:
        return False

# ----- tag
g_tags = ["sample", "example", "test", "this is a long tag"]
def getTags(p_filename):
    return g_files[p_filename]['tags']

def setTags(p_filename, p_val):
    global g_files
    g_files[p_filename]['tags'] = p_val
    return True

def addTag(p_filename, p_val):
    global g_files
    if p_val not in g_files[p_filename]['tags']:
        g_files[p_filename]['tags'].append(p_val)
        return True
    return False

def removeTag(p_filename, p_val):
    #print("SimulateOutside.removeTag(",p_filename, ", ", p_val, ")")
    global g_files
    if p_val in g_files[p_filename]['tags']:
        g_files[p_filename]['tags'].remove(p_val)
        return True
    return False

# ----- rating
g_rating = 3

def containsRating(p_filename):
    return not g_files[p_filename]['rating']==None

def getRating(p_filename):
    if g_files[p_filename]['rating']==None:
        return -1
    return g_files[p_filename]['rating']

def setRating(p_filename, p_val):
    global g_files
    g_files[p_filename]['rating'] = p_val
    return True

def wipeRating(p_filename):
    global g_files
    g_files[p_filename]['rating'] = None
    return True

# ----- source url
g_source = "exampleurl/src/1832.jpg"
def getSource(p_filename):
    return g_files[p_filename]['source']

def setSource(p_filename, p_val):
    global g_files
    g_files[p_filename]['source']= p_val
    return True

# ----- orginal date
#g_originaldate = datetime.datetime(2002, 12, 25, 21, 43, 38)
g_originaldate = None

def containsOrgDate(p_filename):
    return not g_files[p_filename]['date'] == None

def getOriginalDate(p_filename):
    #print("SimulateOutside.getOriginalDate()", g_originaldate)
    if g_files[p_filename]['date']==None:
        return datetime.datetime(1, 1, 1, 0, 0, 0)
    return g_files[p_filename]['date']

def setOriginalDate(p_filename, p_val):
    #print("SimulateOutside.setOriginalDate():", p_val, g_originaldate)
    global g_files
    g_files[p_filename]['date'] = p_val
    return True

# ----- series
g_series = ("Sample Quest", 12)
#g_series = None

def containsSeries(p_filename):
    return not g_files[p_filename]['series'] == None

def getSeries(p_filename):
    if g_files[p_filename]['series']==None:
        return ("", -1)
    return g_files[p_filename]['series']

def setSeries(p_filename, p_name, p_ins):
    global g_files
    g_files[p_filename]['series'] = (p_name, p_ins)
    return True

def wipeSeries(p_filename):
    global g_files
    g_files[p_filename]['series'] = None
    return True

# ------------------------------------
# -----PATH AND FILE NAVIGATION-------
# ------------------------------------

g_path = "C:/Users/H/RealDocs/programming.things/projects/scraps/tagger/pics/"
g_picFile = 'psyduck.jpg'
g_nextFile = ""
g_prevFile = ""

def makeActiveFile(p_filename, p_path=''):
    #p_filename is just the name of the file. it does not include the path
    print("makeActiveFile():", p_filename)
    #this is to change file we're using, and possibly the path we're using as well
    global g_path
    global g_picFile
    global g_nextFile
    global g_prevFile
    f_oldnext = g_nextFile
    f_oldprev = g_prevFile
    f_file = p_filename
    f_path = p_path
    if p_path=='':
        f_path = g_path
    #insead of checking to see if the file or path we used actually exists, we'll throw an exception
    try:
        g_nextFile = ""
        g_prevFile = ""
        f_dir = os.scandir(f_path)
        x = False
        #this quickly navigates the directory
        for i_file in f_dir:
            if x:
                #this is an extra loop to capture the name of the next file after finding our target file
                g_nextFile = i_file.name
                break
            else:
                #print(i_file.name, "\t\t", i_file.path)
                if i_file.name == f_file:
                    x = True
                    #operation is successful at this point, so these global values are changed here
                    g_picFile = f_file
                    g_path = f_path
                else:
                    g_prevFile = i_file.name
        #if the file doesn't exist, x will have never changed. So we need to throw an exception
        if x == False:
            raise FileNotFoundError(f_file+" not found")
    except Exception as ex:
        print("makeActiveFile() error:", ex)
        #if this didn't work, we return things to how they were before running the function
        g_nextFile = f_oldnext
        g_prevFile = f_oldprev
        return False
    return True

def getActiveFilePath():
    return g_path+g_picFile

def getNext():
    return g_nextFile

def getPrev():
    return g_prevFile