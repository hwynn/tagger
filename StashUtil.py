#!/usr/bin/env python3


# -------stashing utility functions
"""Note: 'stashing' is a term I made up
which refers to storing several types of
metadata into a single large string.
This should let us store a variety of
metadata in file types that only have
a few metadata tags"""


def containsStash(p_filename):
    """
    TODO
    :param p_filename: name/path of the file
	:type p_filename: string
	:return: True if we have added a stash string
	:rtype: bool
    """
    return


def getStashIndex(p_filename):
    """
    assuming containsStash() is true
    returns a list of the metadata
    similar to: metadata.exif_keys
    TODO
    """
    return


def searchStashIndex(p_filename, p_key):
    """
    assuming containsStash() is true
    this function checks whether or not
    a type of metadata is present in
    the stash index and the stash string
    returns bool

    :return: true if p_key is in the metadata
    :rtype: bool
    """
    return


def addItemToStashIndex(p_filename, p_key):
    """
    assuming searchStashIndex() returns false
    this function adds a new kind of metadata
    to the stash string. Only certain values of p_key
    are allowed to keep metadata consistent across filetypes
    this also adds a blank metadata entry to the stash string
    TODO
    """
    return


def removeItemFromStashIndex(p_filename, p_key):
    """
    assuming searchStashIndex() returns true
    this function removes a type of metadata
    from the stash string and the stash index
    TODO
    """
    return


def setStashData(p_filename, p_key, p_value):
    """
    assuming searchStashIndex() returns true
    this function stores data of a given type
    into the appropriate place in the stash string
    note: this will completely rewrite a type of stash data
    there is no addStashData function. That must be done
    by the individual metadata functions
    TODO
    """
    return


def getStashData(p_filename, p_key):
    """
    assuming searchStashIndex() returns true
    this function returns the value of the given
    metadata type as a string.
    the individual metadata functions
    are responsible for parsing this string
    TODO
    """
    return

import pyexiv2

def display(p_str,p_var):
    print(p_str+":",p_var)
    #print(p_str + " type:", type(p_var))

def trimSquare(x):
    y = x
    if len(y) < 1:
        return y
    while y[-1]=="\x00":
        y = y[:-1]
        if len(y) < 1:
            break
    return y

#filename = '/home/hwynn/Pictures/fixingComputer.jpg'

#f_metadata = pyexiv2.ImageMetadata(filename)
#f_metadata.read()
#f_keywords = f_metadata['Exif.Image.XPKeywords']
#f_dirtyTitleString = pyexiv2.utils.undefined_to_string(f_keywords.value)

"""
undefined_to_string takes a huge string of spaced numbers and converts it to a string with squares

string_to_undefined takes a string with squares and converts it to a huge string of spaced numbers

perfect inverse functions in this situation
"""
"""
x.encode('utf-8') takes x as a string with squares and returns a 'bytes' object of it.

x.encode('utf-8') and bytes(x, 'utf-8') do the exact same thing.
x.encode('utf-16') and bytes(x, 'utf-16') do the exact same thing.
x.decode('utf-16')  takes x as a 'bytes' object and returns a normal string
str() can be used on a 'bytes' object and return the exact data as a string. The reverse does not seem possible.

x.encode('utf-16') takes normal string and converts it to a 'bytes' object of it.
"""
"""
4 objects:
(a) a huge string of spaced numbers         f_keywords.value directly from file                                    raw
(b) a string with squares                   from pyexiv2.utils.undefined_to_string(f_keywords.value) from file  dirtyStr
(c) a 'bytes' object                                                                                            bytes
(d) a normal string                                                                                             cleanStr
"""


def file_to_a(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_keywords = f_metadata['Exif.Image.XPKeywords']
    return f_keywords.value

def file_to_b(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_keywords = f_metadata['Exif.Image.XPKeywords']
    return pyexiv2.utils.undefined_to_string(f_keywords.value)

def file_to_c(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_keywords = f_metadata['Exif.Image.XPKeywords']
    f_item = pyexiv2.utils.undefined_to_string(f_keywords.value)
    f_bytes = bytes(f_item, 'utf-8')
    #f_bytes = f_item.encode('utf-8')
    return f_bytes

def file_to_d(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_keywords = f_metadata['Exif.Image.XPKeywords']
    f_item = pyexiv2.utils.undefined_to_string(f_keywords.value)
    f_bytes = bytes(f_item, 'utf-8')
    #f_bytes = f_item.encode('utf-8')
    f_d = f_bytes.decode('utf-16')
    return trimSquare(f_d)

#--- a transitions

def a_to_b(x):
    return pyexiv2.utils.undefined_to_string(x)

def a_to_c(x):
    f_b = pyexiv2.utils.undefined_to_string(x)
    return f_b.encode('utf-8')

#def a_to_d(x):
def raw_to_cleanStr(x):
    f_b = pyexiv2.utils.undefined_to_string(x)
    f_c = f_b.encode('utf-8')
    f_d = trimSquare(f_c.decode('utf-16'))
    return f_d


#--- b transitions

def b_to_a(x):
    return pyexiv2.utils.string_to_undefined(x)

def b_to_c(x):
    #return bytes(x, 'utf-8')
    return x.encode('utf-8')

#def b_to_d(x):
def dirtyStr_to_cleanStr(x):
    f_c = x.encode('utf-8')
    f_d = f_c.decode('utf-16')
    return trimSquare(f_d)

#--- c transitions

def c_to_a(x):
    f_b = x.decode('utf-8')
    return pyexiv2.utils.string_to_undefined(f_b)

def c_to_b(x):
    return x.decode('utf-8')

def c_to_d(x):
    f_d = x.decode('utf-16')
    return trimSquare(f_d)

#--- d transitions

def d_to_a(x):
    f_c = x.encode('utf-16')
    f_b = f_c[2:].decode('utf-8')
    return pyexiv2.utils.string_to_undefined(f_b)
#def d_to_b(x):
def cleanStr_to_dirtyStr(x):
    f_c = x.encode('utf-16')
    return f_c[2:].decode('utf-8')

def d_to_c(x):
    #return bytes(x, 'utf-16')
    f_c = x.encode('utf-16')
    return f_c[2:]




"""
a1 = file_to_a(filename)

b1 = file_to_b(filename)

c1 = file_to_c(filename)

d1 = file_to_d(filename)

#---conversions to a
a2 = b_to_a(b1)
a3 = c_to_a(c1)
a4 = d_to_a(d1)
#---conversions to b
b2 = a_to_b(a1)
b3 = c_to_b(c1)
b4 = cleanStr_to_dirtyStr(d1)
#---conversions to c
c2 = a_to_c(a1)
c3 = b_to_c(b1)
c4 = d_to_c(d1)
#---conversions to d
d2 = raw_to_cleanStr(a1)
d3 = dirtyStr_to_cleanStr(b1)
d4 = c_to_d(c1)

display("a1",a1)
display("a2",a2)
display("a3",a3)
display("a4",a4)
display("b1",b1)
display("b2",b2)
display("b3",b3)
display("b4",b4)
display("c1",c1)
display("c2",c2)
display("c3",c3)
display("c4",c4)
display("d1",d1)
display("d2",d2)
display("d3",d3)
display("d4",d4)
"""
#----------flow 1
#f_dirtyXString = pyexiv2.utils.undefined_to_string(f_keywords.value)
#f_cleanXList = dirtyStr2cleanList(f_dirtyXString)
#f_keywords.value -> f_dirtyXString -> f_cleanXList
#      a          ->      b         ->    [d]
#      undefined_to_string     dirtyStr2cleanList

#f_dirtyXString2 = cleanList2dirtyStr(f_cleanXList)
#f_value = pyexiv2.utils.string_to_undefined(f_dirtyXString2)
#f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
#f_metadata.write()
#f_cleanXList ->  f_dirtyXString2 -> f_value
#   [d]       ->        b         ->     a
#    cleanList2dirtyStr       string_to_undefined
#NOTE: every use of cleanList2dirtyStr() follows this use pattern


#----------flow 2
#f_dirtyXString = pyexiv2.utils.undefined_to_string(f_keywords.value)
#f_cleanX = dirtyStr2cleanStr(f_dirtyXString)
# f_keywords.value -> f_dirtyXString -> f_cleanX
#     a            ->       b        ->    d
#       undefined_to_string    dirtyStr2cleanStr

