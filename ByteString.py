#!/usr/bin/env python3

def list2bl(p_list):
    """string List to Byte Literal conversion function"""
    f_string = ';'.join(p_list);
    f_bl = f_string.encode('utf-16');
    return f_bl;

def bl2list(p_bl):
    """Byte Literal to string List conversion function"""
    f_string = p_bl.decode('utf-16')
    return f_string.split(';')

def listHexTrim(p_rawList):
    """Takes a freshly translated string list and rims the '\x00' ends off all the strings"""
    return [x.replace('\x00', '') for x in p_rawList]

def listContainsTag(p_rawList, p_tag):
    """Takes a freshly translated list and a tag.
    Function returns truth value of that tag existing in that list"""
    f_trimList = listHexTrim(p_rawList);
    if p_tag in f_trimList:
        return True;
    return False;

def printList(p_list):
    for i_str in p_list:
        print(i_str);

def addIntoList(p_rawList, p_tag):
    """Takes a freshly translated list and a tag.
    Function creates a trimmed list with the tag
    inserted at the beginning.
    If tag exists in the list, the trimmed list is simply returned"""
    f_trimList = listHexTrim(p_rawList);
    #print("list to check:", f_list)
    #print("checking for:", p_tag)
    if p_tag in f_trimList:
        return f_trimList; #tag already is in the list
    f_trimList.insert(0, p_tag)
    return f_trimList;

def addPreservList(p_rawList, p_tag):
    """Takes a freshly translated list and a tag.
    Function returns the a list with the tag added.
    If tag exists in the list, the raw list is simply returned.
    This function preserves '\x00' tag endings."""
    if(listContainsTag(p_rawList, p_tag)):
        return p_rawList
    f_list = p_rawList;
    f_list.insert(0, p_tag);
    return f_list;

def addTagRaw(p_bl, p_tag):
    """Takes a byte literal of the tags and the tag to add
    This adds the tag and returns it
    as another byte literal of tags"""
    print()
    f_rawList=bl2list(p_bl);
    f_rawList=addPreservList(f_rawList, p_tag);
    f_newbl = list2bl(f_rawList);
    return f_newbl;

def addTagTrim(p_bl, p_tag):
    """Takes a byte literal of the tags and the tag to add
    This adds the tag and returns it
    as another byte literal of tags"""
    print()
    f_rawList=bl2list(p_bl);
    f_trimList=addIntoList(f_rawList, p_tag);
    f_newbl = list2bl(f_trimList);
    return f_newbl;


#string1 = 'cat;animals;cat in a box';
byte1 = b'c\x00a\x00t\x00;\x00a\x00n\x00i\x00m\x00a\x00l\x00s\x00;\x00c\x00a\x00t\x00 \x00i\x00n\x00 \x00a\x00 \x00b\x00o\x00x\x00\x00\x00'

print(bl2list(byte1))
print()
g_list1 = ['cat', 'animals', 'cat in a box']
print(g_list1)
print(bl2list(list2bl(g_list1)))
print()
print(byte1)
#printList(bl2list(byte1))
print(list2bl(bl2list(byte1)))
print()
print(addIntoList(bl2list(byte1), "cute"))
print(addIntoList(bl2list(byte1), "cat in a box"))
print()
print(addPreservList(bl2list(byte1), "cute"))
print(addPreservList(bl2list(byte1), "cat in a box"))
print()
