#!/usr/bin/env python3
import os
import wget
import requests
import MetadataManager
import pyexiv2
import copy



g_outpath = '/home/hwynn/Pictures'
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
    return f_filename
# I made everything from this point on
"""
Author: Harrison Wynn
Created: 2018
"""

g_googlePics1 = {'squirrel': '1ZHDchSv9RMxJmdVeepJvvOtTx4T4am3U',
                 'cat': "1A1Nxr-1mWfFlk9hTVZtzSPfEt6ZC6uzg",
                 'boxcat': "1oxAPZSBKKTYjdXYYuwpvbKR5grK0aCZY",
                 'frogyellow': '1xMHPQrNyODWTIXQ-PxgWSPbwj7_tGerv',
                 'frogjump': '1nqFSb-hoc1c0-BlTETs0jQn3bzWeGg3T',
                 'titanmeme': "1kRybASv2UVde5wMitn_j1i4x3LklIh6s"}
g_googlePics2 = {'fixingComputer': '1pFEbWruySWWgNCShKP8qn8dJ9w7kXNKk',
                 'catScreamPizza': '1eED3AINVizIQV44DXxj91-s2Qa9EWsAX',
                 'gregTwitterJoke': '1PzDc70qhskQzUPtCgoRG3W10AisiP09W',
                 'wikihowRat': '18mFIgX2Na5DCdTO49fwamAMfdqJcjodP',
                 'rippledotzero': '1euq0D6OrdWVkdC4RZdFIrre7WsQ7N9do',
                 'oppusumBitesApple': '1EWTG-xgYGX_SdB4lPDFEs5veattK5Dxy',
                 'creepyCharger': '1MQgoUI6tIQhkNMg7KIDeRraVsGhPrx0H',
                 'princessAtDoor': '1TKjnok6DJuIHYhaeZiYFnS6RgPRcdJPK', }
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
# ----------------------Title Metadata Test functions------------------------
# ===========================================================================
g_getTitle_testData = {'fixingComputer': "crazy man fixing computer",
                       'catScreamPizza': "",
                       'gregTwitterJoke': "greg throws knives",
                       'wikihowRat': "wikihow rat",
                       'rippledotzero': "rippledotzero cover",
                       'oppusumBitesApple': "too small for apple",
                       'creepyCharger': "",
                       'princessAtDoor': "", }
g_containsTitle_testData = {'fixingComputer': True,
                            'catScreamPizza': False,
                            'gregTwitterJoke': True,
                            'wikihowRat': True,
                            'rippledotzero': True,
                            'oppusumBitesApple': True,
                            'creepyCharger': False,
                            'princessAtDoor': False, }
g_setTitle_testData = {'fixingComputer': "stock image of me",
                       'catScreamPizza': "the pizza is here",
                       'gregTwitterJoke': "NITW joke",
                       'wikihowRat': "cool rat",
                       'rippledotzero': "flash game thing",
                       'oppusumBitesApple': "cute opposum",
                       'creepyCharger': "creepy charger",
                       'princessAtDoor': "cute dog gif", }
g_searchTitle_testData = {'fixingComputer': "computer",
                          'catScreamPizza': "dog",
                          'gregTwitterJoke': "greg",
                          'wikihowRat': "rat",
                          'rippledotzero': "game",
                          'oppusumBitesApple': "oppusum",
                          'creepyCharger': "charger",
                          'princessAtDoor': "dog", }
g_searchTitle_testResults = {'fixingComputer': True,
                             'catScreamPizza': False,
                             'gregTwitterJoke': True,
                             'wikihowRat': True,
                             'rippledotzero': False,
                             'oppusumBitesApple': False,
                             'creepyCharger': False,
                             'princessAtDoor': False, }
def EverythingUseageCheck(p_fileEntry, f_outpath=g_outpath):
    #the file you load better have all this metadata in it.
    f_picID = g_googlePics2[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_metadata = pyexiv2.ImageMetadata(f_filename)
    f_metadata.read()
    print(f_metadata.exif_keys)
    #-------------Title--------------------------------------
    key1 = 'Exif.Image.XPTitle'
    f_keywords1 = f_metadata[key1]
    f_dirtyString1 = pyexiv2.utils.undefined_to_string(f_keywords1.value)
    print("titleUseageCheck() f_dirtyString1: \t\t", f_dirtyString1)
    f_cleanThing1 = MetadataManager.dirtyStr2cleanStr(f_dirtyString1)
    print("titleUseageCheck() Title\t\t", f_cleanThing1)
    # -------------Tags--------------------------------------
    key2 = 'Exif.Image.XPTitle'
    f_keywords2 = f_metadata[key2]
    f_dirtyString2 = pyexiv2.utils.undefined_to_string(f_keywords2.value)
    print("titleUseageCheck() f_dirtyString2: \t\t", f_dirtyString2)
    f_cleanThing2 = MetadataManager.dirtyStr2cleanList(f_dirtyString2)
    print("titleUseageCheck() Tags\t\t", f_cleanThing2)
    # -------------Artist--------------------------------------
    key3 = 'Exif.Image.XPAuthor'
    f_keywords3 = f_metadata[key3]
    f_dirtyString3 = pyexiv2.utils.undefined_to_string(f_keywords3.value)
    print("titleUseageCheck() f_dirtyString3: \t\t", f_dirtyString3)
    f_cleanThing3 = MetadataManager.dirtyStr2cleanList(f_dirtyString3)
    print("titleUseageCheck() Artist\t\t", f_cleanThing3)
    # -------------Description--------------------------------------
    key4 = 'Exif.Image.XPComment'
    f_keywords4 = f_metadata[key4]
    f_dirtyString4 = pyexiv2.utils.undefined_to_string(f_keywords4.value)
    print("titleUseageCheck() f_dirtyString4: \t\t", f_dirtyString4)
    f_cleanThing4 = MetadataManager.dirtyStr2cleanStr(f_dirtyString4)
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

#EverythingUseageCheck('fixingComputer')

# ===========================================================================
# ----------------------Artist Metadata Test functions-----------------------
# ===========================================================================
g_getArtists_testData = {'fixingComputer': ["stockphotographer", "publisher: twitter"],
                         'catScreamPizza': ["photographer: idunno", "publisher: tumblrguy"],
                         'gregTwitterJoke': [],
                         'wikihowRat': ["volunteer tracer"],
                         'rippledotzero': ["penguindude"],
                         'oppusumBitesApple': ["VoteForPuff"],
                         'creepyCharger': [],
                         'princessAtDoor': []}
g_containsArtists_testData = {'fixingComputer': True,
                              'catScreamPizza': True,
                              'gregTwitterJoke': False,
                              'wikihowRat': True,
                              'rippledotzero': True,
                              'oppusumBitesApple': True,
                              'creepyCharger': False,
                              'princessAtDoor': False}
g_setArtists_testData = {'fixingComputer': ["stock photo", "funny", "bad stock photos of my job", "technology"],
                         'catScreamPizza': ["Phil"],
                         'gregTwitterJoke': ["Joe"],
                         'wikihowRat': ["volunteer"],
                         'rippledotzero': ["Simon"],
                         'oppusumBitesApple': ["Vote"],
                         'creepyCharger': [],
                         'princessAtDoor': []}
g_searchArtist_testData = {'fixingComputer': "twitter",
                           'catScreamPizza': "Phil",
                           'gregTwitterJoke': "Joe",
                           'wikihowRat': "volunteer",
                           'rippledotzero': "Simon",
                           'oppusumBitesApple': "Vote",
                           'creepyCharger': "",
                           'princessAtDoor': ""}
g_searchArtist_testResults = {'fixingComputer': True,
                              'catScreamPizza': False,
                              'gregTwitterJoke': False,
                              'wikihowRat': True,
                              'rippledotzero': True,
                              'oppusumBitesApple': True,
                              'creepyCharger': False,
                              'princessAtDoor': False}
g_addArtist_testData = {'fixingComputer': "model: crazyguy",
                        'catScreamPizza': "model: pizzadog",
                        'gregTwitterJoke': "Solomon Georgio",
                        'wikihowRat': "publisher: wikihow",
                        'rippledotzero': "Artist: Simon Stalenhag",
                        'oppusumBitesApple': "Model: opposum baby",
                        'creepyCharger': "",
                        'princessAtDoor': ""}
def containsArtistsTest(p_fileEntry, f_outpath=g_outpath):
    # This tests if the function
    # containsArtists() is working properly.
    # Returns true if test passes, otherwise false
    f_picID = g_googlePics1[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_hasArtistTruth1 = g_containsArtists_testData[p_fileEntry]
    f_hasArtistTruth2 = MetadataManager.containsArtists(f_filename)
    if (f_hasArtistTruth1 != f_hasArtistTruth2):
        print("Test FAILED: containsArtists() didn't return the expected truth value")
        os.remove(f_filename)
        return False
    print("Test PASSED: containsArtists() returned the expected truth value")
    os.remove(f_filename)
    return True
def getArtistsTest(p_fileEntry, f_outpath=g_outpath):
    """Warning!!! Please don't try this with a picture with no tags."""
    f_picID = g_googlePics1[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_cleanArtistList = copy.deepcopy(g_getArtists_testData[p_fileEntry])
    # print("getArtistsTest() f_cleanArtistList:\t\t", f_cleanArtistList)
    f_newArtists = MetadataManager.getArtists(f_filename)
    if (f_newArtists != f_cleanArtistList):
        print("Test FAILED: getArtistsTest() didn't find the tags it should have.")
        print("Artists expected:", end="")
        for tag1 in f_cleanArtistList:
            print("\"", tag1, "\"", sep="", end=" ")
        print()
        print("Artists found:", end="")
        for tag2 in f_newArtists:
            print("\"", tag2, "\"", sep="", end=" ")
        print()
        os.remove(f_filename)
        return False
    print("Test PASSED: getArtistsTest() found the proper tags")
    print("Artists expected:", end="")
    for tag1 in f_cleanArtistList:
        print("\"", tag1, "\"", sep="", end=" ")
    print()
    print("Artists found:", end="")
    for tag2 in f_newArtists:
        print("\"", tag2, "\"", sep="", end=" ")
    print()
    os.remove(f_filename)
    return True
def setArtistsTest(p_fileEntry, f_outpath=g_outpath):
    f_picID = g_googlePics1[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_tags = g_setArtists_testData[p_fileEntry]
    MetadataManager.setArtists(f_filename, f_tags)
    f_newArtists = MetadataManager.getArtists(f_filename)
    if (f_newArtists != f_tags):
        print("Test FAILED: setArtistsTest() didn't find the tags it should have")
        print("Artists expected:", end="")
        for tag1 in f_tags:
            print("\"", tag1, "\"", sep="", end=" ")
        print("Artists found:", end="")
        for tag2 in f_newArtists:
            print("\"", tag2, "\"", sep="", end=" ")
        print()
        os.remove(f_filename)
        return False
    print("Test PASSED: setArtistsTest() found the proper tags")
    os.remove(f_filename)
    return True
def searchArtistTest(p_fileEntry, f_outpath=g_outpath):
    f_picID = g_googlePics1[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_hasArtistTruth1 = g_searchArtist_testResults[p_fileEntry]
    f_tag = g_searchArtist_testData[p_fileEntry]
    f_hasArtistTruth2 = MetadataManager.hasArtists(f_filename, f_tag)
    if (f_hasArtistTruth1 != f_hasArtistTruth2):
        print("Test FAILED: searchArtistTest() didn't return the expected truth value")
        os.remove(f_filename)
        return False
    print("Test PASSED: searchArtistTest() returned the expected truth value")
    os.remove(f_filename)
    return True
def addArtistTest(p_fileEntry, f_outpath=g_outpath):
    f_picID = g_googlePics1[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_newArtist = g_addArtist_testData[p_fileEntry]
    f_tags = copy.deepcopy(g_getArtists_testData[p_fileEntry])
    MetadataManager.addArtist(f_filename, f_newArtist)
    f_tags.insert(0, f_newArtist)
    f_tagList1 = f_tags
    f_tagList2 = MetadataManager.getArtists(f_filename)
    if (f_tagList1 != f_tagList2):
        print("Test FAILED: addArtistTest() didn't find the tags it should have")
        print(f_newArtist, "should have been added to", g_getArtists_testData[p_fileEntry])
        print("Artists expected:", end="")
        print(f_tagList1)
        print("Artists found:", end="")
        print(f_tagList2)
        os.remove(f_filename)
        return False
    print("Test PASSED: addArtistTest() found the proper tags")
    os.remove(f_filename)
    return True
# ===========================================================================
# ----------------------Tag Metadata Test functions--------------------------
# ===========================================================================
"""Note: The following variables have a mixed naming convention.
please forgive my deviation from proper naming style.
These names are used since they are used in a testing function which
tests a utility function. These names contain the utility function's name
for the sake of consistency and easy maintenance"""
g_containsTags_testData = {'squirrel': True,
                           'cat': False,
                           'boxcat': True,
                           "frogyellow": True,
                           "frogjump": True,
                           "titanmeme": True}
g_getTags_testData = {'squirrel': ['squirrel'],
                      'cat': [],
                      'boxcat': ['cat', 'animals', 'cat in a box'],
                      "frogyellow": ['frog'],
                      "frogjump": ['frog'],
                      "titanmeme": ['show screenshots']}
g_setTags_testData = {}
g_searchTags_testData = {'squirrel': 'pie',
                         'cat': "cat",
                         'boxcat': "ca",
                         "frogyellow": 'frog',
                         "frogjump": "jumping",
                         "titanmeme": 'show screenshots'}
g_searchTags_testResults = {'squirrel': False,
                            'cat': False,
                            'boxcat': False,
                            "frogyellow": True,
                            "frogjump": False,
                            "titanmeme": True}
g_addTag_testData = {'squirrel': 'animals',
                     'cat': "cat",
                     'boxcat': "cute",
                     "frogyellow": 'amphibian',
                     "frogjump": "jumping",
                     "titanmeme": 'anime'}
g_removeTag_testData = {'squirrel': 'squirrel',
                        'cat': "",
                        'boxcat': "animals",
                        "frogyellow": 'frog',
                        "frogjump": "frog",
                        "titanmeme": 'show screenshots'}
def containsTagsTest(p_fileEntry, f_outpath=g_outpath):
    # This tests if the function
    # containsTags() is working properly.
    # Returns true if test passes, otherwise false
    f_picID = g_googlePics1[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_hasTagTruth1 = g_containsTags_testData[p_fileEntry]
    f_hasTagTruth2 = MetadataManager.containsTags(f_filename)
    if (f_hasTagTruth1 != f_hasTagTruth2):
        print("Test FAILED: containsTags() didn't return the expected truth value")
        os.remove(f_filename)
        return False
    print("Test PASSED: containsTags() returned the expected truth value")
    os.remove(f_filename)
    return True
def getTagsTest(p_fileEntry, f_outpath=g_outpath):
    """Warning!!! Please don't try this with a picture with no tags."""
    f_picID = g_googlePics1[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_cleanTagList = copy.deepcopy(g_getTags_testData[p_fileEntry])
    # print("getTagsTest() f_cleanTagList:\t\t", f_cleanTagList)
    f_newTags = MetadataManager.getTags(f_filename)
    if (f_newTags != f_cleanTagList):
        print("Test FAILED: getTagsTest() didn't find the tags it should have.")
        print("Tags expected:", end="")
        for tag1 in f_cleanTagList:
            print("\"", tag1, "\"", sep="", end=" ")
        print()
        print("Tags found:", end="")
        for tag2 in f_newTags:
            print("\"", tag2, "\"", sep="", end=" ")
        print()
        os.remove(f_filename)
        return False
    print("Test PASSED: getTagsTest() found the proper tags")
    print("Tags expected:", end="")
    for tag1 in f_cleanTagList:
        print("\"", tag1, "\"", sep="", end=" ")
    print()
    print("Tags found:", end="")
    for tag2 in f_newTags:
        print("\"", tag2, "\"", sep="", end=" ")
    print()
    os.remove(f_filename)
    return True
def setTagsTest(p_fileEntry, p_tags, f_outpath=g_outpath):
    f_picID = g_googlePics1[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    MetadataManager.setTags(f_filename, p_tags)
    f_newTags = MetadataManager.getTags(f_filename)
    if (f_newTags != p_tags):
        print("Test FAILED: setTagsTest() didn't find the tags it should have")
        print("Tags expected:", end="")
        for tag1 in p_tags:
            print("\"", tag1, "\"", sep="", end=" ")
        print("Tags found:", end="")
        for tag2 in f_newTags:
            print("\"", tag2, "\"", sep="", end=" ")
        print()
        os.remove(f_filename)
        return False
    print("Test PASSED: setTagsTest() found the proper tags")
    os.remove(f_filename)
    return True
def searchTagsTest(p_fileEntry, f_outpath=g_outpath):
    f_picID = g_googlePics1[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_hasTagTruth1 = g_searchTags_testResults[p_fileEntry]
    f_tag = g_searchTags_testData[p_fileEntry]
    f_hasTagTruth2 = MetadataManager.searchTags(f_filename, f_tag)
    if (f_hasTagTruth1 != f_hasTagTruth2):
        print("Test FAILED: searchTagsTest() didn't return the expected truth value")
        os.remove(f_filename)
        return False
    print("Test PASSED: searchTagsTest() returned the expected truth value")
    os.remove(f_filename)
    return True
def addTagTest(p_fileEntry, f_outpath=g_outpath):
    f_picID = g_googlePics1[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_newTag = g_addTag_testData[p_fileEntry]
    f_tags = copy.deepcopy(g_getTags_testData[p_fileEntry])
    MetadataManager.addTag(f_filename, f_newTag)
    f_tags.insert(0, f_newTag)
    f_tagList1 = f_tags
    f_tagList2 = MetadataManager.getTags(f_filename)
    if (f_tagList1 != f_tagList2):
        print("Test FAILED: addTagTest() didn't find the tags it should have")
        print(f_newTag, "should have been added to", g_getTags_testData[p_fileEntry])
        print("Tags expected:", end="")
        print(f_tagList1)
        print("Tags found:", end="")
        print(f_tagList2)
        os.remove(f_filename)
        return False
    print("Test PASSED: addTagTest() found the proper tags")
    os.remove(f_filename)
    return True
def removeTagTest(p_fileEntry, f_outpath=g_outpath):
    f_picID = g_googlePics1[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_removeThisTag = g_removeTag_testData[p_fileEntry]
    f_tags = copy.deepcopy(g_getTags_testData[p_fileEntry])
    MetadataManager.removeTag(f_filename, f_removeThisTag)
    f_tags.remove(f_removeThisTag)
    f_tagList1 = f_tags
    f_tagList2 = MetadataManager.getTags(f_filename)
    if (f_tagList1 != f_tagList2):
        print("Test FAILED: removeTagTest() didn't find the tags it should have")
        print(g_removeTag_testData[p_fileEntry], "should have been removed from", g_getTags_testData[p_fileEntry])
        print("Tags expected:", end="")
        print(f_tagList1)
        print("Tags found:", end="")
        print(f_tagList2)
        os.remove(f_filename)
        return False
    print("Test PASSED removeTagTest(): The file", f_filename, " has the tags it should.")
    print(g_removeTag_testData[p_fileEntry], "was successfully removed from", g_getTags_testData[p_fileEntry])
    print("Tags expected:", end="")
    print(f_tagList1)
    print("Tags found:", end="")
    print(f_tagList2)
    os.remove(f_filename)
    return True

def tagUseageCheck(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    print(f_metadata.exif_keys)
    f_keywords = f_metadata['Exif.Image.XPKeywords']
    f_dirtyTagString = pyexiv2.utils.undefined_to_string(f_keywords.value)
    print("tagUseageCheck() f_dirtyTagString\t\t", f_dirtyTagString)
    f_cleanTagList = MetadataManager.dirtyStr2cleanList(f_dirtyTagString)
    print("tagUseageCheck() f_cleanTagList\t\t", f_cleanTagList)
    f_dirtyTagString2 = MetadataManager.cleanList2dirtyStr(f_cleanTagList)
    print("tagUseageCheck() f_dirtyTagString2\t\t", f_dirtyTagString2)
    return

# ===========================================================================
# -----Tag Metadata Tests. Successful for CatInBox.jpg-----------------------
# ===========================================================================

#containsTagsTest("boxcat")
#getTagsTest("boxcat")  # test passed
#setTagsTest("boxcat", ["mammal", "feline"])
#searchTagsTest("boxcat")
#addTagTest("boxcat")
#removeTagTest("boxcat")


#testing library function that can give extension
def testExtensionParse2():
    f_filename = ""
    for i_key, i_value in g_googlePics2.items():
        print("i_key:", i_key, "i_value:", i_value)
        f_filename = getGoogleDrivePicture(i_value, g_outpath)
        print("filename:", f_filename)
        print("extension:", MetadataManager.getExtension(f_filename))
        os.remove(f_filename)

#testExtensionParse2()



#some test that can check if all possible keys were used in set functions

#some test to check if all keys from a set function have equal values