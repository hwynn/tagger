#!/usr/bin/env python3
import pyexiv2
import os
from pathlib import PurePosixPath
from pathlib import PureWindowsPath

#-------These are the exceptions that can be thrown
#reasons we might throw an error:
# 1. File not found
# this should already exist as FileNotFoundError

# 2. Unrecognized filetype (or no filetype)
class UnknownFiletypeError(ValueError): pass

# 3. Unsupported filetype
class UnsupportedFiletypeError(ValueError): pass

# 4. Support not yet implemented
# This exception will occur in cases of acceptable use
# but the functionality is not yet complete.
class SupportNotImplementedError(NotImplementedError): pass

# 5. File does not have this data.
# Used when we want to remove metadata but none is present.
class MetadataMissingError(ValueError): pass

class NoSuchItemError(ValueError):
    """This is similar to MetadataMissing (it shows up in similar contexts)
    But it's raised when data is present, but the item we want to remove
    isn't present in the list"""
    pass

class DuplicateDataError(ValueError):
    """we raise this when we try to add a tag
    or something similar to a list and the list already has that item"""
    pass

#both of these are used for setRating
class OutOfRangeError(ValueError): pass
class NotIntegerError(ValueError): pass

def getExtension(p_filepathname):
    #this lets us extract file extensions
    #regardless of operating system
    if os.name == 'nt':
        #this filepath is from windows
        return PureWindowsPath(p_filepathname).suffix
    #assume posix otherwise
    return PurePosixPath(p_filepathname).suffix

def filecheck(p_filename):
    #this function checks the type of the file, and raises an exception
    #if the filetype is not recognized
    if len(p_filename) < 5:
        raise UnknownFiletypeError('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if getExtension(p_filename) != '.jpg' and getExtension(p_filename) != '.png' and getExtension(p_filename) != '.gif':
        raise UnsupportedFiletypeError(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png, gif'.format(p_filename))
    return

def earlySupportCheck(p_filename):
    # this function checks the type of the file.
    # it will raise an exception if this type of file should be supported
    # but that support has not yet been implemented
    # Used for png and gif
    if getExtension(p_filename) == '.png' or getExtension(p_filename) == '.gif':
        raise SupportNotImplementedError('Sorry. This operation not ready to support .png or .gif files yet.')
    return

def alpha1SupportCheck(p_filename):
    # this function checks the type of the file.
    # it will raise an exception if this type of file should be supported
    # but that support has not yet been implemented
    # Used for png and gif
    if getExtension(p_filename) == '.jpg' or getExtension(p_filename) == '.png' or getExtension(p_filename) == '.gif':
        raise SupportNotImplementedError('Sorry. This operation is not ready for anything.')
    return

#-------string cleaning utility functions
def listHexTrim(p_rawList):
    # Takes a freshly translated string list and
    # trims the '\x00' ends off all the strings
    #print("listHexTrim(", p_rawList, ")")
    return [x.replace('\x00', '') for x in p_rawList]
def dirtyStr2cleanStr(p_bustedTags):
    f_tags = ""
    for y in [x.replace('\x00', '') for x in p_bustedTags]:
        if y != '':
            f_tags += y
    return f_tags
def cleanStr2dirtyStr(p_newtag):
    f_bustedTag = ""
    for x in p_newtag:
        f_bustedTag += x
        f_bustedTag += '\x00'
    return f_bustedTag
def dirtyStr2cleanList(p_dirtyTagStr):
    # Takes a semicolon-delimited list of tags
    # represented by a dirty (\x00 filled) string.
    # This function returns a list of tags
    # represented by clean strings
    f_dirtyTagList = p_dirtyTagStr.split(';')
    # print("dirtyStr2cleanList(): f_dirtyTagList", f_dirtyTagList)
    f_cleanTagList = [dirtyStr2cleanStr(x) for x in f_dirtyTagList]
    # print("dirtyStr2cleanList(): f_cleanTagList", f_cleanTagList)
    return f_cleanTagList
def cleanList2dirtyStr(p_cleanTagList):
    # Takes a list of tags
    # represented by clean strings.
    # This function returns a semicolon-delimited list of tags
    # represented by a dirty (\x00 filled) string.
    f_dirtyTagList = [cleanStr2dirtyStr(x) for x in p_cleanTagList]
    # print("cleanList2dirtyStr(): f_dirtyTagList", f_dirtyTagList)
    f_dirtyTagString = ";\x00".join(f_dirtyTagList) + "\x00\x00"
    # print("cleanList2dirtyStr(): f_dirtyTagString", f_dirtyTagString)
    return f_dirtyTagString
def cleanList2cleanStr(p_cleanTagList):
    return ";".join(p_cleanTagList)
#-------stashing utility functions
"""Note: 'stashing' is a term I made up
which refers to storing several types of 
metadata into a single large string.
This should let us store a variety of
metadata in file types that only have 
a few metadata tags"""
def containsStash(p_filename):
    # checks if we have added a stash string
    # at all. Returns bool
    # TODO
    return
def getStashIndex(p_filename):
    # assuming containsStash() is true
    # returns a list of the metadata
    # similar to: metadata.exif_keys
    # TODO
    return
def searchStashIndex(p_filename, p_key):
    # assuming containsStash() is true
    # this function checks whether or not
    # a type of metadata is present in
    # the stash index and the stash string
    #returns bool
    return
def addItemToStashIndex(p_filename, p_key):
    # assuming searchStashIndex() returns false
    # this function adds a new kind of metadata
    # to the stash string. Only certain values of p_key
    # are allowed to keep metadata consistent across filetypes
    # this also adds a blank metadata entry to the stash string
    # TODO
    return
def removeItemFromStashIndex(p_filename, p_key):
    # assuming searchStashIndex() returns true
    # this function removes a type of metadata
    # from the stash string and the stash index
    # TODO
    return
def setStashData(p_filename, p_key, p_value):
    # assuming searchStashIndex() returns true
    # this function stores data of a given type
    # into the appropriate place in the stash string
    # note: this will completely rewrite a type of stash data
    # there is no addStashData function. That must be done
    # by the individual metadata functions
    # TODO
    return
def getStashData(p_filename, p_key):
    # assuming searchStashIndex() returns true
    # this function returns the value of the given
    # metadata type as a string.
    # the individual metadata functions
    # are responsible for parsing this string
    # TODO
    return


# ------edit title metadata
def containsTitle(p_filename):
    # This will tell us if the file
    # has any title metadata.
    # Returns bool
    filecheck(p_filename)
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    earlySupportCheck(p_filename)
    if ((getExtension(p_filename) == '.jpg') and ('Exif.Image.XPTitle' in f_metadata.exif_keys)):
        # print("this file already has title data")
        return True
    # print("this file has no title data")
    return False
def getTitle(p_filename):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsTitle(p_filename):
            return ""
        f_keywords = f_metadata['Exif.Image.XPTitle']
        f_dirtyTitleString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        #print("dirty Title:", f_dirtyTitleString)
        f_cleanTitle = dirtyStr2cleanStr(f_dirtyTitleString)
        #print("clean Title:", f_cleanTitle)
        return f_cleanTitle
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        # TODO error check: does this file have Title data?
        return ""
    return ""
def setTitle(p_filename, p_setTitleToThis):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_key = 'Exif.Image.XPTitle'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_dirtyString = cleanStr2dirtyStr(p_setTitleToThis)
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyString)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        return
    return
def searchTitle(p_filename, p_searchForThis):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsTitle(p_filename):
            return False
        f_keywords = f_metadata['Exif.Image.XPTitle']
        f_dirtyTitleString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        f_cleanTitle = dirtyStr2cleanStr(f_dirtyTitleString)
        #Note: Title does not need to be entire search term to return true
        if p_searchForThis in f_cleanTitle:
            return True
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        # TODO error check: does this file have Title data?
        return False
    return False
def wipeTitle(p_filename):
    # considering renaming the function wipeTitle(p_filename)
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_key = 'Exif.Image.XPTitle'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        if not containsTitle(p_filename):
            raise MetadataMissingError("there is no description to remove")
        f_dirtyString = cleanStr2dirtyStr(" ")
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyString)
        # we set the value to (almost) nothing before removing the key just in case the values stick around
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        f_metadata.__delitem__(f_key)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        return
    return
# ------edit artist metadata
def containsArtists(p_filename):
	# This will tell us if the file
	# has any artist metadata.
	# Returns bool
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        if ('Exif.Image.XPAuthor' in f_metadata.exif_keys):
            # print("this file already has artist data")
            return True
        # print("this file has no artist data")
        return False
    else:
        # TODO add png and gif support
        return False
    return False
def getArtists(p_filename):
    # returns list of artists
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsArtists(p_filename):
            return []
        f_keywords = f_metadata['Exif.Image.XPAuthor']
        f_dirtyArtistString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        # print("getArtists() f_dirtyArtistString\t\t", f_dirtyArtistString)
        f_cleanArtistList = dirtyStr2cleanList(f_dirtyArtistString)
        # print("getArtists() f_cleanArtistList\t\t", f_cleanArtistList)
        return f_cleanArtistList
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        # TODO error check: does this file have artist data?
        return []
    return []
def setArtists(p_filename, p_cleanArtistList):
    # Instead of appending a new artist to the list of artists already present
    # This function replaces all artists with the list of artists provided as p_cleanArtistList.
    # Use this function with caution. Because.. you know. It wipes your artists.
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_key = 'Exif.Image.XPAuthor'
        # print(f_metadata.exif_keys)
        f_dirtyArtistString = cleanList2dirtyStr(p_cleanArtistList)
        # print("setArtists() f_dirtyArtistString\t\t", f_dirtyArtistString)
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyArtistString)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        #f_metadata['Exif.Image.Artist'] = pyexiv2.ExifTag('Exif.Image.Artist', cleanList2cleanStr(p_cleanArtistList))
        f_metadata.read()
        f_artistDataToSet = f_metadata['Exif.Image.Artist']
        f_artistString = cleanList2cleanStr(p_cleanArtistList)
        print("new artists should be:", f_artistString)
        #f_artistDataToSet.value = f_artistString
        f_artistDataToSet.value = "hwllo testing akjhjwe"
        #f_metadata['Exif.Image.Artist'].value = cleanList2cleanStr(p_cleanArtistList)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        return
def searchArtists(p_filename, p_artist):
    filecheck(p_filename)

    if (getExtension(p_filename) == '.jpg'):
        f_metaData = pyexiv2.ImageMetadata(p_filename)
        f_metaData.read()
        if not containsArtists(p_filename):
            return False
        f_keywords = f_metaData['Exif.Image.XPAuthor']
        f_bustedArtistString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        # Note: the conditions for finding an artist are very relaxed.
        # We're only searching for a substring.
        # so if an artist entry is "composer: Sarah Sharp"
        # searches for: "composer", "Sarah Sharp", "Sarah", "sharp", and "Sar"
        # will all return true.
        # Perhaps a strictSearchArtists() function is needed
        f_found = False
        for i_artist in dirtyStr2cleanList(f_bustedArtistString):
            if p_artist.lower in i_artist.lower:
                f_found = True
                break
        return f_found
    else:
        # TODO add png and gif support
        # TODO error check: does this file have artist data?
        return False
    return False
def addArtist(p_filename, p_artist):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        f_key = 'Exif.Image.XPAuthor'
        if not containsArtists(p_filename):
            f_cleanArtistList = [p_artist]
            f_dirtyArtistString2 = cleanList2dirtyStr(f_cleanArtistList)
            f_value = pyexiv2.utils.string_to_undefined(f_dirtyArtistString2)
            f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
            f_metadata.write()
            f_metadata['Exif.Image.Artist'] = pyexiv2.ExifTag('Exif.Image.Artist', cleanList2cleanStr(f_cleanArtistList))
            f_metadata.write()
            return
        f_keywords = f_metadata['Exif.Image.XPAuthor']
        f_dirtyArtistString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        #print("addArtist() f_dirtyArtistString\t\t", f_dirtyArtistString)
        f_cleanArtistList = dirtyStr2cleanList(f_dirtyArtistString)
        #print("addArtist() f_cleanArtistList\t\t", f_cleanArtistList)
        if p_artist in f_cleanArtistList:
            raise DuplicateDataError("file already contains this artist")
        f_cleanArtistList.insert(0, p_artist)
        f_dirtyArtistString2 = cleanList2dirtyStr(f_cleanArtistList)
        #print("addArtist() f_dirtyArtistString2\t\t", f_dirtyArtistString2)
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyArtistString2)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        f_metadata['Exif.Image.Artist'] = pyexiv2.ExifTag('Exif.Image.Artist', cleanList2cleanStr(f_cleanArtistList))
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        # TODO error check: does this file have artist data?
        return
    return
def removeArtist(p_filename, p_artist):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsArtists(p_filename):
            raise MetadataMissingError(
                'The file \'{}\' does not contain any artist data \n This operation cannot be performed'.format(
                    p_filename))
        f_keywords = f_metadata['Exif.Image.XPAuthor']
        f_key = 'Exif.Image.XPAuthor'
        f_dirtyArtistString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        #print("removeArtist() f_dirtyArtistString\t\t", f_dirtyArtistString)
        f_cleanArtistList = dirtyStr2cleanList(f_dirtyArtistString)
        #print("removeArtist() f_cleanArtistList\t\t", f_cleanArtistList)
        #Note that p_artist must be an exact match with an entry to have it removed
        if p_artist not in f_cleanArtistList:
            raise NoSuchItemError(
                'The file \'{}\' does not contain the artist \'{}\' \n This operation cannot be performed'.format(
                    p_filename, p_artist))
        f_cleanArtistList.remove(p_artist)
        f_dirtyArtistString2 = cleanList2dirtyStr(f_cleanArtistList)
        #print("removeArtist() f_dirtyArtistString2\t\t", f_dirtyArtistString2)
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyArtistString2)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        print("artist string should be:", cleanList2cleanStr(f_cleanArtistList))
        #f_metadata['Exif.Image.Artist'] = pyexiv2.ExifTag('Exif.Image.Artist', cleanList2cleanStr(f_cleanArtistList))
        f_metadata['Exif.Image.Artist'].value = cleanList2cleanStr(f_cleanArtistList)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        # TODO error check: does this file have artist data?
        return
    return

# -----edit tag metadata
def containsTags(p_filename):
	# This will tell us if the file
	# has any tag metadata.
	# Returns bool
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        if ('Exif.Image.XPKeywords' in f_metadata.exif_keys):
            # print("this file already has tag data")
            return True
        # print("this file has no tag data")
        return False
    else:
        # TODO add png and gif support
        return False
    return False
def getTags(p_filename):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsTags(p_filename):
            return []
        f_keywords = f_metadata['Exif.Image.XPKeywords']
        f_dirtyTagString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        # print("getTags() f_dirtyTagString\t\t", f_dirtyTagString)
        f_cleanTagList = dirtyStr2cleanList(f_dirtyTagString)
        # print("getTags() f_cleanTagList\t\t", f_cleanTagList)
        return f_cleanTagList
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        # TODO error check: does this file have tag data?
        return []
    return []
def setTags(p_filename, p_cleanTagList):
    # Instead of appending a new tag to the list of tags already present
    # This function replaces all tags with the list of tags provided as p_cleanTagList.
    # Use this function with caution. Because.. you know. It wipes your tags.
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_key = 'Exif.Image.XPKeywords'
        # print(f_metadata.exif_keys)
        f_dirtyTagString = cleanList2dirtyStr(p_cleanTagList)
        # print("setTags() f_dirtyTagString\t\t", f_dirtyTagString)
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyTagString)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return True
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        return True
def searchTags(p_filename, p_tag):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metaData = pyexiv2.ImageMetadata(p_filename)
        f_metaData.read()
        if not containsTags(p_filename):
            return False
        f_keywords = f_metaData['Exif.Image.XPKeywords']
        f_bustedTagString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        # Note: these are strict searches. They are case sensative
        # non case sensative searches may require longer execution time
        if p_tag in dirtyStr2cleanList(f_bustedTagString):
            return True
    else:
        # TODO add png and gif support
        # TODO error check: does this file have tag data?
        return False
    return False
def addTag(p_filename, p_tag):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        f_key = 'Exif.Image.XPKeywords'
        if not containsTags(p_filename):
            f_cleanTagList = [p_tag]
            f_dirtyTagString2 = cleanList2dirtyStr(f_cleanTagList)
            f_value = pyexiv2.utils.string_to_undefined(f_dirtyTagString2)
            f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
            f_metadata.write()
            return
        f_keywords = f_metadata['Exif.Image.XPKeywords']
        f_dirtyTagString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        #print("addTag() f_dirtyTagString\t\t", f_dirtyTagString)
        f_cleanTagList = dirtyStr2cleanList(f_dirtyTagString)
        #print("addTag() f_cleanTagList\t\t", f_cleanTagList)
        if p_tag in f_cleanTagList:
            raise DuplicateDataError("file already contains this tag")
        f_cleanTagList.insert(0, p_tag)
        f_dirtyTagString2 = cleanList2dirtyStr(f_cleanTagList)
        #print("addTag() f_dirtyTagString2\t\t", f_dirtyTagString2)
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyTagString2)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        # TODO error check: does this file have tag data?
        return
    return
def removeTag(p_filename, p_tag):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsTags(p_filename):
            raise MetadataMissingError(
                'The file \'{}\' does not contain any tag data \n This operation cannot be performed'.format(
                    p_filename))
        f_keywords = f_metadata['Exif.Image.XPKeywords']
        f_key = 'Exif.Image.XPKeywords'
        f_dirtyTagString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        #print("removeTag() f_dirtyTagString\t\t", f_dirtyTagString)
        f_cleanTagList = dirtyStr2cleanList(f_dirtyTagString)
        #print("removeTag() f_cleanTagList\t\t", f_cleanTagList)
        if p_tag not in f_cleanTagList:
            raise NoSuchItemError(
                'The file \'{}\' does not contain the tag \'{}\' \n This operation cannot be performed'.format(
                    p_filename, p_tag))
        f_cleanTagList.remove(p_tag)
        f_dirtyTagString2 = cleanList2dirtyStr(f_cleanTagList)
        #print("removeTag() f_dirtyTagString2\t\t", f_dirtyTagString2)
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyTagString2)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        # TODO error check: does this file have tag data?
        return
    return
# -------edit description metadata
def containsDescr(p_filename):
	# This will tell us if the file
	# has any description metadata.
	# Returns bool
    filecheck(p_filename)
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    if ((getExtension(p_filename) == '.jpg') and ('Exif.Image.XPComment' in f_metadata.exif_keys)):
        # print("this file already has description data")
        return True
    # print("this file has no description data")
    return False
def getDescr(p_filename):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsDescr(p_filename):
            return ""
        f_keywords = f_metadata['Exif.Image.XPComment']
        f_dirtyDescrString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        #print("dirty Descr:", f_dirtyDescrString)
        f_cleanDescr = dirtyStr2cleanStr(f_dirtyDescrString)
        #print("clean Descr:", f_cleanDescr)
        return f_cleanDescr
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        # TODO error check: does this file have Descr data?
        return ""
    return ""


    return
def setDescr(p_filename, p_setDescrToThis):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_key = 'Exif.Image.XPComment'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_dirtyString = cleanStr2dirtyStr(p_setDescrToThis)
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyString)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        return
    return
def searchDescr(p_filename, p_searchForThis):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsDescr(p_filename):
            return False
        f_keywords = f_metadata['Exif.Image.XPComment']
        f_dirtyDescrString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        f_cleanDescr = dirtyStr2cleanStr(f_dirtyDescrString)
        if p_searchForThis in f_cleanDescr:
            return True
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        # TODO error check: does this file have Descr data?
        return False
    return False
def addDescr(p_filename, p_addThisToDescr):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_key = 'Exif.Image.XPComment'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        f_cleanDescr = ""
        if containsDescr(p_filename):
            f_keywords = f_metadata['Exif.Image.XPComment']
            f_dirtyDescrString = pyexiv2.utils.undefined_to_string(f_keywords.value)
            f_cleanDescr = dirtyStr2cleanStr(f_dirtyDescrString)
        f_setDescrToThis = f_cleanDescr + p_addThisToDescr
        f_dirtyString = cleanStr2dirtyStr(f_setDescrToThis)
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyString)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        return
    return
def wipeDescr(p_filename):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_key = 'Exif.Image.XPComment'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        if not containsDescr(p_filename):
            raise MetadataMissingError("there is no description to remove")
        f_dirtyString = cleanStr2dirtyStr(" ")
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyString)
        # we set the value to (almost) nothing before removing the key just in case the values stick around
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        f_metadata.__delitem__(f_key)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        return
    return
# ------edit rating metadata
def containsRating(p_filename):
	# This will tell us if the file
	# has any rating metadata.
	# Returns bool
    filecheck(p_filename)
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    if ((getExtension(p_filename) == '.jpg') and ('Exif.Image.Rating' in f_metadata.exif_keys)):
        # print("this file already has rating data")
        return True
    # print("this file has no rating data")
    return False
def getRating(p_filename):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsRating(p_filename):
            return -1
        f_keywords = f_metadata['Exif.Image.Rating']
        #print("getRating() Rating\t\t", f_keywords.value)
        f_rating = f_keywords.value
        return f_rating
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        # TODO error check: does this file have rating data?
        return -1
    return -1
def setRating(p_filename, p_setRatingToThis):
    if not (1 < p_setRatingToThis < 5):
        raise OutOfRangeError('number out of range (must be 1..5)')
    if not isinstance(p_setRatingToThis, int):
        raise NotIntegerError('non-integers can not be used')
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
        f_key = 'Exif.Image.Rating'
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()

        f_value = p_setRatingToThis
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return
    else:
        earlySupportCheck(p_filename)
        # TODO add png and gif support
        return
    return
def searchRating(p_filename, p_searchForThisRating):
    filecheck(p_filename)
    if (getExtension(p_filename) == '.jpg'):
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
        # TODO add png and gif support
        # TODO error check: does this file have rating data?
        return False
    return False
#TODO def wipeRating(p_filename):
# ------edit metadata that can store source url
def containsSrc(p_filename):
	# This will tell us if the file
	# has any source url metadata.
	# Returns bool
    filecheck(p_filename)
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    if ((getExtension(p_filename) == '.jpg') and ('Exif.Image.ImageHistory' in f_metadata.exif_keys)):
        # print("this file already has history/source data")
        return True
    # print("this file has no history/source data")
    return False
def getSrc(p_filename):
    filecheck(p_filename)
    alpha1SupportCheck(p_filename)
    # TODO
    return
def addSrc(p_filename, x):
    filecheck(p_filename)
    alpha1SupportCheck(p_filename)
    # TODO
    return
def searchSrc(p_filename, x):
    filecheck(p_filename)
    alpha1SupportCheck(p_filename)
    # TODO
    return
# -------edit orginal date
def containsOrgDate(p_filename):
	# This will tell us if the file
	# has any original date metadata.
	# Returns bool
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    if ((getExtension(p_filename) == '.jpg') and ('Exif.Image.DateTimeOriginal' in f_metadata.exif_keys)):
        # print("this file already has original date data")
        return True
    # print("this file has no original date data")
    return False
def getOrgDate(p_filename):
    filecheck(p_filename)
    alpha1SupportCheck(p_filename)
    # TODO
    return
def setOrgDate(p_filename, x):
    filecheck(p_filename)
    alpha1SupportCheck(p_filename)
    # TODO
    return
def searchOrgDate(p_filename, x):
    filecheck(p_filename)
    alpha1SupportCheck(p_filename)
    # TODO
    return
