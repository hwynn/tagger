#!/usr/bin/env python3
from typing import Dict, List

import pyexiv2
import os
import datetime
from pathlib import PurePosixPath
from pathlib import PureWindowsPath
import dateutil.parser


# ========================================================
# ---------------Defined exceptions-----------------------
# ========================================================
class UnknownFiletypeError(ValueError):
    """Unrecognized filetype (or no filetype)"""
    pass
class UnsupportedFiletypeError(ValueError):
    """Unsupported filetype"""
    pass
class SupportNotImplementedError(NotImplementedError):
    """
    Support not yet implemented
    This exception will occur in cases of acceptable use
    but the functionality is not yet complete.
    """
    pass
class MetadataMissingError(ValueError):
    """File does not have this data.
    Used when we want to remove metadata but none is present."""
    pass
class NoSuchItemError(ValueError):
    """This is similar to MetadataMissing (it shows up in similar contexts)
    But it's raised when data is present, but the item we want to remove
    isn't present in the list"""
    pass
class NoKeysError(ValueError):
    """This is used in get functions. If no appropriate keys are found,
    we raise this error. But contains() functions should always be used first,
    so this exception should never be raised."""
    pass
class DuplicateDataError(ValueError):
    """we raise this when we try to add a tag
    or something similar to a list and the list already has that item"""
    pass
class OutOfRangeError(ValueError):
    """used for setRating"""
    pass
class NotIntegerError(ValueError):
    """used for setRating"""
    pass
class UnsupportedOperationError(ValueError):
    """This operation cannot be done for this tyoe of metadata"""
    pass

# ========================================================
# ------------------Utility functions---------------------
# ========================================================
def getExtension(p_filepathname):
    """!
    this function checks the type of the file.
    Used for png and gif

    :param p_filepathname: the path/name of the file
    :type p_filepathname: string

    :return: the file extension
    :rtype: string
    """
    if os.name == 'nt':
        # this filepath is from windows
        return PureWindowsPath(p_filepathname).suffix
    # assume posix otherwise
    return PurePosixPath(p_filepathname).suffix


def rating2percent(x):
    #input: int of rating
    #output: int of rating percent
    if x==1:
        return 1
    if x==2:
        return 25
    if x==3:
        return 50
    if x==4:
        return 75
    if x==5:
        return 99
    raise OutOfRangeError('number out of range (must be 1..5)')
def rating2percentStr(x):
    #input: int of rating
    #output: string of rating percent
    if x==1:
        return '1'
    if x==2:
        return '25'
    if x==3:
        return '50'
    if x==4:
        return '75'
    if x==5:
        return '99'
    raise OutOfRangeError('number out of range (must be 1..5)')
def percent2rating(x):
    #input: int of rating percent
    #output int, the star rating
    if x==1:
        return 1
    if x==25:
        return 2
    if x==50:
        return 3
    if x==75:
        return 4
    if x==99:
        return 5
    raise OutOfRangeError('not valid rating percents ' + str(x))
def percentStr2rating(x):
    #input: string of rating percent
    # (for some reason pyexiv returns the value of 'Xmp.MicrosoftPhoto.Rating' as a string)
    #input: int
    #output int, the star rating
    if int(x)==1:
        return 1
    if int(x)==25:
        return 2
    if int(x)==50:
        return 3
    if int(x)==75:
        return 4
    if int(x)==99:
        return 5
    raise OutOfRangeError('not valid rating percents ' + x)



#dictionary (keys= metadata types) (values= list of keys for that metadata type for tiff files)


#dictionary (keys= metadata keys) (values= the functions needed to parse the metadata values into clean values)
#dictionary (keys= metadata keys) (values= the functions needed to change clean values into metadata values)
#def key2value      without knowing the parsing details, key to value returns clean value we want

# -------string cleaning utility functions
"""
4 objects:
(raw)       a huge string of spaced numbers     f_keywords.value directly from file
(dirtyStr)  a string with squares               from pyexiv2.utils.undefined_to_string(f_keywords.value) from file
(bytes)     a 'bytes' object
(cleanStr)   a normal string
"""
def trimSquare(x):
    """
    :param x: a string that possibly has one or more '\x00' at the end
    :type x: string
    :return: a completely clean string
    :rtype: string
    """
    y = x
    if len(y) < 1:
        return y
    while y[-1] == '\x00':
        y = y[:-1]
        if len(y) < 1:
            break
    return y

def raw_to_cleanStr(x):
    """
    :param x: a raw metadata value stored as a long string of numbers
    :type x: string
    :return: a clean human-readable string
    :rtype: string
    """
    f_b = pyexiv2.utils.undefined_to_string(x)
    f_c = f_b.encode('utf-8')
    f_d = trimSquare(f_c.decode('utf-16'))
    return f_d
def raw_to_cleanList(x):
    """
    :param x: a raw metadata value stored as a long string of numbers
    :type x: string
    :return: a list of clean human-readable strings
    :rtype: list<string>
    """
    f_b = pyexiv2.utils.undefined_to_string(x)
    f_c = f_b.encode('utf-8')
    f_d = trimSquare(f_c.decode('utf-16'))
    f_cleanXList = f_d.split(';')
    # Note: an empty list represented by f_b translates to
    # the non empty list ['']. This should compensate for that.
    if f_cleanXList == ['']:
        return []
    return f_cleanXList
def cleanStr_to_raw(x):
    """
    :param x: a clean human-readable string
    :type x: string
    :return: a raw metadata value stored as a long string of numbers
    :rtype: string
    """
    f_c = x.encode('utf-16')
    f_b = f_c[2:].decode('utf-8')
    return pyexiv2.utils.string_to_undefined(f_b)
def cleanList_to_raw(x):
    """
    :param x: a list of clean human-readable strings
    :type x: list<string>
    :return: a raw metadata value stored as a long string of numbers
    :rtype: string
    """
    f_cleanXString = ';'.join(x)
    f_c = f_cleanXString.encode('utf-16')
    f_dirtyXString = f_c[2:].decode('utf-8')
    #Note: metadata values cannot be set to no value. This is why we provide a space here.
    if f_dirtyXString=="":
        f_dirtyXString = "\x00\x00"
    f_raw = pyexiv2.utils.string_to_undefined(f_dirtyXString)
    return f_raw

def dirtyStr2cleanStr(p_bustedTags):
    """!
    trims the '\x00' ends off all the characters in a byte-string
    :param p_bustedTags: a single tag in byte-string format
    :type p_bustedTags: string

    :return: a single tag in string format
    :rtype: string
    """
    f_c = p_bustedTags.encode('utf-8')
    f_d = f_c.decode('utf-16')
    f_tags = trimSquare(f_d)
    return f_tags
def cleanStr2dirtyStr(p_newtag):
    """!
    adds the '\x00' on all the characters of a string
    :param p_newtag: a single tag in string format
    :type p_newtag: string

    :return: a single tag in byte-string format
    :rtype: string
    """
    f_c = p_newtag.encode('utf-16')
    return f_c[2:].decode('utf-8')

def dirtyStr2cleanList(p_dirtyTagStr):
    """!
    Takes a byte-string representing a ; delimited list
    trims the '\x00' ends off all the strings
    Name: dirty string means it is filled with \x00
    :param p_dirtyTagStr: ; delimited list represented as a byte-string
    :type p_dirtyTagStr: string

    :return: a list of tags in string format
    :rtype: list<string>
    """
    f_c = p_dirtyTagStr.encode('utf-8')
    f_d = f_c.decode('utf-16')
    f_dirtyXString = trimSquare(f_d)
    f_cleanXList = f_dirtyXString.split(';')
    # Note: an empty list represented by p_dirtyTagStr translates to
    # the non empty list ['']. This should compensate for that.
    if f_cleanXList == ['']:
        return []
    return f_cleanXList
def cleanList2dirtyStr(p_cleanTagList):
    """!
    :param p_cleanTagList: a list of tags in string format
    :type p_cleanTagList: list<string>

    :return: ; delimited list represented as a byte-string
    :rtype: string
    """
    f_cleanXString = ';'.join(p_cleanTagList)
    f_c = f_cleanXString.encode('utf-16')
    f_dirtyXString = f_c[2:].decode('utf-8')
    # Note: metadata values cannot be set to no value. This is why we provide a space here.
    if f_dirtyXString == "":
        return "\x00\x00"
    return f_dirtyXString

def cleanStr2cleanList(p_cleanTagList):
    """
    :param p_cleanTagList: ; delimited list represented as a string
    :type p_cleanTagList: string

    :return: a list of tags in string format
    :rtype: list<string>
    """
    return p_cleanTagList.split(';')
def cleanList2cleanStr(p_cleanTagList):
    """!
    :param: p_cleanTagList: a list of tags in string format
    :type: p_cleanTagList: list<string>

    :return: ; delimited list represented as a string
    :rtype: list<string>
    """
    return ";".join(p_cleanTagList)

# -------additional transformation functions
"""
The translation functions
these single parameter functions are used to automatically parse metadata values
these functions are called by another function that determines which translation is needed
"""
def valTranslateFromDictDef(p_dict):
    """!
    returns what you give it and does nothing
    :param p_dict: a dictionary containing a value like title
    :type p_dict: dictionary

    :raise KeyError: if the 'x-default' is not in p_dict

    :return: the value in the dictionary assigned to the key 'x-default'
    :rtype: string
    """
    return p_dict['x-default']

def valTranslateToDictDef(p_val):
    """!
    returns what you give it and does nothing
    :param p_val: a value like title
    :type p_val: string

    :raise KeyError: if the 'x-default' is not in p_dict

    :return: dictionary with the given value assigned to the key 'x-default'
    :rtype: dictionary
    """
    f_dict = {'x-default': p_val}
    return f_dict

def valTranslateNone(p_val):
    """!
    returns what you give it and does nothing
    :param p_val: what you give it
    :type p_file: unknown

    :return: the parameter passed in with no change and no side effects
    :rtype: unknown
    """
    return p_val
#https://codeyarns.com/2017/10/12/how-to-convert-datetime-to-and-from-iso-8601-string/
def Iso8601_to_date(p_isodate):
    """
    :param p_isodate: the date in ISO 8601 string format
    :type p_isodate: string

    :return: a date
    :rtype: datetime object
    """
    f_parsedDate = dateutil.parser.parse(p_isodate)
    return f_parsedDate
def date_to_Iso8601(p_date):
    """
    :param p_date: a date
    :type p_date: datetime object

    :return: the date in ISO 8601 string format
    :rtype: string
    """
    f_unparsedDate = p_date.isoformat()
    return f_unparsedDate

#--------------------------------------
#-------Key data and operations--------
#--------------------------------------

#dictionary (keys= metadata types) (values= list of keys for that metadata type for jpg files)
# Note: the order of these keys is not arbitrary.
# Get functions will use the leftmost availible key in the list
# So we are assuming the correct key is the earliest in the list, in case of mismatched values.
g_jpgKeys = {
    "Title": ['Exif.Image.XPTitle', 'Xmp.dc.title', 'Xmp.dc.description'],
    "Description": ['Exif.Image.XPComment'],
    "Rating": ['Exif.Image.Rating', 'Exif.Image.RatingPercent', 'Xmp.xmp.Rating', 'Xmp.MicrosoftPhoto.Rating'],
    "Tags": ['Exif.Image.XPKeywords', 'Xmp.dc.subject', 'Xmp.MicrosoftPhoto.LastKeywordXMP'],
    "Artist": ['Exif.Image.Artist', 'Exif.Image.XPAuthor', 'Xmp.dc.creator'],
    "Date Created": ['Exif.Photo.DateTimeOriginal', 'Exif.Photo.DateTimeDigitized', 'Xmp.MicrosoftPhoto.DateAcquired', 'Xmp.xmp.CreateDate']
}
g_tiffKeys = {
    "Title": ['Exif.Image.XPTitle', 'Exif.Image.ImageDescription', 'Xmp.dc.title', 'Xmp.dc.description'],
    "Description": ['Exif.Image.XPComment'],
    "Rating": ['Exif.Image.Rating', 'Exif.Image.RatingPercent', 'Xmp.xmp.Rating', 'Xmp.MicrosoftPhoto.Rating'],
    "Tags": ['Exif.Image.XPKeywords', 'Xmp.dc.subject'],
    "Artist": ['Exif.Image.Artist', 'Exif.Image.XPAuthor', 'Xmp.dc.creator'],
    "Date Created": ['Exif.Photo.DateTimeOriginal', 'Exif.Photo.DateTimeDigitized', 'Xmp.MicrosoftPhoto.DateAcquired']
}
g_pngKeys = {
    "Title": ['Exif.Image.XPTitle', 'Xmp.dc.title', 'Xmp.dc.description'],
    "Description": ['Exif.Image.XPComment'],
    "Rating": ['Exif.Image.Rating', 'Exif.Image.RatingPercent', 'Xmp.xmp.Rating', 'Xmp.MicrosoftPhoto.Rating'],
    "Tags": ['Exif.Image.XPKeywords', 'Xmp.dc.subject', 'Xmp.MicrosoftPhoto.LastKeywordXMP'],
    "Artist": ['Exif.Image.Artist', 'Exif.Image.XPAuthor', 'Xmp.dc.creator'],
    "Date Created": ['Exif.Photo.DateTimeOriginal', 'Exif.Photo.DateTimeDigitized', 'Xmp.MicrosoftPhoto.DateAcquired', 'Xmp.xmp.CreateDate']
}

g_keylists: Dict[str, Dict[str, List[str]]] = {
    '.jpg': g_jpgKeys,
    '.tiff': g_tiffKeys,
    '.png': g_pngKeys
}

def appropriateKeys(p_file, p_metatype):
    """!
    returns keys associated with that metadata type that work with that file
    :param p_file: name/path of the file
    :type p_file: string
    :param p_metatype: a metadata type (Title, Description, Tags, etc)
    :type p_metatype: string

    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, tiff, or .gif
    :raise KeyError: if the p_metatype is not in f_keydict

    :return: list of keys that the file can store p_metatype data in
    :rtype: list<string>
    """
    # TODO support for gif, tiff, and png
    f_filetype = getExtension(p_file)
    if f_filetype not in g_keylists:
        raise UnsupportedFiletypeError(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png, gif'.format(p_file))
    f_keydict = g_keylists[f_filetype]
    f_keys = f_keydict[p_metatype]
    return f_keys

def keyHoldingValue(p_file, p_metatype):
    """!
    In get() functions, we cannot assume all keyvalue pairs for a metadata type
    are present and matching. But checking this is too costly.
    so we pick a key that is most likely to be correct
    :param p_file: name/path of the file
    :type p_file: string
    :param p_metatype: a metadata type (Title, Description, Tags, etc)
    :type p_metatype: string

    :raise NoKeysError: if no keys were present. Shouldn't happen if contains() is checked beforehand

    :return: a single key that we assume contains the correct value
    :rtype: string
    """
    f_metadata = pyexiv2.ImageMetadata(p_file)
    f_metadata.read()
    for i_key in appropriateKeys(p_file, p_metatype):
        if i_key in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            return i_key
    raise NoKeysError("no keys for this metadata type found. You should've checked this before.")

#these change values from file metadata into human readable values
g_translaters = {'Exif.Image.XPTitle': raw_to_cleanStr,
                 'Exif.Image.XPSubject': raw_to_cleanStr,
                 'Exif.Image.XPComment': raw_to_cleanStr,
                 'Exif.Image.XPKeywords': raw_to_cleanList,
                 'Exif.Image.XPAuthor': raw_to_cleanList,
                 'Xmp.dc.title': valTranslateFromDictDef,
                 'Xmp.dc.description': valTranslateFromDictDef,
                 'Xmp.dc.subject': valTranslateNone,
                 'Xmp.MicrosoftPhoto.LastKeywordXMP': valTranslateNone,
                 'Exif.Image.Artist': cleanStr2cleanList,
                 'Xmp.dc.creator': valTranslateNone,
                 'Exif.Image.Rating': valTranslateNone,
                 'Xmp.xmp.Rating': valTranslateNone,
                 'Exif.Image.RatingPercent': percent2rating,
                 'Xmp.MicrosoftPhoto.Rating': percentStr2rating,
                 'Exif.Photo.DateTimeOriginal': valTranslateNone,
                 'Exif.Photo.DateTimeDigitized': valTranslateNone,
                 'Xmp.MicrosoftPhoto.DateAcquired': Iso8601_to_date,
                 'Xmp.xmp.CreateDate':Iso8601_to_date
                 }
#these change human readable values into values we can store in files
g_untranslaters = {'Exif.Image.XPTitle': cleanStr_to_raw,
                 'Exif.Image.XPSubject': cleanStr_to_raw,
                 'Exif.Image.XPComment': cleanStr_to_raw,
                 'Exif.Image.XPKeywords': cleanList_to_raw,
                 'Exif.Image.XPAuthor': cleanList_to_raw,
                 'Xmp.dc.title': valTranslateToDictDef,
                 'Xmp.dc.description': valTranslateToDictDef,
                 'Xmp.dc.subject': valTranslateNone,
                 'Xmp.MicrosoftPhoto.LastKeywordXMP': valTranslateNone,
                 'Exif.Image.Artist': cleanList2cleanStr,
                 'Xmp.dc.creator': valTranslateNone,
                 'Exif.Image.Rating': valTranslateNone,
                 'Xmp.xmp.Rating': valTranslateNone,
                 'Exif.Image.RatingPercent': rating2percent,
                 'Xmp.MicrosoftPhoto.Rating': rating2percentStr,
                 'Exif.Photo.DateTimeOriginal': valTranslateNone,
                 'Exif.Photo.DateTimeDigitized': valTranslateNone,
                 'Xmp.MicrosoftPhoto.DateAcquired': date_to_Iso8601,
                 'Xmp.xmp.CreateDate': date_to_Iso8601
                 }
#TODO make unit tests that uses these dictionaries
#for every key, its translate and untranslate function should be one to one

# ========================================================
# ---------------Error checking functions-----------------
# ========================================================
def filecheck(p_filename):
    """!
    this function checks the type of the file.
    Used for png and gif

    :param p_filename: the type of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype is not recognized
    :raise UnsupportedFiletypeError: if the filetype is recognized but not supported
    """
    if len(p_filename) < 5:
        f_error = "Filename '{}' is too short to have any accepted filename extension".format(p_filename)
        raise UnknownFiletypeError(f_error)
    if getExtension(p_filename) == '':
        raise UnknownFiletypeError(
            'Filename \'{}\' has no extension. What even is this hot mess you gave us?'.format(p_filename))
    if getExtension(p_filename) != '.jpg' and getExtension(p_filename) != '.png' and getExtension(p_filename) != '.gif':
        raise UnsupportedFiletypeError(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png, gif'.format(p_filename))
    return
def earlySupportCheck(p_filename):
    """!
    this function checks the type of the file.
    Used for png and gif

    :param p_filename: the type of the file
    :type p_filename: string

    :raise SupportNotImplementedError: if type of given file should be supported
    but that support has not yet been implemented
    """
    if getExtension(p_filename) not in g_keylists:
        raise SupportNotImplementedError(
            'Sorry. This operation not ready to support \'{}\' files yet.'.format(getExtension(p_filename)))
    return
def alpha1SupportCheck(p_filename):
    """!
    this function checks the type of the file.
    it will raise an exception if this type of file should be supported
    Used for completely unfinished functions

    :param p_filename: the type of the file
    :type p_filename: string

    :raise SupportNotImplementedError: if this type of file is recognized
    """
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.gif':
        raise SupportNotImplementedError('Sorry. This operation is not ready for anything.')
    return



#--------------------------------------
#---------Metadata operations----------
#--------------------------------------
# ========================================================
# ---------------MetaData functionality-------------------
# ========================================================

# ------edit title metadata
def containsTitle(p_filename):
    """!
    This will tell us if the file
    has any title metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if file has title metadata
    :rtype: bool
    """
    filecheck(p_filename)
    earlySupportCheck(p_filename)
    f_possibleKeys = appropriateKeys(p_filename, "Title")
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    for i_key in f_possibleKeys:
        if i_key in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            return True
    # print("this file has no title data")
    return False
def getTitle(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: title if it exists. Else, ""
    :rtype: string
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        if not containsTitle(p_filename):
            return ""
        f_key = keyHoldingValue(p_filename, "Title")
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_cleanTitle = g_translaters[f_key](f_metadata[f_key].value)
        # print("clean Title:", f_cleanTitle)
        return f_cleanTitle
    else:
        earlySupportCheck(
            p_filename)  # TODO gif support
    return ""
def setTitle(p_filename, p_setTitleToThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_setTitleToThis: title we will store as title metadata
	:type p_setTitleToThis: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_key = "Exif.Image.XPTitle"
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_value = cleanStr_to_raw(p_setTitleToThis)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return
def searchTitle(p_filename, p_searchForThis):
    """
    takes: filename as string (including path)
    returns: truth value of p_searchForThis being in the title
    always returns false when no title exists

    # Note: Title does not need to be entire search term to return true
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_searchForThis: title that we're checking for
    :type p_searchForThis: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if p_searchForThis was in title metadata
    :rtype: bool
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsTitle(p_filename):
            return False
        f_keywords = f_metadata["Exif.Image.XPTitle"]
        f_cleanTitle = raw_to_cleanStr(f_keywords.value)

        if p_searchForThis in f_cleanTitle:
            return True
    else:
        earlySupportCheck(
            p_filename)  # TODO add gif support
    return False
def wipeTitle(p_filename):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    :raise MetadataMissingError: if the file has no title metadata
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_key = 'Exif.Image.XPTitle'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        if not containsTitle(p_filename):
            raise MetadataMissingError("there is no title to remove")
        f_value = cleanStr_to_raw(" ")
        # we set the value to (almost) nothing before removing the key just in case the values stick around
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        f_metadata.__delitem__(f_key)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return


# ------edit artist metadata
def containsArtists(p_filename):
    """!
    This will tell us if the file
    has any artist metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if file has artist metadata
    :rtype: bool
    """
    filecheck(p_filename)
    earlySupportCheck(p_filename)
    f_possibleKeys = appropriateKeys(p_filename, "Artist")
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    for i_key in f_possibleKeys:
        if i_key in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            return True
    # print("this file has no artist data")
    return False
def getArtists(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: list of artists if it exists. Else, []
    :rtype: list<string>
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        if not containsArtists(p_filename):
            return []
        f_key = keyHoldingValue(p_filename, "Artist")
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_cleanXList = g_translaters[f_key](f_metadata[f_key].value)
        return f_cleanXList
    else:
        earlySupportCheck(
            p_filename)  # TODO add gif support
    return []
def setArtists(p_filename, p_cleanArtistList):
    """
    Instead of appending a new artist to the list of artists already present
    This function replaces all artists with the list of artists provided as p_cleanArtistList.
    Use this function with caution. Because.. you know. It wipes your artists.

    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_cleanArtistList: a list of artists we will set artist metadata to
    :type p_cleanArtistList: list<string>

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_key = 'Exif.Image.XPAuthor'
        # print(f_metadata.exif_keys)
        f_value = cleanList_to_raw(p_cleanArtistList)

        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add gif support
        return
def searchArtists(p_filename, p_artist):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_artist: artist we are searching for in the metadata
	:type p_artist: string


    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if p_artist was in artist metadata
    :rtype: bool
    """
    filecheck(p_filename)

    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metaData = pyexiv2.ImageMetadata(p_filename)
        f_metaData.read()
        if not containsArtists(p_filename):
            return False
        f_keywords = f_metaData['Exif.Image.XPAuthor']
        # Note: the conditions for finding an artist are very relaxed.
        # We're only searching for a substring.
        # so if an artist entry is "composer: Sarah Sharp"
        # searches for: "composer", "Sarah Sharp", "Sarah", "sharp", and "Sar"
        # will all return true.
        # Perhaps a strictSearchArtists() function is needed
        f_found = False
        f_cleanXList = raw_to_cleanList(f_keywords.value)
        for i_artist in f_cleanXList:
            if p_artist.lower() in i_artist.lower():
                f_found = True
                break
        return f_found
    else:
        earlySupportCheck(
            p_filename)  # TODO add gif support
    return False
def addArtist(p_filename, p_artist):
    """
    appends new artist to the artist metadata

    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_artist: artist we are adding into the artist metadata
	:type p_artist: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    :raise DuplicateDataError: if the file already has this artist in its artist metadata
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        f_key = 'Exif.Image.XPAuthor'
        f_key2 = 'Exif.Image.Artist'
        if not containsArtists(p_filename):
            f_cleanXList = [p_artist]
            f_value = cleanList_to_raw(f_cleanXList)
            f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
            f_metadata.write()
            f_metadata[f_key2] = pyexiv2.ExifTag(f_key2, cleanList2cleanStr(f_cleanXList))
            f_metadata.write()
            return
        f_keywords = f_metadata['Exif.Image.XPAuthor']
        f_cleanXList = raw_to_cleanList(f_keywords.value)
        # print("addArtist() f_cleanXList\t\t", f_cleanXList)
        if p_artist in f_cleanXList:
            raise DuplicateDataError("file already contains this artist")
        f_cleanXList.insert(0, p_artist)
        f_value = cleanList_to_raw(f_cleanXList)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(
            p_filename)  # TODO add gif support
    return
def removeArtist(p_filename, p_artist):
    """
    removes artist from artist metadata

    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_artist: artist we are removing from the artist metadata
	:type p_artist: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    :raise MetadataMissingError: if the file has no artist metadata
    :raise NoSuchItemError: if the file does not have p_artist in their artist list
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsArtists(p_filename):
            raise MetadataMissingError(
                'The file \'{}\' does not contain any artist data \n This operation cannot be performed'.format(
                    p_filename))
        f_keywords = f_metadata['Exif.Image.XPAuthor']
        f_key = 'Exif.Image.XPAuthor'
        f_cleanXList = raw_to_cleanList(f_keywords.value)
        # print("removeArtist() f_cleanXList\t\t", f_cleanXList)
        # Note that p_artist must be an exact match with an entry to have it removed
        if p_artist not in f_cleanXList:
            raise NoSuchItemError(
                'The file \'{}\' does not contain the artist \'{}\' \n This operation cannot be performed'.format(
                    p_filename, p_artist))
        f_cleanXList.remove(p_artist)
        f_value = cleanList_to_raw(f_cleanXList)
        # print("removeArtist() f_value\t\t", f_value)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(
            p_filename)  # TODO add gif support
    return


# -----edit tag metadata
def containsTags(p_filename):
    """!
    This will tell us if the file
    has any tag metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if file has tag metadata
    :rtype: bool
    """
    filecheck(p_filename)
    earlySupportCheck(p_filename)
    f_possibleKeys = appropriateKeys(p_filename, "Tags")
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    for i_key in f_possibleKeys:
        if i_key in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            return True
    # print("this file has no tag data")
    return False
def getTags(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: list of tags if it exists. Else, []
    :rtype: list<string>
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_key = keyHoldingValue(p_filename, "Tags")
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_cleanXList = g_translaters[f_key](f_metadata[f_key].value)
        return f_cleanXList
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return []
def setTags(p_filename, p_cleanTagList):
    """
    Instead of appending a new tag to the list of tags already present
    This function replaces all tags with the list of tags provided as p_cleanTagList.
    Use this function with caution. Because.. you know. It wipes your tags.
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_cleanTagList: list of tags that tag metadata will be set to
	:type p_cleanTagList: list<string>

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_key = 'Exif.Image.XPKeywords'
        # print(f_metadata.exif_keys)
        f_value = cleanList_to_raw(p_cleanTagList)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return True
    else:
        earlySupportCheck(p_filename)
        # TODO add gif support
        return True
def searchTags(p_filename, p_tag):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_tag: tag we will search the tag metadata for
	:type p_tag: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if p_tag was in tag metadata
    :rtype: bool
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metaData = pyexiv2.ImageMetadata(p_filename)
        f_metaData.read()
        if not containsTags(p_filename):
            return False
        f_keywords = f_metaData['Exif.Image.XPKeywords']
        # Note: these are strict searches. They are case sensative
        # non case sensative searches may require longer execution time
        f_cleanXList = raw_to_cleanList(f_keywords.value)
        if p_tag in f_cleanXList:
            return True
    else:
        earlySupportCheck(p_filename)
        # TODO add gif support
        # TODO error check: does this file have tag data?
        return False
    return False
def addTag(p_filename, p_tag):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_tag: tag you will be adding to the tag metadata
	:type p_tag: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    :raise DuplicateDataError: if the file already has this tag in its tag metadata
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        f_key = 'Exif.Image.XPKeywords'
        if not containsTags(p_filename):
            f_cleanXList = [p_tag]
            f_value = cleanList_to_raw(f_cleanXList)
            f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
            f_metadata.write()
            return
        f_keywords = f_metadata['Exif.Image.XPKeywords']
        f_cleanXList = raw_to_cleanList(f_keywords.value)
        # print("addTag() f_cleanXList\t\t", f_cleanXList)
        if p_tag in f_cleanXList:
            raise DuplicateDataError("file already contains this tag")
        f_cleanXList.insert(0, p_tag)
        f_value = cleanList_to_raw(f_cleanXList)

        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return
def removeTag(p_filename, p_tag):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_tag: tag you will be removing from the tag metadata
	:type p_tag: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    :raise MetadataMissingError: if the file has no tag metadata
    :raise NoSuchItemError: if the file does not have p_artist in their tag list
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsTags(p_filename):
            raise MetadataMissingError(
                'The file \'{}\' does not contain any tag data \n This operation cannot be performed'.format(
                    p_filename))
        f_keywords = f_metadata['Exif.Image.XPKeywords']
        f_key = 'Exif.Image.XPKeywords'
        f_cleanXList = raw_to_cleanList(f_keywords.value)
        # print("removeTag() f_cleanXList\t\t", f_cleanXList)
        if p_tag not in f_cleanXList:
            raise NoSuchItemError(
                'The file \'{}\' does not contain the tag \'{}\' \n This operation cannot be performed'.format(
                    p_filename, p_tag))
        f_cleanXList.remove(p_tag)
        # print("removeTag() f_cleanXList\t\t", f_cleanXList)
        f_value = cleanList_to_raw(f_cleanXList)
        # print("removeTag() f_value\t\t", f_value)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return


# -------edit description metadata
def containsDescr(p_filename):
    """!
    This will tell us if the file
    has any Description metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if file has description metadata
    :rtype: bool
    """
    filecheck(p_filename)
    earlySupportCheck(p_filename)
    f_possibleKeys = appropriateKeys(p_filename, "Description")
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    for i_key in f_possibleKeys:
        if i_key in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            return True
    # print("this file has no description data")
    return False
def getDescr(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: description if it exists. Else, ""
    :rtype: string
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        if not containsDescr(p_filename):
            return ""
        f_key = keyHoldingValue(p_filename, "Description")
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_cleanDescr = g_translaters[f_key](f_metadata[f_key].value)
        # print("clean Descr:", f_cleanDescr)
        return f_cleanDescr
    else:
        earlySupportCheck(
            p_filename)  # TODO add gif support
    return ""
def setDescr(p_filename, p_setDescrToThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_setDescrToThis: description metadata will be set to this
	:type p_setDescrToThis: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_key = 'Exif.Image.XPComment'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_value = cleanStr_to_raw(p_setDescrToThis)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return
def searchDescr(p_filename, p_searchForThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_searchForThis: description that we're checking for
    :type p_searchForThis: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if p_searchForThis was in description metadata
    :rtype: bool
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsDescr(p_filename):
            return False
        f_keywords = f_metadata['Exif.Image.XPComment']
        f_cleanDescr = raw_to_cleanStr(f_keywords.value)
        if p_searchForThis in f_cleanDescr:
            return True
    else:
        earlySupportCheck(
            p_filename)  # TODO add gif support
    return False
def addDescr(p_filename, p_addThisToDescr):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_addThisToDescr: string you will be appending to the description metadata
	:type p_addThisToDescr: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_key = 'Exif.Image.XPComment'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_cleanDescr = ""
        if containsDescr(p_filename):
            f_keywords = f_metadata['Exif.Image.XPComment']
            f_cleanDescr = raw_to_cleanStr(f_keywords.value)
        f_setDescrToThis = f_cleanDescr + p_addThisToDescr
        f_value = cleanStr_to_raw(f_setDescrToThis)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return
def wipeDescr(p_filename):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    :raise MetadataMissingError: if the file has no description metadata
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_key = 'Exif.Image.XPComment'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        if not containsDescr(p_filename):
            raise MetadataMissingError("there is no description to remove")
        # we set the value to (almost) nothing before removing the key just in case the values stick around
        f_value = cleanStr_to_raw(" ")
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        f_metadata.__delitem__(f_key)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return


# ------edit rating metadata
def containsRating(p_filename):
    """!
    This will tell us if the file
    has any rating metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if file has rating metadata
    :rtype: bool
    """
    filecheck(p_filename)
    earlySupportCheck(p_filename)
    f_possibleKeys = appropriateKeys(p_filename, "Rating")
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    for i_key in f_possibleKeys:
        if i_key in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            return True
    # print("this file has no rating data")
    return False
def getRating(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: rating if it exists. Else, -1
    :rtype: int
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        if not containsRating(p_filename):
            return -1
        f_key = keyHoldingValue(p_filename, "Rating")
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_rating = g_translaters[f_key](f_metadata[f_key].value)
        return f_rating
    else:
        earlySupportCheck(
            p_filename)  # TODO add gif support
    return -1
def setRating(p_filename, p_setRatingToThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_setRatingToThis: rating metadata will be set to this
	:type p_setRatingToThis: int

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    :raise OutOfRangeError: if p_setRatingToThis is not between 1 to 5
    :raise NotIntegerError: if p_setRatingToThis is not a whole number
    """
    if not (1 <= p_setRatingToThis <= 5):
        raise OutOfRangeError('number out of range (must be 1..5)')
    if not isinstance(p_setRatingToThis, int):
        raise NotIntegerError('non-integers can not be used')
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_key = 'Exif.Image.Rating'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()

        f_value = p_setRatingToThis
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return
def searchRating(p_filename, p_searchForThisRating):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_searchForThisRating: rating that we're checking for
    :type p_searchForThisRating: int

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    :raise OutOfRangeError: if p_setRatingToThis is not between 1 to 5
    :raise NotIntegerError: if p_setRatingToThis is not a whole number

    :return: True if p_searchForThisRating matched rating metadata
    :rtype: bool
    """
    if not (-1 <= p_searchForThisRating <= 5):
        # Note: the reason we allow for searches of 0 and -1
        # is that theoretically, getRating() is used to get the value for searching
        # and it returns -1 if the file contains no rating.
        # we don't actually use getRating() for this search functtion
        # But we might change this function to work that way.
        raise OutOfRangeError('number out of range (must be 1..5)')
    if not isinstance(p_searchForThisRating, int):
        raise NotIntegerError('non-integers can not be used')
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        if not containsRating(p_filename):
            return False
        f_keywords = f_metadata['Exif.Image.Rating']
        f_rating = f_keywords.value
        if f_rating == p_searchForThisRating:
            return True
    else:
        earlySupportCheck(p_filename)
        # TODO add gif support
        # TODO error check: does this file have rating data?
        return False
    return False

# TODO def wipeRating(p_filename):

# ------edit metadata that can store source url
def containsSrc(p_filename):
    """!
    This will tell us if the file
    has any source url metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if file has source url metadata
    :rtype: bool
    """
    filecheck(p_filename)
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    earlySupportCheck(p_filename)
    if ((getExtension(p_filename) == '.jpg') and ('Exif.Image.ImageHistory' in f_metadata.exif_keys)):
        # print("this file already has history/source data")
        return True
    # print("this file has no history/source data")
    return False
def getSrc(p_filename):
    """!
    src info is planned to be used to store picture origin url
     along with the history of edits this software has performed upon it

    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: source url if it exists. Else, ""
    :rtype: string
    """
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsSrc(p_filename):
            return ""
        f_keywords = f_metadata['Exif.Image.ImageHistory']
        f_SrcString = f_keywords.value
        return f_SrcString
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return ""
def addSrc(p_filename, x):
    """
    appends source info to the end of the current src info
    we don't want src info to be removed.
     But we do allow more to be added

    :param p_filename: name/path of the file
	:type p_filename: string
	:param x: source url metadata will be set to this
	:type x: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    """
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_key = 'Exif.Image.ImageHistory'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # this is an append, so we fetch any src data to add
        f_value = getSrc(p_filename)
        # Note the line break. This means all future added data begins on a new line'
        if f_value == "":
            f_value = x
        else:
            f_value = f_value + "\n" + x
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return
def searchSrc(p_filename, p_searchForThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_searchForThis: sourrce url that we're checking for
    :type p_searchForThis: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: returns true is p_searchForThis is found anywhere in the src string
    :rtype: bool
    """
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsSrc(p_filename):
            return False
        f_cleanSrc = getSrc(p_filename)
        if p_searchForThis in f_cleanSrc:
            return True
    else:
        earlySupportCheck(p_filename)
        # TODO add gif support
        # TODO error check: does this file have Src data?
        return False
    return False


# -------edit orginal date

def containsOrgDate(p_filename):
    """!
    This will tell us if the file
    has any original date metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if file has original date metadata
    :rtype: bool
    """
    filecheck(p_filename)
    earlySupportCheck(p_filename)
    f_possibleKeys = appropriateKeys(p_filename, "Title")
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    for i_key in f_possibleKeys:
        if i_key in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            return True
    # print("this file has no date created data")
    return False
def getOrgDate(p_filename):
    """
    if none exists, returns datetime.datetime(1, 1, 1)
    please don't use this as a magic number. It's just to keep consistent types
    since set and get should have the same requirements to work.
    :param p_filename: name/path of the file
    :type p_filename: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: original data if it exists. Else, datetime.datetime(1,1,1)
    :rtype: datetime
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        if not containsOrgDate(p_filename):
            return datetime.datetime(1, 1, 1)
        f_key = keyHoldingValue(p_filename, "Title")
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        if f_key=='Xmp.MicrosoftPhoto.DateAcquired' or f_key=='Xmp.xmp.CreateDate':
            f_value = g_translaters[f_key](f_metadata[f_key].raw_value)
        else:
            f_value = g_translaters[f_key](f_metadata[f_key].value)
        return f_value
    else:
        earlySupportCheck(p_filename)
        # TODO add gif support
        # TODO error check: does this file have Descr data?
        return datetime.datetime(1, 1, 1)
def setOrgDate(p_filename, p_date):
    """
    takes filename and datetime object
    sets the file's metadata to be this new datetime
    Note: this function doesn't work for 'Exif.Image.DateTimeOriginal:'
    I'm having a problem similar to the problem with 'Exif.Image.Artist'

    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_date: original date metadata will be set to this
	:type p_date: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_key = 'Exif.Photo.DateTimeOriginal'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()


        """
        f_untranslatedVals = []
        for i_key in f_keys:
            if i_key=='Xmp.MicrosoftPhoto.DateAcquired' or i_key=='Xmp.xmp.CreateDate':
                f_untranslatedVals.append(p_date)
            else:
                f_untranslatedVals.append(MetadataManager.g_untranslaters[i_key](p_date))
        print("In the file ", p_filename, " the following keys will be set:\n", f_keys)
        """

        f_value = str(p_date)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        f_key = 'Exif.Photo.DateTimeDigitized'
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        # print(getOrgDate(p_filename))
        return
    else:
        earlySupportCheck(p_filename)  # TODO add gif support
    return
def searchOrgDate(p_filename, p_startDate, p_endDate):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_startDate: start of the date range we are searching for
	:type p_startDate: datetime
    :param p_endDate: end of the date range we are searching for
    :type p_endDate: datetime

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if the datetime is inbetween p_startDate and p_endDate
    :rtype: bool
    """
    filecheck(p_filename)
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.tiff':
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsOrgDate(p_filename):
            return False
        f_cleanOrgDate = getOrgDate(p_filename)
        if p_startDate <= f_cleanOrgDate <= p_endDate:
            return True
    else:
        earlySupportCheck(p_filename)
        # TODO add gif support
        return False
    return False


# ---------edit series data

# TODO def getSeries(p_filename):

# TODO def setSeries(p_filename):

# TODO def searchSeries(p_filename):

# TODO def removeSeries(p_filename):






#----------------------------------------
#--------Data given Metadata type--------
#----------------------------------------
"""
There's a lot we can figure out just given the metadata type.
We can figure out what keys we'll use, what functions to call,
etc. This is where we keep the information to do high level calls
given the type of metadata we will be operating with.
"""
# -------key selection functions

g_getFunctions = {'Title': getTitle,
                  'Description': getDescr,
                  'Rating': getRating,
                  'Tags': getTags,
                  'Artist': getArtists,
                  'Date Created': getOrgDate
                  }


# TODO make a dictionary with lists of operations
# every key is a metadata type
# and the dictionary contains lists of
# what operations are supported for that metadata type
# this will be used for the UI manager to know what buttons to display




