#!/usr/bin/env python3
import datetime
"""
This just holds functions that simulate the behaviour of other functions
"""
g_file = "samplefilename.jpg"

# ----- title
g_title = "A generic title"
def getTitle(p_filename):
    return g_title

def setTitle(p_filename, p_val):
    global g_title
    g_title = p_val
    return True

# ----- artist
g_artists = ["Artist: Jane Doe", "sample artist"]
def getArtists(p_filename):
    return g_artists

def setArtists(p_filename, p_val):
    global g_artists
    g_artists = p_val
    return True

def addArtist(p_filename, p_val):
    global g_artists
    if p_val not in g_artists:
        g_artists.append(p_val)
        return True
    return False

def removeArtist(p_filename, p_val):
    global g_artists
    if p_val in g_artists:
        g_artists.remove(p_val)
        return True
    return False

# ----- description
g_desc = "Sample test string. Look how long this is. This is supposed to be a description." \
           "I think it's pretty great so far."

def getDesc(p_filename):
    return g_desc

def setDesc(p_filename, p_value):
    global g_desc
    if len(p_value)>10 or len(p_value)<3:
        g_desc = p_value
        return True
    else:
        return False

# ----- tag
g_tags = ["sample", "example", "test", "this is a long tag"]
def getTags(p_filename):
    return g_tags

def setTags(p_filename, p_val):
    global g_tags
    g_tags = p_val
    return True

def addTag(p_filename, p_val):
    global g_tags
    if p_val not in g_tags:
        g_tags.append(p_val)
        return True
    return False

def removeTag(p_filename, p_val):
    #print("SimulateOutside.removeTag(",p_filename, ", ", p_val, ")")
    global g_tags
    if p_val in g_tags:
        g_tags.remove(p_val)
        return True
    return False

# ----- rating
g_rating = 3

def containsRating(p_filename):
    return not g_rating==None

def getRating(p_filename):
    if g_rating==None:
        return -1
    return g_rating

def setRating(p_filename, p_val):
    global g_rating
    g_rating = p_val
    return True

def wipeRating(p_filename):
    global g_rating
    g_rating = None
    return True

# ----- source url
g_source = "exampleurl/src/1832.jpg"
def getSource(p_filename):
    return g_source

def setSource(p_filename, p_val):
    global g_source
    g_source = p_val
    return True

# ----- orginal date
#g_originaldate = datetime.datetime(2002, 12, 25, 21, 43, 38)
g_originaldate = None

def containsOrgDate(p_filename):
    return not g_originaldate == None

def getOriginalDate(p_filename):
    #print("SimulateOutside.getOriginalDate()", g_originaldate)
    if g_originaldate==None:
        return datetime.datetime(1, 1, 1, 0, 0, 0)
    return g_originaldate

def setOriginalDate(p_filename, p_val):
    #print("SimulateOutside.setOriginalDate():", p_val, g_originaldate)
    global g_originaldate
    g_originaldate = p_val
    return True

# ----- series
g_series = ("Sample Quest", 12)
#g_series = None

def containsSeries(p_filename):
    return not g_series == None

def getSeries(p_filename):
    if g_series==None:
        return ("", -1)
    return g_series

def setSeries(p_filename, p_name, p_ins):
    global g_series
    g_series = (p_name, p_ins)
    return True

def wipeSeries(p_filename):
    global g_series
    g_series = None
    return True