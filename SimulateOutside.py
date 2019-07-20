#!/usr/bin/env python3
import datetime
"""
This just holds functions that simulate the behaviour of other functions
"""

def getTitle(p_filename):
    return "Generic Title"

def setTitle(p_filename, p_val):
    return True

def getArtists(p_filename):
    return ["Artist: Jane Doe", "sample artist"]

def setArtists(p_filename, p_val):
    return True

def getDesc(p_filename):
    return "Sample test string. Look how long this is. This is supposed to be a description." \
           "I think it's pretty great so far."

def setDesc(p_filename, p_value):
    if len(p_value)>10 or len(p_value)<3:
        return True
    else:
        return

def getTags(p_filename):
    return ["sample", "example", "test", "this is a long tag"]

def setTags(p_filename, p_val):
    return True

def getRating(p_filename):
    return 3

def setRating(p_filename, p_val):
    return True

def getSource(p_filename):
    return "exampleurl/src/1832.jpg"

def setSource(p_filename, p_val):
    return True

def getOriginalDate(p_filename):
    return datetime.datetime(1, 7, 5)

def setOriginalDate(p_filename, p_val):
    return True

def getSeries(p_filename):
    return ("Sample Quest", 12)

def setSeries(p_filename, p_name, p_ins):
    return True