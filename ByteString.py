#!/usr/bin/env python3
import pyexiv2

def list2bl(p_list):
    """string List to Byte Literal conversion function"""
    print("list2bl(", p_list, ")")
    f_string = ';'.join(p_list)
    f_bl = f_string.encode('utf-16')
    return f_bl

def bl2list(p_bl):
    """Byte Literal to string List conversion function"""
    print("bl2list(", p_bl, ")")
    f_string = p_bl.decode('utf-16')
    return f_string.split(';')




def listHexTrim(p_rawList):
    """Takes a freshly translated string list and
    trims the '\x00' ends off all the strings"""
    print("listHexTrim(", p_rawList, ")")
    return [x.replace('\x00', '') for x in p_rawList]

def stringHexTrim(p_dirtyTags):
    f_tags=""
    for y in [x.replace('\x00', '') for x in p_dirtyTags]:
        if y!='':
            f_tags+=y
    return f_tags

def stringHexify(p_newtag):
    f_dirtyTag=""
    for x in p_newtag:
        f_dirtyTag+= x
        f_dirtyTag += '\x00'
    return f_dirtyTag




def freshExifTags(p_et, p_tag):
    """takes an ExifTag object and a string with a tag.
    Returns a new ExifTag object with the new tag added to it."""
    f_bl = pyexiv2.utils.undefined_to_string(p_et.value)
    #print("freshExifTags. file has these tags:", stringHexTrim(f_bl))
    if p_tag in stringHexTrim(f_bl):
        print("This file already has the tag \"", p_tag ,"\"", sep='')
        return p_et.value
    f_newTagString = stringHexify(p_tag) + ";\x00" + f_bl
    #print("freshExifTags. file will now have these tags:", stringHexTrim(f_newTagString))
    return pyexiv2.utils.string_to_undefined(f_newTagString)

def removeExifTag(p_et, p_tag):
    """takes an ExifTag object and a string with a tag.
    Returns a new ExifTag object with the tag removed from it."""
    f_dirtyTagString = pyexiv2.utils.undefined_to_string(p_et.value)
    #print("freshExifTags. file has these tags:", stringHexTrim(f_dirtyTagString))
    f_TagList = stringHexTrim(f_dirtyTagString).split(';')
    if p_tag not in f_TagList:
        print("the tag \"", p_tag, "\" was not found", sep='')
        return p_et.value
    f_TagList.remove(p_tag)
    f_dirtyTagString = stringHexify(';'.join(f_TagList)) + "\x00" + "\x00"
    #print("removeExifTag. file will now have these tags:", stringHexTrim(f_dirtyTagString))
    return pyexiv2.utils.string_to_undefined(f_dirtyTagString)

def setExifTags(p_tagList):
    f_dirtyTagString = stringHexify(';'.join(p_tagList)) + "\x00" + "\x00"
    return pyexiv2.utils.string_to_undefined(f_dirtyTagString)

def getExifTags(p_et):
    """takes an ExifTag object and returns a list of tags"""
    f_dirtyTagString = pyexiv2.utils.undefined_to_string(p_et.value)
    f_TagList = stringHexTrim(f_dirtyTagString).split(';')
    return f_TagList

def hasTag(p_et, p_tag):
    f_dirtyTagString = pyexiv2.utils.undefined_to_string(p_et.value)
    if p_tag in stringHexTrim(f_dirtyTagString):
        #print("This file already has the tag \"", p_tag ,"\"", sep='')
        return True
    return False

