#!/usr/bin/env python3
"""
This library exists to partition MetadataManager functions.
This is Level 1 MetadataManager functions.
All functions in level 1 rely on functions in level 0.
These functions are to be tested seperately
"""
import pyexiv2
import datetime
import configManagement
from MetadataManagerL0 import filecheck, earlySupportCheck, MetadataMissingError, OutOfRangeError, NotIntegerError
from MetadataManagerL0 import getTitle, containsArtists, getArtists, setArtists, wipeArtists,\
    containsTags, getTags, setTags,  wipeTags, getDescr, setDescr, \
    getRating, getSource, getSeriesName, getExtension, containsOrgDate, getOrgDate, \
    getSeriesInstallment, containsMetadataDate, getMetadataDate, containsTaggerMark, getVersionNum, \
    wipeSeriesName, wipeSeriesInstallment, containsSeriesName, containsSeriesInstallment, setSeriesName, \
    setSeriesInstallment, setMetadataDate, setTaggerMark, setVersionNum


# ========================================================
# ---------------Defined exceptions-----------------------
# ========================================================
class NoSuchItemError(ValueError):
    """This is similar to MetadataMissing (it shows up in similar contexts)
    But it's raised when data is present, but the item we want to remove
    isn't present in the list"""
    pass
class DuplicateDataError(ValueError):
    """we raise this when we try to add a tag
    or something similar to a list and the list already has that item"""
    pass

# ========================================================
# ---------------MetaData functionality-------------------
# ========================================================

# ------edit title metadata
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
    f_title = getTitle(p_filename)
    if f_title == "":
        return False
    if p_searchForThis in f_title:
        return True
    return False

# ------edit artist metadata
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
    f_artists = getArtists(p_filename)
    if f_artists == []:
        return False
    # Note: the conditions for finding an artist are very relaxed.
    # We're only searching for a substring.
    # so if an artist entry is "composer: Sarah Sharp"
    # searches for: "composer", "Sarah Sharp", "Sarah", "sharp", and "Sar"
    # will all return true.
    # Perhaps a strictSearchArtists() function is needed
    for i_artist in f_artists:
        #print("finding artist:", p_artist.lower(), i_artist.lower())
        if p_artist.lower() in i_artist.lower():
            return True
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
    f_cleanXList = getArtists(p_filename)
    # print("addArtist() f_cleanXList\t\t", f_cleanXList)
    if p_artist in f_cleanXList:
        raise DuplicateDataError("file already contains this artist")
    f_cleanXList.insert(0, p_artist)
    setArtists(p_filename, f_cleanXList)
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
    if not containsArtists(p_filename):
        raise MetadataMissingError("there is no artist data to remove")
    f_cleanXList = getArtists(p_filename)
    # print("removeArtist() f_cleanXList\t\t", f_cleanXList)
    # Note that p_artist must be an exact match with an entry to have it removed
    if p_artist not in f_cleanXList:
        raise NoSuchItemError(
            'The file \'{}\' does not contain the artist \'{}\' \n This operation cannot be performed'.format(
                p_filename, p_artist))
    f_cleanXList.remove(p_artist)
    if f_cleanXList == []:
        wipeArtists(p_filename)
        return
    setArtists(p_filename, f_cleanXList)
    return

# -----edit tag metadata
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
    f_keywords = getTags(p_filename)
    # Note: these are strict searches. They are case sensative
    # non case sensative searches may require longer execution time
    if f_keywords == []:
        return False
    if p_tag in f_keywords:
        return True
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
    f_cleanXList = getTags(p_filename)
    # print("addTag() f_cleanXList\t\t", f_cleanXList)
    if p_tag in f_cleanXList:
        raise DuplicateDataError("file already contains this tag")
    f_cleanXList.insert(0, p_tag)
    setTags(p_filename, f_cleanXList)
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
    if not containsTags(p_filename):
        raise MetadataMissingError("there is no tag data to remove")
    f_cleanXList = getTags(p_filename)
    # print("addTag() f_cleanXList\t\t", f_cleanXList)
    if p_tag not in f_cleanXList:
        raise NoSuchItemError(
            'The file \'{}\' does not contain the tag \'{}\' \n This operation cannot be performed'.format(
                p_filename, p_tag))
    f_cleanXList.remove(p_tag)
    if f_cleanXList == []:
        wipeTags(p_filename)
        return
    # print("removeTag() f_cleanXList\t\t", f_cleanXList)
    setTags(p_filename, f_cleanXList)
    return

# -------edit description metadata
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
    f_descr = getDescr(p_filename)
    if f_descr == "":
        return False
    if p_searchForThis in f_descr:
        return True
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
    f_setDescrToThis = getDescr(p_filename) + p_addThisToDescr
    setDescr(p_filename, f_setDescrToThis)
    return

# ------edit rating metadata
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
        # we don't actually use getRating() for this search function
        # But we might change this function to work that way.
        raise OutOfRangeError('number out of range (must be 1..5)')
    if not isinstance(p_searchForThisRating, int):
        raise NotIntegerError('non-integers can not be used')
    f_rating = getRating(p_filename)
    if f_rating == -1:
        return False
    if f_rating ==p_searchForThisRating:
        return True
    return False


# ------edit metadata that can store source url
def searchSource(p_filename, p_searchForThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_searchForThis: source url that we're checking for
    :type p_searchForThis: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if p_searchForThis was in source metadata
    :rtype: bool
    """
    filecheck(p_filename)
    f_source = getSource(p_filename)
    if f_source == "":
        return False
    if p_searchForThis in f_source:
        return True
    return False


# -------edit orginal date
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

#------edit metadata that can store series information (like comic name and strip number)
def searchSeriesName(p_filename, p_searchForThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_searchForThis: series name that we're checking for
    :type p_searchForThis: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if p_searchForThis was in series name metadata
    :rtype: bool
    """
    filecheck(p_filename)
    f_series_name = getSeriesName(p_filename)
    if f_series_name == "":
        return False
    if p_searchForThis in f_series_name:
        return True
    return False
def searchSeriesInstallment(p_filename, p_searchForThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_searchForThis: series installment that we're checking for
    :type p_searchForThis: int

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if p_searchForThis was in series installment metadata
    :rtype: bool
    """
    filecheck(p_filename)
    f_series_installment = getSeriesInstallment(p_filename)
    if f_series_installment == -1:
        return False
    if p_searchForThis in f_series_installment:
        return True
    return False

def setSeries(p_filename, p_name, p_ins):
    setSeriesName(p_filename, p_name)
    setSeriesInstallment(p_filename, p_ins)

def wipeSeries(p_filename):
    if containsSeriesName(p_filename):
        wipeSeriesName(p_filename)
    if containsSeriesInstallment(p_filename):
        wipeSeriesInstallment(p_filename)

# -------edit metadata date
def searchMetadataDate(p_filename, p_startDate, p_endDate):
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
        if not containsMetadataDate(p_filename):
            return False
        f_cleanMetadataDate = getMetadataDate(p_filename)
        if p_startDate <= f_cleanMetadataDate <= p_endDate:
            return True
    else:
        earlySupportCheck(p_filename)
        # TODO add gif support
        return False
    return False


#----edit hidden software marks
def searchTaggerMark(p_filename, p_searchForThis):
    """
    takes: filename as string (including path)
    returns: truth value of p_searchForThis being in the TaggerMark
    always returns false when no TaggerMark exists

    # Note: TaggerMark does not need to be entire search term to return true
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_searchForThis: TaggerMark that we're checking for
    :type p_searchForThis: string

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if p_searchForThis was in TaggerMark metadata
    :rtype: bool
    """
    filecheck(p_filename)
    if containsTaggerMark(p_filename) == False:
        return False
    if p_searchForThis in containsTaggerMark(p_filename):
        return True
    return False
def searchVersionNum(p_filename, p_searchForThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_searchForThis: VersionNum that we're checking for
    :type p_searchForThis: int

    :raise UnknownFiletypeError: if the filetype cannot be found
    :raise UnsupportedFiletypeError: if the filetype is not .jpg, .png, or .gif

    :return: True if p_searchForThis was in VersionNum metadata
    :rtype: bool
    """
    filecheck(p_filename)
    f_VersionNum = getVersionNum(p_filename)
    if f_VersionNum == -1:
        return False
    if p_searchForThis in f_VersionNum:
        return True
    return False

def getCurrentVersion():
    """
    This returns the version number from the config manager
    :return: the version number
    :rtype: string
    """
    f_version = configManagement.currentVersion()
    return f_version

def placeMark(p_filename):
    """
    This should be used after every metadata edit.
    It gives a hidden mark to a file editted. This is so any edits
    will show that they were made with this software.
    The hidden mark contains the name of the software, the version
    of the software, and the date/time the edit was made.
    The software name is included to let us know what assumptions we can
    make about the metadata.
    Version number is included because metadata formatting might change
    between versions. Knowing which version was used to create an edit
    will inform us about what format specific assumptions we can make.
    Metadata edit date is included to distinguish which version of
    a file is more recent, since modification date theoretically
    won't change in an edit operation
    :param p_filename: name/path of the file
    :type p_filename: string
    """
    setTaggerMark(p_filename, configManagement.getSoftwareName())
    setVersionNum(p_filename, configManagement.currentVersion())
    setMetadataDate(p_filename, datetime.datetime.today())