#!/usr/bin/env python3
import pyexiv2
import shutil
import os
from pathlib import PurePosixPath
from pathlib import PureWindowsPath
import MetadataManager
"""
This libraryhas functions that will allow us to easily
create and manage files for metadata testing
"""
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

def shadowClones(p_filename, p_howmany, p_mod=''):
    #creates several copies of a file if possible.
    ext = getExtension(p_filename)
    f_name = p_filename[:-len(ext)]
    f_newfiles = []
    for i in range(p_howmany):
        f_newfiles.append(f_name+str(i+1)+p_mod+ext)
    return f_newfiles

def jutsu(p_filename, p_files):
    for file in p_files:
        if os.path.isfile(file)==True:
            print("File already exists")
            return
    for file in p_files:
        shutil.copy(p_filename, file)

def release(p_files):
    for file in p_files:
        os.remove(file)

def missingKeys(p_file_1, p_file_2):
    #print("missing keys")
    #prints keys that are in file1, but not in file2
    f_metadata1 = pyexiv2.ImageMetadata(p_file_1)
    f_metadata1.read()
    f_metadata2 = pyexiv2.ImageMetadata(p_file_2)
    f_metadata2.read()
    missingkeys = []
    #print("exif:")
    for key1 in f_metadata1.exif_keys:
        if key1 not in f_metadata2.exif_keys:
            #print(key1)
            missingkeys.append(key1)
    #print("iptc:")
    for key1 in f_metadata1.iptc_keys:
        if key1 not in f_metadata2.iptc_keys:
            #print(key1)
            missingkeys.append(key1)
    #print("xmp:")
    for key1 in f_metadata1.xmp_keys:
        if key1 not in f_metadata2.xmp_keys:
            #print(key1)
            missingkeys.append(key1)
    return missingkeys

def allMeta(p_file_1):
    #prints all keys and associated values
    f_metadata = pyexiv2.ImageMetadata(p_file_1)
    f_metadata.read()
    print("exif:")
    for key in f_metadata.exif_keys:
        print("key:",key)
        #print(f_metadata[key])
        print(f_metadata[key].value)
    print("iptc:")
    for key in f_metadata.iptc_keys:
        print("key:",key)
        #print(f_metadata[key])
        print(f_metadata[key].value)
    print("xmp:")
    for key in f_metadata.xmp_keys:
        print("key:",key)
        #print(f_metadata[key])
        print(f_metadata[key].value)
    print()



def appropriateKeys(p_file, p_metatype):
    # for now this assumes jpg
    # TODO support for gif, tiff, and png
    # takes a filename and a metadata type (Title, Description, Tags, etc)
    # returns keys associated with that metadata type that work with that file
    f_filetype = getExtension(p_file)
    f_keydict = MetadataManager.g_keylists[f_filetype]
    f_keys = f_keydict[p_metatype]
    return f_keys

def checkAllKeysPresent(p_file, p_metatype):
    #takes a filename and a metadata type (Title, Description, Tags, etc)
    #and returns true if all keys associated with that metadata type are present in the file
    #used for testing the metadata editing functions
    f_metadata = pyexiv2.ImageMetadata(p_file)
    f_metadata.read()
    f_keys = appropriateKeys(p_file, p_metatype)
    for key in f_keys:
        if key not in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            return False
    return True

def allSame(p_list, ifempty=True):
    #this takes a list and returns true if all items are the same
    #returns false if any item is different
    #if empty, returns bool specified by caller. default is true
    #intended use: checking if all values for a metadata type are the same
    if len(p_list)==0:
        return ifempty
    f_item = p_list[0]
    for i_item in p_list[1:]:
        if f_item!=i_item:
            return False
    return True

def selectVals (p_file, p_keys):
    #assumes all these keys exist in the file.
    #takes filename and list of keys
    #returns list of key value pairs
    f_metadata = pyexiv2.ImageMetadata(p_file)
    f_metadata.read()
    pairs = []
    for key in p_keys:
        pairs.append((key,f_metadata[key].value))
    return pairs

print(appropriateKeys("/media/sf_tagger/windowstesting/skullA.jpg", "Artist"))
print(checkAllKeysPresent("/media/sf_tagger/windowstesting/skullA.jpg", "Artist"))

g_titleVals = selectVals("/media/sf_tagger/windowstesting/skullA.jpg", appropriateKeys("/media/sf_tagger/windowstesting/skullA.jpg", "Artist"))
for i_pair in g_titleVals:
    print(i_pair)


def valTranslateFromDictDef(p_dict):
    #this is one of the translation functions
    #these single parameter functions are used to automatically parse metadata values
    #these functions are called by another function that determines which translation is needed
    #input: dictionary
    #output: string
    #we assume 'x-default' is in the dictionary
    return p_dict['x-default']
def valTranslateToDictDef(p_val):
    f_dict = {'x-default': p_val}
    return f_dict

def valTranslateFromRawS(p_raw):
    #this is one of the translation functions
    #these single parameter functions are used to automatically parse metadata values
    #these functions are called by another function that determines which translation is needed
    #input: string of numbers
    #output: string
    return MetadataManager.raw_to_cleanStr(p_raw)
def valTranslateToRawS(p_val):
    return MetadataManager.cleanStr_to_raw(p_val)

def valTranslateFromRawL(p_raw):
    #this is one of the translation functions
    #these single parameter functions are used to automatically parse metadata values
    #these functions are called by another function that determines which translation is needed
    #input: string of numbers
    #output: list
    return MetadataManager.raw_to_cleanList(p_raw)
def valTranslateToRawL(p_val):
    return MetadataManager.cleanList_to_raw(p_val)

def valTranslateNone(p_val):
    #this is one of the translation functions
    #these single parameter functions are used to automatically parse metadata values
    #these functions are called by another function that determines which translation is needed
    #input: value of unknown type
    #output: the parameter passed in with no change and no side effects
    return p_val

g_translaters = {'Exif.Image.XPTitle': valTranslateFromRawS,
                 'Exif.Image.XPSubject': valTranslateFromRawS,
                 'Exif.Image.XPComment': valTranslateFromRawS,
                 'Exif.Image.XPKeywords': valTranslateFromRawL,
                 'Exif.Image.XPAuthor': valTranslateFromRawL,
                 'Xmp.dc.title': valTranslateFromDictDef,
                 'Xmp.dc.description': valTranslateFromDictDef,
                 'Xmp.dc.subject': valTranslateNone,
                 'Xmp.MicrosoftPhoto.LastKeywordXMP': valTranslateNone,
                 'Exif.Image.Artist': MetadataManager.cleanStr2cleanList,
                 'Xmp.dc.creator': valTranslateNone,
                 'Exif.Image.Rating': valTranslateNone,
                 'Xmp.xmp.Rating': valTranslateNone,
                 'Exif.Image.RatingPercent': MetadataManager.percent2rating,
                 'Xmp.MicrosoftPhoto.Rating': MetadataManager.percentStr2rating,
                 'Exif.Photo.DateTimeOriginal': valTranslateNone,
                 'Exif.Photo.DateTimeDigitized': valTranslateNone
                 }
g_untranslaters = {'Exif.Image.XPTitle': valTranslateToRawS,
                 'Exif.Image.XPSubject': valTranslateToRawS,
                 'Exif.Image.XPComment': valTranslateToRawS,
                 'Exif.Image.XPKeywords': valTranslateToRawL,
                 'Exif.Image.XPAuthor': valTranslateToRawL,
                 'Xmp.dc.title': valTranslateToDictDef,
                 'Xmp.dc.description': valTranslateToDictDef,
                 'Xmp.dc.subject': valTranslateNone,
                 'Xmp.MicrosoftPhoto.LastKeywordXMP': valTranslateNone,
                 'Exif.Image.Artist': MetadataManager.cleanList2cleanStr,
                 'Xmp.dc.creator': valTranslateNone,
                 'Exif.Image.Rating': valTranslateNone,
                 'Xmp.xmp.Rating': valTranslateNone,
                 'Exif.Image.RatingPercent': MetadataManager.rating2percent,
                 'Xmp.MicrosoftPhoto.Rating': MetadataManager.rating2percentStr,
                 'Exif.Photo.DateTimeOriginal': valTranslateNone,
                 'Exif.Photo.DateTimeDigitized': valTranslateNone
                 }

g_translatedVals = []
for i in range(len(g_titleVals)):
    g_translatedVals.append(g_translaters[g_titleVals[i][0]](g_titleVals[i][1]))

g_untranslatedVals = []
for i in range(len(g_titleVals)):
    g_untranslatedVals.append(g_untranslaters[g_titleVals[i][0]](g_translatedVals[i]))

print()
print(g_translatedVals)
print(allSame(g_translatedVals))

for i in range(len(g_titleVals)):
    print((g_titleVals[i][0] ,g_untranslatedVals[i]))
"""
g_mainfile = "/media/sf_tagger/windowstesting/skull.jpg"
g_files = shadowClones(g_mainfile, 5)
jutsu(g_mainfile,g_files)
print(g_files)
print(allMeta(g_mainfile))
for file in g_files:
    print()
    print(file)
    #print(missingKeys("/media/sf_tagger/windowstesting/skull.jpg",file))
    print(allMeta(file))
"""
#MetadataManager.setRating(g_files[2], 4)
"""
for file in g_files:
    print()
    print(file)
    #print(missingKeys("/media/sf_tagger/windowstesting/skull.jpg",file))
    print(allMeta(file))
"""
#release(g_files)

g_title = "Sample Title"
g_rating = 2
g_description = "a silly propaganda picture"
g_tags = ['skeleton', 'mood']
g_artist = ['George Washington', 'model: Skeletore']
g_modfile = "/media/sf_tagger/windowstesting/skullA.jpg"