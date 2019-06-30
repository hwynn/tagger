#!/usr/bin/env python3
import os
import wget
import requests
import MetadataManagerL0
import MetadataManagerL1
import pyexiv2
import copy
import shutil
from TestStructures import TestFile, TestData
from TData import g_outpath, g_fileList, g_files

# several functions below found from: https://stackoverflow.com/a/39225272
def download_file_from_google_drive(id, destination):
    """downloads files from google drive.
    Found from https://stackoverflow.com/a/39225272"""
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)
    session.close()

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None
def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
def getGoogleDrivePicture(p_picID, p_outpath):
    """if __name__ == "__main__":
        file_id = 'TAKE ID FROM SHAREABLE LINK'
        destination = 'DESTINATION FILE ON YOUR DISK'
        download_file_from_google_drive(file_id, destination)"""
    f_downloadURL = 'https://drive.google.com/uc?authuser=0&id=' + p_picID + '&export=download'
    f_filename = wget.download(f_downloadURL, p_outpath)
    download_file_from_google_drive(p_picID, f_filename)
    #print("getGoogleDrivePicture() filename: ", f_filename)
    return f_filename
# I made everything from this point on
"""
Author: Harrison Wynn
Created: 2018
"""
# ===========================================================================
# ---------------------------Test File Functions-----------------------------
# ===========================================================================
"""
These are functions that will allow us to easily
create and manage files for metadata testing
"""
def downloadGooglePicture(p_file, p_path=g_outpath):
    """
    Downloads a picture from google drive for testing purposes
    :param p_file: information about the test file, including filename and googleID
    :type p_file: TestFile class instance
    :param p_path: path the files will be saved to (default: g_outpath imported from TData)
    :type p_path: string
    """
    f_downloadedFileName = getGoogleDrivePicture(p_file.googleID, p_path)
    #print("downloadGooglePicture() filename:", f_downloadedFileName)
    return f_downloadedFileName
def loadFiles(p_allFiles):
    """
    Downloads a list of files from google drive if we haven't downloaded them already.
    Used for testing purposes.
    :param p_allFiles: information about each test file, including filename and googleID
    :type p_file: list<TestFile class instance>

    :return: full names of the files loaded including their paths. This includes the prexisting files.
    :rtype: list<string>
    """
    f_filenames = []
    #check if we have each file  <-   allFiles
    for i_file in p_allFiles:
        if os.path.isfile(i_file.fullname)==False:
        #for each missing file
            # download file from google drive
            f_filenames.append(downloadGooglePicture(i_file))
        else:
            f_filenames.append(i_file.fullname)
    return f_filenames
def singleClone(p_filename, p_stop=False):
    """
    creates a copy of a file and gives the copy a "clone name".
    Used to create fresh files for metadata editting tests
    example:
        given a file home/user/pictures/birds.jpg exists,
        singleClone('home/user/pictures/birds.jpg')
        will return "home/user/pictures/birdsCopy.jpg"
        and 'home/user/pictures/birdsCopy.jpg' will be created
    Note: according to the shutil documentation, this might not copy all metadata
    :param p_filename: full filename including the path
    :type p_filename: string
    :param p_stop: True if we want to prevent existing clones from being overwritten (default: False)
    :type p_stop: Boolean

    :raise OSError: if no file with p_filename is found
    :raise ValueError: if p_stop is True and a file with a clone's name already exists

    :return: name of the cloned file including the path
    :rtype: string
    """
    ext = MetadataManagerL0.getExtension(p_filename)
    f_name = p_filename[:-len(ext)]
    f_newfile = f_name+"Copy"+ext
    if os.path.isfile(f_newfile)==True:
        if p_stop:
            raise ValueError('File \'{}\' already exists'.format(f_newfile))
        else:
            singleRelease(f_newfile)
            shutil.copy2(p_filename, f_newfile)
    shutil.copy2(p_filename, f_newfile)
    return f_newfile
def cloneThese(p_filenames):
    """
    creates a copies of several files at once.
    Used to create fresh files for metadata editting tests.
    For a given test, we give this function a list of the files needed.
    :param p_filenames: full filenames including the paths
    :type p_filename: list<string>

    :raise OSError: if no file with p_filename is found
    :raise ValueError: if p_stop is True and a file with a clone's name already exists

    :return: names of the cloned files including the paths
    :rtype: list<string>
    """
    f_clonefiles = []
    for i_filename in p_filenames:
        f_clonefiles.append(singleClone(i_filename))
    return f_clonefiles

def removeAllFiles(p_fileList=g_fileList ,p_path=g_outpath):
    """
    removes several files at once.
    Used for testing to remove original or copied files once they aren't needed
    :param p_fileList: information about each test file including filenames (default: g_fileList from TData)
    :type p_fileList: list<TestFile class instance>
    :param p_path: path the files will be saved to (default: g_outpath imported from TData)
    :type p_path: string
    """
    f_file = ''
    for item in p_fileList:
        f_file = p_path + '/' + item.filename
        if os.path.exists(f_file):
            #print("removeAllFiles() removing ", f_file)
            os.remove(f_file)
    return
def singleRelease(p_filename):
    """
    removes a file. Redundant
    Used with singleClone(). Removes the copy that function created.
    :param p_filename: full filename including the path
    :type p_filename: string

    :raise OSError: if no file with p_filename is found

    :return: name of the cloned file including the path
    :rtype: string
    """
    #print("singleRelease removing ", p_filename)
    os.remove(p_filename)
def releaseAllClones(p_clonelist):
    """
    Removes several files at once.
    p_clonelist should be obtained from cloneThis()
    Used for testing to clean up files left by previous tests
    Used with singleClone(). Removes the copy that function created.
    :param p_clonelist: full filenames including their paths
    :type p_clonelist: list<string>
    """
    for i_file in p_clonelist:
        if os.path.exists(i_file):
            #print("releaseAllClones() removing ", i_file)
            os.remove(i_file)

# ===========================================================================
# ------------------------Windows Metadata Testing---------------------------
# ===========================================================================
"""
Windows has some capalibities that let users add metadata to certain kinds of files just using
the windows file explorer. 
We want our software to be compatible with all of this behaviour. 
So we need to know how these windows metadata operations behave. 

Testing 1:
We will need to make a list of all type of metadata that windows allows us to add and modify.
This will all be put into a chart. (wChart1)
Testing 2:
For every data type in wChart1, we will perform tests at various stages and document the results.
-control test:		This test will only be done once per filetype.
                    We will download a fresh file with no metadata into windows
                    and document what metadata tags and values it has.
-init keys test:	When we add a new kind of metadata to a file (that hasn't have it before),
                    We will check to see what exif tags were added.
-init format test:	Done alongside init keys test. This will be used to check the formatting
                    of the metadata added by windows. Our program must be able to read this.
                    Here we must figure out how to translate the metadata into a human readable format.
-modify test:		We will modify metadata values (like change the title, add and artist, change a tag)
                    then we will see if we can still use our format translation from init format test
-remove/wipe test:  We will erase a value, leaving a blank value. We need to see if windows 
                    allows blank or empty metadata values, or if it immediately wipes them.
                    This will be checking if the keys from the init keys test still exist.
                    and if the blank values can be read
-wipe key test:		We will completely remove a value (value must be previously non-empty) 
                    and check if all the keys from init keys test were removed.
-wipe value test:	Done alongside wipe key test. This will check if we can still fetch a value
                    after removing it from a file using windows. 

Testing 3:
This testing will be performed alongside or after General Metadata Testing (below)
For every key found in the init keys test:
-General Metadata Testing		all tests from this test group will be performed and documented.
                    All tests performed afterwards will assume a key passed all general metadata tests.
-read add:			Given a file with no metadata, we will add a key/value to the metadata.
                    The value will have the formatting from the init format test.
                    We will check to see if windows recognizes our added metadata and displays it.
-read modify		Given a file which has been given metadata by windows, we will edit the value
                    of that metadata and see if windows recognizes and displays those changes. 
-read remove:		Given a file which has been given metadata by windows, we will make the value blank
                    and see if windows still shows that kind of metadata as holding a blank value
-read wipe:			Given a file which has been given metadata by windows, we remove the key/value
                    then check to see if windows recognizes this and displays those changes.
"""

# ===========================================================================
# ------------------------General Metadata Testing---------------------------
# ===========================================================================
"""
Most types of of metadata (title, tags, creator, etc) have multiple tags that could store them in a file. 
Some tags will not work for some file types. Some tags are non-standard and discouraged. 
Some tags won't work with pyexiv2.
Our goal is to figure out what keys can be used to successfully store metadata in various file types.
Every kind of metadata (datatype) is mandatory. Every filetype is mandatory. 
For every combination of datatype and filetype, there must be at least one tag that can be used.

GENERAL FILE BEHAVIOR  (for any single filetype)
    A file has an index with every key of metadata successfully stored in it.
    No two datatypes can have the same key associated with them. 
    A datatype may have more than one key associated with it.
    If (the only) key for a datatype is in the index, it must have a value binded to it
        However, this value can be empty (like the string " ")
    A key may have "sister keys". These sister keys contain values tied to 
        the first key's value (like rating and ratingpercent)
    If a key has sister keys, it and all the sister keys are associated keys of the same datatype.
        All previous rules about keys, datatypes, and values apply to sister keys. 
    It is allowed for a sister key to be impossible to set directly, but it must be possible to change the value
        by setting an associated key
    Each datatype's associated value will have a required type.
    
    
KEY REQUIREMENTS (as in requirements of a key)
given a datatype and filetype, a key must be able to perform 3 operations
    GET
        if a file does not have a value of this datatype, get must return an empty value of some kind.		
                                [check for " " from get, assuming no value exists]
        given a file has a value of this datatype stored, get must return it.								
                                [difficult to prove]
        if a value of a datatype has been set, the value from get might be formatted differently						
                                [function comparing value differences to LEARN format]
        A value of the datatype must be (or must be able to be transformed into) the required type				
                                [Check to LEARN if this is possible]
    SET
        for a given key, the value given to set might have to be in a specific format											
                                [set test to LEARN format requirement]
        The required type for the datatype must be representable in the previously mentioned format								
                                [test to LEARN if this is possible]
        if a file does not have a value of this datatype, no associated keys must be in the index before set					
                                [function checking for EXPECTED index]
        It must be possible to set the value of a key to an empty value of some kind. 											
                                [set key to empty value to LEARN]
        given a file has a value of this type stored, set must replace this with a new value. 									
            The old value must not be availible anywhere associated with that datatype											
                                [set all associated keys to empty value then check all their EXPECTED values]
        If a file does not have a value of this datatype, and set is used, 
            the key for that datatype must be in the index.		
                                [function checking for EXPECTED index changes]
        Setting a value for a single key may automatically cause the inclusion and value setting for other						
                                [function comparing index differences to LEARN changes]
            associated keys (this is the case for sister keys)
        If a datatype has more than one associated key, all those keys must be in the index 									
                                [function checking index for EXPECTED keys]
            given the file has that metadata of that type stored inside it
        If the value for a datatype is changed, the values of all the associated keys must be changed.							
                                [check for EXPECTED differences in values from each associated key]
    WIPE
        It must be possible to remove the key from the index with a wipe														
                                [function checking for EXPECTED index changes]
        Given a datatype has multiple associated keys, wiping that datatype must remove all associated keys 
            from the index,	along with the values binded to them. 		
                                [function checking for EXPECTED index changes]
                                                                                        
        If a file has metadata of a given type, but that metadata is then wiped, 												
            the keys must not be in the index. Those metadata values must not be retrievable.
                               [wipe, then set all associated keys to empty value then check all their EXPECTED values]
    
    CONTAINS (this simply tells us if a value of a datatype is present based on the keys in the index)
        if a file does not have a value of this datatype, no associated keys must be in the index								
                                        [tested with wipe]
        If a datatype has more than one associated key, all those keys must be in the index 									
            if the file has that metadata of that type stored inside it
                                        [tested with set]
"""
"""
Things we need to begin:
    A list of the datatypes			(title, tags, creator, etc)
    A list of the associated required types for their values	(string, int, list<string>, etc)
    A list of potential keys associated with each datatype
    A list of filetypes
        jpeg
        png
        gif
        tiff
    An empty file for each datatype (available for fresh download via google drive)
    A spreadsheet of accepted keys for each filetype/datatype combination
    A list of values that we will use for the keys
"""
"""
Given a datatype/filetype combination and a key
We will do the following things to test it:
    #TODO
    #TODO
    #testing procedure not yet defined. 
"""


# ===========================================================================
# ------------------------Banging Rocks Together 201-------------------------
# ===========================================================================

def EverythingUseageCheck(p_fileEntry, p_testfilelist, f_outpath=g_outpath):
    #the file you load better have all this metadata in it.
    f_picID = p_testfilelist[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_metadata = pyexiv2.ImageMetadata(f_filename)
    f_metadata.read()
    print(f_metadata.exif_keys)
    #-------------Title--------------------------------------
    key1 = 'Exif.Image.XPTitle'
    f_keywords1 = f_metadata[key1]
    f_dirtyString1 = pyexiv2.utils.undefined_to_string(f_keywords1.value)
    print("titleUseageCheck() f_dirtyString1: \t\t", f_dirtyString1)
    f_cleanThing1 = MetadataManagerL0.dirtyStr2cleanStr(f_dirtyString1)
    print("titleUseageCheck() Title\t\t", f_cleanThing1)
    # -------------Tags--------------------------------------
    key2 = 'Exif.Image.XPTitle'
    f_keywords2 = f_metadata[key2]
    f_dirtyString2 = pyexiv2.utils.undefined_to_string(f_keywords2.value)
    print("titleUseageCheck() f_dirtyString2: \t\t", f_dirtyString2)
    f_cleanThing2 = MetadataManagerL0.dirtyStr2cleanList(f_dirtyString2)
    print("titleUseageCheck() Tags\t\t", f_cleanThing2)
    # -------------Artist--------------------------------------
    key3 = 'Exif.Image.XPAuthor'
    f_keywords3 = f_metadata[key3]
    f_dirtyString3 = pyexiv2.utils.undefined_to_string(f_keywords3.value)
    print("titleUseageCheck() f_dirtyString3: \t\t", f_dirtyString3)
    f_cleanThing3 = MetadataManagerL0.dirtyStr2cleanList(f_dirtyString3)
    print("titleUseageCheck() Artist\t\t", f_cleanThing3)
    # -------------Description--------------------------------------
    key4 = 'Exif.Image.XPComment'
    f_keywords4 = f_metadata[key4]
    f_dirtyString4 = pyexiv2.utils.undefined_to_string(f_keywords4.value)
    print("titleUseageCheck() f_dirtyString4: \t\t", f_dirtyString4)
    f_cleanThing4 = MetadataManagerL0.dirtyStr2cleanStr(f_dirtyString4)
    print("titleUseageCheck() Description\t\t", f_cleanThing4)
    # -------------Rating--------------------------------------
    key5 = 'Exif.Image.Rating'
    f_keywords5 = f_metadata[key5]
    print("titleUseageCheck() f_keywords5: \t\t", f_keywords5)
    print("titleUseageCheck() f_keywords5.value: \t\t", f_keywords5.value)
    #f_metadata.__delitem__('Exif.Image.Rating')
    #f_metadata.__delitem__('Exif.Image.RatingPercent')
    #f_metadata.write()
    #f_metadata.read()
    #print(f_metadata.exif_keys)


    # ------------Source URL-----------------------------------

    key6 = 'Exif.Image.ImageHistory'
    value6 = "modified by file tagger"
    f_metadata[key6] = pyexiv2.ExifTag(key6, value6)
    f_metadata.write()
    f_metadata.read()
    print(f_metadata.exif_keys)
    f_keywords6 = f_metadata[key6]
    print("titleUseageCheck() f_keywords6: \t\t", f_keywords6)
    print("titleUseageCheck() f_keywords6.value: \t\t", f_keywords6.value)
    print("titleUseageCheck() type(f_keywords6.value): \t\t", type(f_keywords6.value))

    # ------------Original Date--------------------------------

    key7 = 'Exif.Photo.DateTimeOriginal'
    f_keywords7 = f_metadata[key7]
    print("titleUseageCheck() f_keywords7: \t\t", f_keywords7)
    print("titleUseageCheck() f_keywords7.value: \t\t", f_keywords7.value)
    print("titleUseageCheck() type(f_keywords7.value): \t\t", type(f_keywords7.value))


    #f_dirtyTagString = pyexiv2.utils.undefined_to_string(f_keywords.value)
    #print("titleUseageCheck() f_dirtyTagString\t\t", f_dirtyTagString)
    #f_cleanTagList = MetadataManager.dirtyStr2cleanList(f_dirtyTagString)
    #print("titleUseageCheck() f_cleanTagList\t\t", f_cleanTagList)
    #f_dirtyTagString2 = MetadataManager.cleanList2dirtyStr(f_cleanTagList)
    #print("titleUseageCheck() f_dirtyTagString2\t\t", f_dirtyTagString2)
    os.remove(f_filename)
    return

def tagUseageCheck(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    print(f_metadata.exif_keys)
    f_keywords = f_metadata['Exif.Image.XPKeywords']
    f_dirtyTagString = pyexiv2.utils.undefined_to_string(f_keywords.value)
    print("tagUseageCheck() f_dirtyTagString\t\t", f_dirtyTagString)
    f_cleanTagList = MetadataManagerL0.dirtyStr2cleanList(f_dirtyTagString)
    print("tagUseageCheck() f_cleanTagList\t\t", f_cleanTagList)
    f_dirtyTagString2 = MetadataManagerL0.cleanList2dirtyStr(f_cleanTagList)
    print("tagUseageCheck() f_dirtyTagString2\t\t", f_dirtyTagString2)
    return


def tryAddData(p_filename):
    #this will try to add every kind of metadata possible to an image.
    #-------------Title--------------------------------------
    MetadataManagerL0.setTitle(p_filename, "testFile")
    # -------------Tags--------------------------------------
    MetadataManagerL1.addArtist(p_filename, "creator: weirdo")
    # -------------Artist------------------------------------
    MetadataManagerL1.addTag(p_filename, "test")
    # -------------Description-------------------------------
    MetadataManagerL0.setDescr(p_filename, "this is a sample description")
    # -------------Rating------------------------------------
    MetadataManagerL0.setRating(p_filename, 3)
    return


#some test that can check if all possible keys were used in set functions

#some test to check if all keys from a set function have equal values

# ===========================================================================
# ---------------------Unit Testing Utility Functions------------------------
# ===========================================================================

#this should be true after a successful set operation is performed
def checkAllKeysPresent(p_file, p_metatype):
    #takes a filename and a metadata type (Title, Description, Tags, etc)
    #and returns true if all keys associated with that metadata type are present in the file
    #used for testing the metadata editing functions
    f_metadata = pyexiv2.ImageMetadata(p_file)
    f_metadata.read()
    f_keys = MetadataManagerL0.appropriateKeys(p_file, p_metatype)
    for key in f_keys:
        if key not in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            return False
    return True

#this should be false after a successful wipe operation is performed
def checkAnyKeysPresent(p_file, p_metatype, p_verbose=False):
    #takes a filename and a metadata type (Title, Description, Tags, etc)
    #and returns true if any keys associated with that metadata type are present in the file
    #used for testing the metadata editing functions
    f_metadata = pyexiv2.ImageMetadata(p_file)
    f_metadata.read()
    f_keys = MetadataManagerL0.appropriateKeys(p_file, p_metatype)
    f_present = []
    for key in f_keys:
        if key in (f_metadata.exif_keys + f_metadata.xmp_keys + f_metadata.iptc_keys):
            f_present.append(key)
    if p_verbose:
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
