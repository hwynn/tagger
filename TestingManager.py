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
g_googlePictures = {'squirrel': '1ZHDchSv9RMxJmdVeepJvvOtTx4T4am3U',
                    'cat': "1A1Nxr-1mWfFlk9hTVZtzSPfEt6ZC6uzg",
                    'boxcat': "1oxAPZSBKKTYjdXYYuwpvbKR5grK0aCZY",
                    "frogyellow": '1xMHPQrNyODWTIXQ-PxgWSPbwj7_tGerv',
                    "frogjump": '1nqFSb-hoc1c0-BlTETs0jQn3bzWeGg3T',
                    "titanmeme": "1kRybASv2UVde5wMitn_j1i4x3LklIh6s"}


g_pictureTags = {'squirrel': ['squirrel'],
                 'cat': [],
                 'boxcat': ['cat', 'animals', 'cat in a box'],
                 "frogyellow": ['frog'],
                 "frogjump": ['frog'],
                 "titanmeme": ['show screenshots']}
g_pictureHasTags = {'squirrel': True,
                    'cat': False,
                    'boxcat': True,
                    "frogyellow": True,
                    "frogjump": True,
                    "titanmeme": True}
g_pictureSearchThis = {'squirrel': 'pie',
                       'cat': "cat",
                       'boxcat': "animals",
                       "frogyellow": 'frog',
                       "frogjump": "jumping",
                       "titanmeme": 'show screenshots'}
g_pictureSearchResult = {'squirrel': False,
                         'cat': False,
                         'boxcat': True,
                         "frogyellow": True,
                         "frogjump": False,
                         "titanmeme": True}
g_pictureAddThisTag = {'squirrel': 'animals',
                       'cat': "cat",
                       'boxcat': "cute",
                       "frogyellow": 'amphibian',
                       "frogjump": "jumping",
                       "titanmeme": 'anime'}
g_pictureRemoveThisTag = {'squirrel': 'squirrel',
                          'cat in a box': "",
                          'boxcat': "animals",
                          "frogyellow": 'frog',
                          "frogjump": "frog",
                          "titanmeme": 'show screenshots'}

def hasAnyTagsTest(p_fileEntry, f_outpath=g_outpath):
    f_picID = g_googlePictures[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_hasTagTruth1 = g_pictureHasTags[p_fileEntry]
    f_hasTagTruth2 = MetadataManager.hasAnyTags(f_filename)
    if (f_hasTagTruth1 != f_hasTagTruth2):
        print("Test FAILED: hasAnyTags() didn't return the expected truth value")
        os.remove(f_filename)
        return False
    print("Test PASSED: hasAnyTags() returned the expected truth value")
    os.remove(f_filename)
    return True


def hasTagsTest(p_fileEntry, f_outpath=g_outpath):
    f_picID = g_googlePictures[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_hasTagTruth1 = g_pictureSearchResult[p_fileEntry]
    f_tag = g_pictureSearchThis[p_fileEntry]
    f_hasTagTruth2 = MetadataManager.hasTags(f_filename, f_tag)
    if (f_hasTagTruth1 != f_hasTagTruth2):
        print("Test FAILED: hasTagsTest() didn't return the expected truth value")
        os.remove(f_filename)
        return False
    print("Test PASSED: hasTagsTest() returned the expected truth value")
    os.remove(f_filename)
    return True


def tagGetTest(p_fileEntry, f_outpath=g_outpath):
    """Warning!!! Please don't try this with a picture with no tags."""
    f_picID = g_googlePictures[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_cleanTagList = copy.deepcopy(g_pictureTags[p_fileEntry])
    # print("tagGetTest() f_cleanTagList:\t\t", f_cleanTagList)
    f_newTags = MetadataManager.getTags(f_filename)
    if (f_newTags != f_cleanTagList):
        print("Test FAILED: tagGetTest() didn't find the tags it should have.")
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
    print("Test PASSED: tagGetTest() found the proper tags")
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


def tagSetTest(p_fileEntry, p_tags, f_outpath=g_outpath):
    f_picID = g_googlePictures[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    MetadataManager.setTags(f_filename, p_tags)
    f_newTags = MetadataManager.getTags(f_filename)
    if (f_newTags != p_tags):
        print("Test FAILED: tagSetTest() didn't find the tags it should have")
        print("Tags expected:", end="")
        for tag1 in p_tags:
            print("\"", tag1, "\"", sep="", end=" ")
        print("Tags found:", end="")
        for tag2 in f_newTags:
            print("\"", tag2, "\"", sep="", end=" ")
        print()
        os.remove(f_filename)
        return False
    print("Test PASSED: tagSetTest() found the proper tags")
    os.remove(f_filename)
    return True


def tagAddTest(p_fileEntry, f_outpath=g_outpath):
    f_picID = g_googlePictures[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_newTag = g_pictureAddThisTag[p_fileEntry]
    f_tags = copy.deepcopy(g_pictureTags[p_fileEntry])
    MetadataManager.addTag(f_filename, f_newTag)
    f_tags.insert(0, f_newTag)
    f_tagList1 = f_tags
    f_tagList2 = MetadataManager.getTags(f_filename)
    if (f_tagList1 != f_tagList2):
        print("Test FAILED: tagAddTest() didn't find the tags it should have")
        print(f_newTag, "should have been added to", g_pictureTags[p_fileEntry])
        print("Tags expected:", end="")
        print(f_tagList1)
        print("Tags found:", end="")
        print(f_tagList2)
        os.remove(f_filename)
        return False
    print("Test PASSED: tagAddTest() found the proper tags")
    os.remove(f_filename)
    return True


def tagRemoveTest(p_fileEntry, f_outpath=g_outpath):
    f_picID = g_googlePictures[p_fileEntry]
    f_filename = getGoogleDrivePicture(f_picID, f_outpath)
    f_removeThisTag = g_pictureRemoveThisTag[p_fileEntry]
    f_tags = copy.deepcopy(g_pictureTags[p_fileEntry])
    MetadataManager.removeTag(f_filename, f_removeThisTag)
    f_tags.remove(f_removeThisTag)
    f_tagList1 = f_tags
    f_tagList2 = MetadataManager.getTags(f_filename)
    if (f_tagList1 != f_tagList2):
        print("Test FAILED: tagRemoveTest() didn't find the tags it should have")
        print(g_pictureRemoveThisTag[p_fileEntry], "should have been removed from", g_pictureTags[p_fileEntry])
        print("Tags expected:", end="")
        print(f_tagList1)
        print("Tags found:", end="")
        print(f_tagList2)
        os.remove(f_filename)
        return False
    print("Test PASSED tagRemoveTest(): The file", f_filename, " has the tags it should.")
    print(g_pictureRemoveThisTag[p_fileEntry], "was successfully removed from", g_pictureTags[p_fileEntry])
    print("Tags expected:", end="")
    print(f_tagList1)
    print("Tags found:", end="")
    print(f_tagList2)
    os.remove(f_filename)
    return True

def useageCheck(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    print(f_metadata.exif_keys)
    f_keywords = f_metadata['Exif.Image.XPKeywords']
    f_dirtyTagString = pyexiv2.utils.undefined_to_string(f_keywords.value)
    print("useageCheck() f_dirtyTagString\t\t", f_dirtyTagString)
    f_cleanTagList = MetadataManager.dirtyStr2cleanList(f_dirtyTagString)
    print("useageCheck() f_cleanTagList\t\t", f_cleanTagList)
    f_dirtyTagString2 = MetadataManager.cleanList2dirtyStr(f_cleanTagList)
    print("useageCheck() f_dirtyTagString2\t\t", f_dirtyTagString2)
    return


# g_picID = g_googlePictures["boxcat"]
# g_filename = getGoogleDrivePicture(g_picID, g_outpath)
# print(g_filename)
# useageCheck(g_filename)
# os.remove(g_filename)

hasAnyTagsTest("boxcat")
hasTagsTest("boxcat")
tagGetTest("boxcat")  # test passed
tagSetTest("boxcat", ["mammal", "feline"])
tagAddTest("boxcat")
tagRemoveTest("boxcat")
