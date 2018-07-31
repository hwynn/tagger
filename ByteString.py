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
    """Takes a freshly translated string list and rims the '\x00' ends off all the strings"""
    print("listHexTrim(", p_rawList, ")")
    return [x.replace('\x00', '') for x in p_rawList]

def stringHexTrim(p_bustedTags):
    f_tags="";
    for y in [x.replace('\x00', '') for x in p_bustedTags]:
        if y!='':
            f_tags+=y;
    return f_tags

def stringHexify(p_newtag):
    f_bustedTag=""
    for x in p_newtag:
        f_bustedTag+= x
        f_bustedTag += '\x00'
    return f_bustedTag

def listContainsTag(p_rawList, p_tag):
    """Takes a freshly translated list and a tag.
    Function returns truth value of that tag existing in that list"""
    print("listContainsTag(", p_rawList, p_tag, ")")
    f_trimList = listHexTrim(p_rawList)
    if p_tag in f_trimList:
        return True
    return False


def printList(p_list):
    for i_str in p_list:
        print(i_str)


def addIntoList(p_rawList, p_tag):
    """Takes a freshly translated list and a tag.
    Function creates a trimmed list with the tag
    inserted at the beginning.
    If tag exists in the list, the trimmed list is simply returned"""
    print("addIntoList(", p_rawList, p_tag, ")")
    f_trimList = listHexTrim(p_rawList)
    # print("list to check:", f_list)
    # print("checking for:", p_tag)
    if p_tag in f_trimList:
        return f_trimList  # tag already is in the list
    f_trimList.insert(0, p_tag)
    return f_trimList


def addPreservList(p_rawList, p_tag):
    """Takes a freshly translated list and a tag.
    Function returns the a list with the tag added.
    If tag exists in the list, the raw list is simply returned.
    This function preserves '\x00' tag endings."""
    print("addPreservList(", p_rawList, p_tag, ")")
    if (listContainsTag(p_rawList, p_tag)):
        return p_rawList
    f_list = p_rawList
    f_list.insert(0, p_tag)
    return f_list


def addTagRaw(p_bl, p_tag):
    """Takes a byte literal of the tags and the tag to add
    This adds the tag and returns it
    as another byte literal of tags"""
    print("addTagRaw(", p_bl, p_tag, ")")
    f_rawList = bl2list(p_bl)
    f_rawList = addPreservList(f_rawList, p_tag)
    f_newbl = list2bl(f_rawList)
    return f_newbl


def addTagTrim(p_bl, p_tag):
    """Takes a byte literal of the tags and the tag to add
    This adds the tag and returns it
    as another byte literal of tags"""
    print("addTagTrim(", p_bl, p_tag, ")")
    f_rawList = bl2list(p_bl)
    f_trimList = addIntoList(f_rawList, p_tag)
    f_newbl = list2bl(f_trimList)
    return f_newbl

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
    f_bustedTagString = pyexiv2.utils.undefined_to_string(p_et.value)
    #print("freshExifTags. file has these tags:", stringHexTrim(f_bustedTagString))
    f_TagList = stringHexTrim(f_bustedTagString).split(';')
    if p_tag not in f_TagList:
        print("the tag \"", p_tag, "\" was not found", sep='')
        return p_et.value
    f_TagList.remove(p_tag)
    f_bustedTagString = stringHexify(';'.join(f_TagList)) + "\x00" + "\x00"
    #print("removeExifTag. file will now have these tags:", stringHexTrim(f_bustedTagString))
    return pyexiv2.utils.string_to_undefined(f_bustedTagString)


# string1 = 'cat;animals;cat in a box'
byte1 = b'c\x00a\x00t\x00;\x00a\x00n\x00i\x00m\x00a\x00l\x00s\x00;\x00c\x00a\x00t\x00 \x00a\x00 \x00b\x00o\x00x\x00\x00\x00'

printList(bl2list(byte1))
#print()
g_list1 = ['cat', 'animals', 'cat in a box']
#print(g_list1)
#print(bl2list(list2bl(g_list1)))
#print()
#print(byte1)
# printList(bl2list(byte1))
#print(list2bl(bl2list(byte1)))
#print()
#print(addIntoList(bl2list(byte1), "cute"))
#print(addIntoList(bl2list(byte1), "cat in a box"))
#print()
#print(addPreservList(bl2list(byte1), "cute"))
#print(addPreservList(bl2list(byte1), "cat in a box"))
#print()
