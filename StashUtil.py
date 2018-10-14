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
from struct import *
import pyexiv2
"""
print(pack('>hhl', 1, 2, 3))
print(pack('<hhl', 1, 2, 3))
print(type(pack('>hhl', 1, 2, 3)))
print(calcsize('>hhl'))
#b'\x00\x01\x00\x02\x00\x00\x00\x03'
print(unpack('>hhl', b'\x00\x01\x00\x02\x00\x00\x00\x03'))
print(unpack('<hhl', b'\x00\x01\x00\x02\x00\x00\x00\x03'))
print(type(unpack('>hhl', b'\x00\x01\x00\x02\x00\x00\x00\x03')))
##print(calcsize('hhl'))
print(type(b'\x00\x01\x00\x02\x00\x00\x00\x03'))
"""


def display(p_str,p_var):
    print(p_str+":",p_var)
    print(p_str + " type:", type(p_var))


filename = '/home/hwynn/Pictures/fixingComputer.jpg'
f_metadata = pyexiv2.ImageMetadata(filename)
f_metadata.read()
#print(f_metadata.exif_keys)

f_keywords = f_metadata['Exif.Image.XPTitle']
f_dirtyTitleString = pyexiv2.utils.undefined_to_string(f_keywords.value)

"""
undefined_to_string takes a huge string of spaced numbers and converts it to a string with squares

string_to_undefined takes a string with squares and converts it to a huge string of spaced numbers

perfect inverse functions in this situation
"""
"""
4 objects:
(a) a huge string of spaced numbers         f_keywords.value directly from file
(b) a string with squares                   from pyexiv2.utils.undefined_to_string(f_keywords.value) from file
(c) a 'bytes' object
(d) a normal string
"""

def file_to_a(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_keywords = f_metadata['Exif.Image.XPTitle']
    return f_keywords.value

def file_to_b(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_keywords = f_metadata['Exif.Image.XPTitle']
    return pyexiv2.utils.undefined_to_string(f_keywords.value)

def file_to_c(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_keywords = f_metadata['Exif.Image.XPTitle']
    f_item = pyexiv2.utils.undefined_to_string(f_keywords.value)
    f_bytes = bytes(f_item, 'utf-8')
    #f_bytes = f_item.encode('utf-8')
    return f_bytes

def file_to_d(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_keywords = f_metadata['Exif.Image.XPTitle']
    f_item = pyexiv2.utils.undefined_to_string(f_keywords.value)
    f_bytes = bytes(f_item, 'utf-8')
    #f_bytes = f_item.encode('utf-8')
    return f_bytes.decode('utf-16')

def a_to_b(x):
    return pyexiv2.utils.undefined_to_string(x)

def b_to_a(x):
    return pyexiv2.utils.string_to_undefined(x)

def b_to_c(x):
    return x.encode('utf-8')

def d_to_c(x):
    return x.encode('utf-16')

def c_to_d(x):
    return x.decode('utf-16')

def c_to_b(x):
    return x.decode('utf-8')

def d_to_b(x):
    f_c = d_to_c(x)
    return c_to_b(f_c[2:])

"""
x.encode('utf-8') takes x as a string with squares and returns a 'bytes' object of it.

x.encode('utf-8') and bytes(x, 'utf-8') do the exact same thing.
x.encode('utf-16') and bytes(x, 'utf-16') do the exact same thing.
x.decode('utf-16')  takes x as a 'bytes' object and returns a normal string
str() can be used on a 'bytes' object and return the exact data as a string. The reverse does not seem possible.

x.encode('utf-16') takes normal string and converts it to a 'bytes' object of it.
"""
"""

v1 = bytes(f_dirtyTitleString, 'utf-8') #works
#v2 = bytes(f_dirtyTitleString, 'utf-16')
display("v1",v1)
#print(v2)
#v3 = f_dirtyTitleString.decode(encoding='utf-16')
v3 = v1.decode('utf-16')  #works perfectly
display("v3",v3) #works perfectly
v4 = v3.encode('utf-16')
display("v4",v4)
v5 = v4.decode('utf-16')
display("v5",v5)
"""
"""
v6 = pyexiv2.utils.undefined_to_string(f_value4)
display("v6",v6)
v9 = v5.encode('utf-16')
display("v9",v9)
#v6 and v9 are identical except that v9 is 'bytes'
#v6 is string and cannot be made into bytes now
#v6 and str(v9) are identical in every way.
"""

a1 = file_to_a(filename)

b1 = file_to_b(filename)

c1 = file_to_c(filename)

d1 = file_to_d(filename)

c2 = b_to_c(b1)
c3 = d_to_c(d1)
b2 = c_to_b(c1)
a2 = b_to_a(b1)
b3 = a_to_b(a2)
d2 = c_to_d(c3)
b4 = c_to_b(c3[2:])
b5 = d_to_b(d1)



display("a1",a1)
display("a2",a2)
display("b1",b1)
display("b2",b2)
display("b3",b3)
display("b4",b4)
display("b5",b5)
display("c1",c1)
display("c2",c2)
display("cx",c3[2:])
display("c3",c3)
display("d1",d1)
display("d2",d2)

