#!/usr/bin/env python3
import pyexiv2
import shutil
import os
from pathlib import PurePosixPath
from pathlib import PureWindowsPath

import MetadataManager

"""
This library has functions that will allow us to easily
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
            raise ValueError(
                'File \'{}\' already exists'.format(file))
    for file in p_files:
        shutil.copy2(p_filename, file)

def release(p_files):
    for file in p_files:
        os.remove(file)


def singleClone(p_filename):
    #creates a single copy of a file and returns the name of the copy
    #creates several copies of a file if possible.
    ext = getExtension(p_filename)
    f_name = p_filename[:-len(ext)]
    f_newfile = f_name+"Copy"+ext
    if os.path.isfile(f_newfile)==True:
        #raise ValueError('File \'{}\' already exists'.format(f_newfile))
        os.remove(f_newfile)
    shutil.copy2(p_filename, f_newfile)
    return f_newfile

def singleRelease(p_filename):
    #used with singleClone(). Removes the copy that function created
    os.remove(p_filename)

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

def MetaDataVals(p_file, p_metatype):
    #given a file and a metadata type
    #reads the values of the appropriate keys
    #returns a list of the key/value pairs
    f_metadata = pyexiv2.ImageMetadata(p_file)
    f_metadata.read()
    f_keys = MetadataManager.appropriateKeys(p_file, p_metatype)
    pairs = []
    for key in f_keys:
        if key not in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            continue
        if key=='Xmp.MicrosoftPhoto.DateAcquired' or key=='Xmp.xmp.CreateDate':
            pairs.append((key, f_metadata[key].raw_value))
        else:
            pairs.append((key,f_metadata[key].value))
    return pairs

#TODO make unit tests that use this function.
#this should be true after a successful set operation is performed
def checkAllKeysPresent(p_file, p_metatype):
    #takes a filename and a metadata type (Title, Description, Tags, etc)
    #and returns true if all keys associated with that metadata type are present in the file
    #used for testing the metadata editing functions
    f_metadata = pyexiv2.ImageMetadata(p_file)
    f_metadata.read()
    f_keys = MetadataManager.appropriateKeys(p_file, p_metatype)
    for key in f_keys:
        if key not in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            return False
    return True

#TODO make unit tests that use this function.
#this should be false after a successful wipe operation is performed
def checkAnyKeysPresent(p_file, p_metatype):
    #takes a filename and a metadata type (Title, Description, Tags, etc)
    #and returns true if any keys associated with that metadata type are present in the file
    #used for testing the metadata editing functions
    f_metadata = pyexiv2.ImageMetadata(p_file)
    f_metadata.read()
    f_keys = MetadataManager.appropriateKeys(p_file, p_metatype)
    f_present = []
    for key in f_keys:
        if key in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            f_present.append(key)
    print("In", p_file, "the following", p_metatype, "keys still exist:", f_present)
    if len(f_present)==0:
        return False
    return True

#TODO make unit tests that use this function.
#this should be true after a successful set operation is performed
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


#given a file with a type of metadata
#take that value. create a new file (of the same filetype)
#give that new file the same kind of metadata
#check the associated key/value pairs of each value
#they must be identical
#we need: filewithvalue, filetocopy, newfilename, metadatatype

g_getFunctions = {'Title': MetadataManager.getTitle,
                  'Description': MetadataManager.getDescr,
                  'Rating': MetadataManager.getRating,
                  'Tags': MetadataManager.getTags,
                  'Artist': MetadataManager.getArtists,
                  'Date Created': MetadataManager.getOrgDate
                  }

def testMetadataSet(p_filewithvalue, p_filetocopy, p_metatype):
    #this takes a file with a value, another file of the same type, and a metadata type
    #finds the value of the first file.
    #then it adds appropriately transformed versions of that value to all
    #the appropriate keys of a copy of the second file
    #then it compares all the appropriate key/value pairs
    #a list of all the differing values is made
    #if a key/value pair is so different that the clean versions are different, we return false (and the list)
    #else we return true (and the list)
    if getExtension(p_filewithvalue)!=getExtension(p_filetocopy):
        raise ValueError(
            'file extensions must be the same')
    f_newfilel = shadowClones(p_filetocopy, 1) #creates names for files
    jutsu(p_filetocopy, f_newfilel) #this actually makes the new files
    f_newfile = f_newfilel[0]
    f_valueToSet = MetadataManager.g_getFunctions[p_metatype](p_filewithvalue)
    f_keys = MetadataManager.appropriateKeys(f_newfile, p_metatype)
    #read metadata value of p_filewithvalue

    f_untranslatedVals = []
    for i_key in f_keys:
        if i_key=='Xmp.MicrosoftPhoto.DateAcquired' or i_key=='Xmp.xmp.CreateDate':
            f_untranslatedVals.append(f_valueToSet)
        else:
            f_untranslatedVals.append(MetadataManager.g_untranslaters[i_key](f_valueToSet))
    print("In the file ", f_newfile, " the following keys will be set:\n", f_keys)
    print("the value to be set is ", f_valueToSet)
    print("it will be formatted in the following ways:\n", f_untranslatedVals)

    f_metadata = pyexiv2.ImageMetadata(f_newfile)
    f_metadata.read()
    #this actually sets the appropriately formatted values to the appropriate keys in the file
    for i in range(len(f_keys)):
        i_key = f_keys[i]
        i_value = f_untranslatedVals[i]
        #print(i_key)
        i_prefix = i_key[:i_key.find('.')]
        #print(i_prefix)
        if i_prefix=='Exif':
            f_metadata[i_key] = pyexiv2.ExifTag(i_key, i_value)
        elif i_prefix=='Xmp':
            f_metadata[i_key] = pyexiv2.XmpTag(i_key, i_value)
        elif i_prefix=='Iptc':
            f_metadata[i_key] = pyexiv2.IptcTag(i_key, i_value)
        else: raise ValueError('the key:  \'{}\' is invalid'.format(i_key))
        f_metadata.write()
    print()
    f_oldfileVals = MetaDataVals(p_filewithvalue, p_metatype)
    print("these are the key/value pairs from the original file ", p_filewithvalue)
    for i_pair in f_oldfileVals:
        print(i_pair)
    f_newfileVals = MetaDataVals(f_newfile, p_metatype)
    print("these are the key/value pairs from the new file ", f_newfile)
    for i_pair in f_newfileVals:
        print(i_pair)
    f_same = True
    f_diff = []
    #comparing the metadata values of both files
    for i in range(len(f_oldfileVals)):
        i_a = f_oldfileVals[i]
        i_b = f_newfileVals[i]
        if i_a!=i_b: #if the untranslated values don't exactly match, check if the translated ones do
            i_c = MetadataManager.g_translaters[i_a[0]](i_a[1])
            i_d = MetadataManager.g_translaters[i_b[0]](i_b[1])
            if i_c!=i_d:
                f_same=False
            f_diff.append((i_a,i_b)) #either way, slight differences are recorded and will be returned
    release(f_newfilel)
    return (f_same,f_diff)

g_title = "Sample Title"
g_rating = 2
g_description = "a silly propaganda picture"
g_tags = ['skeleton', 'mood']
g_artist = ['George Washington', 'model: Skeletore']
"""
g_fulljpg = "/media/sf_tagger/windowstesting/skullA.jpg"
g_newfile = singleClone(g_fulljpg)

#remove tag.
#remove artist
#wipe everything
#delete individual key

checkAnyKeysPresent(g_newfile, "Title")
g_metadata = pyexiv2.ImageMetadata(g_newfile)
g_metadata.read()
g_metadata.__delitem__('Xmp.dc.title')
g_metadata.write()
checkAnyKeysPresent(g_newfile, "Title")

singleRelease(g_newfile)
"""