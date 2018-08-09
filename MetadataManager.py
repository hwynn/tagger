#!/usr/bin/env python3
import pyexiv2

# ------edit title metadata
def containsTitle(p_filename):
	"""This will tell us if the file
	has any title metadata.
	Returns bool"""
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    if ((p_filename[-4:] == '.jpg') and ('Exif.Image.XPTitle' in f_metadata.exif_keys)):
        # print("this file already has title data")
        return True
    # print("this file has no title data")
    return False


def getTitle(p_filename):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def setTitle(p_filename, y):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def searchTitle(p_filename, y):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def removeTitle(p_filename):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


# ------edit artist metadata
def containsArtist(p_filename):
	"""This will tell us if the file
	has any artist metadata.
	Returns bool"""
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    if ((p_filename[-4:] == '.jpg') and ('Exif.Image.Artist' in f_metadata.exif_keys)):
        # print("this file already has artist data")
        return True
    # print("this file has no artist data")
    return False


def getArtist(p_filename):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def setArtist(p_filename, y):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def searchArtist(p_filename, y):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def removeArtist(p_filename, y):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


# -----edit tag metadata


def listHexTrim(p_rawList):
    """Takes a freshly translated string list and
    trims the '\x00' ends off all the strings"""
    print("listHexTrim(", p_rawList, ")")
    return [x.replace('\x00', '') for x in p_rawList]


def stringHexTrim(p_bustedTags):
    f_tags = ""
    for y in [x.replace('\x00', '') for x in p_bustedTags]:
        if y != '':
            f_tags += y
    return f_tags


def stringHexify(p_newtag):
    f_bustedTag = ""
    for x in p_newtag:
        f_bustedTag += x
        f_bustedTag += '\x00'
    return f_bustedTag


def dirtyStr2cleanList(p_dirtyTagStr):
    """Takes a semicolon-delimited list of tags
    represented by a dirty (\x00 filled) string.
    This function returns a list of tags
    represented by clean strings"""
    f_dirtyTagList = p_dirtyTagStr.split(';')
    # print("dirtyStr2cleanList(): f_dirtyTagList", f_dirtyTagList)
    f_cleanTagList = [stringHexTrim(x) for x in f_dirtyTagList]
    # print("dirtyStr2cleanList(): f_cleanTagList", f_cleanTagList)
    return f_cleanTagList


def cleanList2dirtyStr(p_cleanTagList):
    """Takes a list of tags
    represented by clean strings.
    This function returns a semicolon-delimited list of tags
    represented by a dirty (\x00 filled) string."""
    f_dirtyTagList = [stringHexify(x) for x in p_cleanTagList]
    # print("cleanList2dirtyStr(): f_dirtyTagList", f_dirtyTagList)
    f_dirtyTagString = ";\x00".join(f_dirtyTagList) + "\x00\x00"
    # print("cleanList2dirtyStr(): f_dirtyTagString", f_dirtyTagString)
    return f_dirtyTagString


def containsTags(p_filename):
	"""This will tell us if the file
	has any tag metadata.
	Returns bool"""
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    if (p_filename[-4:] == '.jpg'):
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
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    if (p_filename[-4:] == '.jpg'):
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
        # TODO add png and gif support
        # TODO error check: does this file have tag data?
        return []
    return []


def setTags(p_filename, p_cleanTagList):
    """Instead of appending a new tag to the list of tags already present
    This function replaces all tags with the list of tags provided as p_cleanTagList.
    Use this function with caution. Because.. you know. It wipes your tags."""
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    if (p_filename[-4:] == '.jpg'):
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
        # TODO add png and gif support
        return True


def searchTags(p_filename, p_tag):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    if (p_filename[-4:] == '.jpg'):
        f_metaData = pyexiv2.ImageMetadata(p_filename)
        f_metaData.read()
        if not containsTags(p_filename):
            return False
        f_keywords = f_metaData['Exif.Image.XPKeywords']
        f_bustedTagString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        if p_tag in stringHexTrim(f_bustedTagString):
            # print("This file already has the tag \"", p_tag ,"\"", sep='')
            return True
        return False
    else:
        # TODO add png and gif support
        # TODO error check: does this file have tag data?
        return False
    return False


def addTag(p_filename, p_tag):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    if (p_filename[-4:] == '.jpg'):
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
            return True
        f_keywords = f_metadata['Exif.Image.XPKeywords']
        f_dirtyTagString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        print("addTag() f_dirtyTagString\t\t", f_dirtyTagString)
        f_cleanTagList = dirtyStr2cleanList(f_dirtyTagString)
        print("addTag() f_cleanTagList\t\t", f_cleanTagList)
        if p_tag in f_cleanTagList:
            print("Warning: file already contains this tag")
            return False
        f_cleanTagList.insert(0, p_tag)
        f_dirtyTagString2 = cleanList2dirtyStr(f_cleanTagList)
        print("addTag() f_dirtyTagString2\t\t", f_dirtyTagString2)
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyTagString2)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return True
    else:
        # TODO add png and gif support
        # TODO error check: does this file have tag data?
        return True
    return False


def removeTag(p_filename, p_tag):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    if (p_filename[-4:] == '.jpg'):
        f_metadata = pyexiv2.ImageMetadata(p_filename)
        f_metadata.read()
        # print(f_metadata.exif_keys)
        if not containsTags(p_filename):
            raise Exception(
                'The file \'{}\' does not contain any tag data \n This operation cannot be performed'.format(
                    p_filename))
        f_keywords = f_metadata['Exif.Image.XPKeywords']
        f_key = 'Exif.Image.XPKeywords'
        f_dirtyTagString = pyexiv2.utils.undefined_to_string(f_keywords.value)
        print("removeTag() f_dirtyTagString\t\t", f_dirtyTagString)
        f_cleanTagList = dirtyStr2cleanList(f_dirtyTagString)
        print("removeTag() f_cleanTagList\t\t", f_cleanTagList)
        if p_tag not in f_cleanTagList:
            raise Exception(
                'The file \'{}\' does not contain the tag \'{}\' \n This operation cannot be performed'.format(
                    p_filename, p_tag))
        f_cleanTagList.remove(p_tag)
        f_dirtyTagString2 = cleanList2dirtyStr(f_cleanTagList)
        print("removeTag() f_dirtyTagString2\t\t", f_dirtyTagString2)
        f_value = pyexiv2.utils.string_to_undefined(f_dirtyTagString2)
        f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
        f_metadata.write()
        return True
    else:
        # TODO add png and gif support
        # TODO error check: does this file have tag data?
        return True
    return False


# -------edit description metadata

def containsDescr(p_filename):
	"""This will tell us if the file
	has any description metadata.
	Returns bool"""
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    if ((p_filename[-4:] == '.jpg') and ('Exif.Image.XPComment' in f_metadata.exif_keys)):
        # print("this file already has description data")
        return True
    # print("this file has no description data")
    return False


def getDescr(p_filename):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def setDescr(p_filename, x):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return
	

def searchDescr(p_filename, x):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def addDescr(p_filename, x):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def removeDescr(p_filename):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


# ------edit rating metadata

def containsRating(p_filename):
	"""This will tell us if the file
	has any rating metadata.
	Returns bool"""
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    if ((p_filename[-4:] == '.jpg') and ('Exif.Image.Rating' in f_metadata.exif_keys)):
        # print("this file already has rating data")
        return True
    # print("this file has no rating data")
    return False


def getRating(p_filename):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def setRating(p_filename, x):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def searchRating(p_filename, x):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return



# ------edit metadata that can store source url

def containsSrc(p_filename):
	"""This will tell us if the file
	has any source url metadata.
	Returns bool"""
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    if ((p_filename[-4:] == '.jpg') and ('Exif.Image.ImageHistory' in f_metadata.exif_keys)):
        # print("this file already has history/source data")
        return True
    # print("this file has no history/source data")
    return False


def getSrc(p_filename):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def addSrc(p_filename, x):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def searchSrc(p_filename, x):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return



# -------edit orginal date

def containsOrgDate(p_filename):
	"""This will tell us if the file
	has any original date metadata.
	Returns bool"""
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    # TODO add png support
    if ((p_filename[-4:] == '.jpg') and ('Exif.Image.DateTimeOriginal' in f_metadata.exif_keys)):
        # print("this file already has original date data")
        return True
    # print("this file has no original date data")
    return False


def getOrgDate(p_filename):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def setOrgDate(p_filename, x):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return


def searchOrgDate(p_filename, x):
    if len(p_filename) < 5:
        raise Exception('Filename \'{}\' is too short to have any accepted filename extension'.format(p_filename))
    if p_filename[-4:] != '.jpg' and p_filename[-4:] != '.png':
        raise Exception(
            'Filename \'{}\' is not a supported filetype.\n Supported filetypes: jpg, png'.format(p_filename))
    # TODO
    return

