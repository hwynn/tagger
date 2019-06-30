#!/usr/bin/env python3
"""
This is Level 2 MetadataManager functions.
These rely on Level 1 and 2 Metadata functions.
These functions are to be tested seperately.
These ae the functions the application calls.
"""
import MetadataManagerL1, MetadataManagerL0
import datetime

# ----- title
def containsTitle(p_filename):
    """!
    This will tell us if the file
    has any title metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :return: True if file has title metadata
    :rtype: bool
    """
    try:
        return MetadataManagerL0.containsTitle(p_filename)
    except Exception as e:
        print("MetadataManager2.containsTitle() error: ", e)
        return False
def getTitle(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :return: title if it exists. Else, ""
    :rtype: string
    """
    try:
        return MetadataManagerL0.getTitle(p_filename)
    except Exception as e:
        print("MetadataManager2.getTitle() error: ", e)
        return ""
def setTitle(p_filename, p_setTitleToThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_setTitleToThis: title we will store as title metadata
	:type p_setTitleToThis: string

	:return: True if operation was successful
    :rtype: bool
    """
    if p_setTitleToThis == "":
        try:
            MetadataManagerL0.wipeTitle(p_filename)
        except Exception as e:
            print("MetadataManager2.setTitle() error: ", e)
            return False
    else:
        try:
            MetadataManagerL0.setTitle(p_filename, p_setTitleToThis)
        except Exception as e:
            print("MetadataManager2.setTitle() error: ", e)
            return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.setTitle() Mark error: ", e)
        return False

# ----- artist
def containsArtists(p_filename):
    """!
    This will tell us if the file
    has any artist metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :return: True if file has artist metadata
    :rtype: bool
    """
    try:
        return MetadataManagerL0.containsArtists(p_filename)
    except Exception as e:
        print("MetadataManager2.containsArtists() error: ", e)
        return False
def getArtists(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :return: list of artists if it exists. Else, []
    :rtype: list<string>
    """
    try:
        return MetadataManagerL0.getArtists(p_filename)
    except Exception as e:
        print("MetadataManager2.getArtists() error: ", e)
        return []
def addArtist(p_filename, p_artist):
    """
    appends new artist to the artist metadata
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_artist: artist we are adding into the artist metadata
	:type p_artist: string

	:return: True if operation was successful
    :rtype: bool
    """
    try:
        MetadataManagerL1.addArtist(p_filename, p_artist)
    except Exception as e:
        print("MetadataManager2.addArtist() error: ", e)
        return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.addArtist() Mark error: ", e)
        return True
def removeArtist(p_filename, p_artist):
    """
    removes artist from artist metadata

    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_artist: artist we are removing from the artist metadata
	:type p_artist: string

	:return: True if operation was successful
    :rtype: bool
    """
    try:
        MetadataManagerL1.removeArtist(p_filename, p_artist)
    except Exception as e:
        print("MetadataManager2.removeArtist() error: ", e)
        return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.removeArtist() Mark error: ", e)
        return True

# ----- tag
def containsTags(p_filename):
    """!
    This will tell us if the file
    has any tag metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :return: True if file has tag metadata
    :rtype: bool
    """
    try:
        return MetadataManagerL0.containsTags(p_filename)
    except Exception as e:
        print("MetadataManager2.containsTags() error: ", e)
        return False
def getTags(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :return: list of tags if it exists. Else, []
    :rtype: list<string>
    """
    try:
        return MetadataManagerL0.getTags(p_filename)
    except Exception as e:
        print("MetadataManager2.getTags() error: ", e)
        return []
def addTag(p_filename, p_tag):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_tag: tag you will be adding to the tag metadata
	:type p_tag: string

	:return: True if operation was successful
    :rtype: bool
    """
    try:
        MetadataManagerL1.addTag(p_filename, p_tag)
    except Exception as e:
        print("MetadataManager2.addTag() error: ", e)
        return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.addTag() Mark error: ", e)
        return True
def removeTag(p_filename, p_tag):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_tag: tag you will be removing from the tag metadata
	:type p_tag: string

	:return: True if operation was successful
    :rtype: bool
    """
    try:
        MetadataManagerL1.removeTag(p_filename, p_tag)
    except Exception as e:
        print("MetadataManager2.removeTag() error: ", e)
        return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.removeTag() Mark error: ", e)
        return True

# ----- description
def containsDescr(p_filename):
    """!
    This will tell us if the file
    has any Description metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :return: True if file has description metadata
    :rtype: bool
    """
    try:
        return MetadataManagerL0.containsDescr(p_filename)
    except Exception as e:
        print("MetadataManager2.containsDescr() error: ", e)
        return False
def getDescr(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :return: description if it exists. Else, ""
    :rtype: string
    """
    try:
        return MetadataManagerL0.getDescr(p_filename)
    except Exception as e:
        print("MetadataManager2.getDescr() error: ", e)
        return ""
def setDescr(p_filename, p_setDescrToThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_setDescrToThis: description metadata will be set to this
	:type p_setDescrToThis: string

	:return: True if operation was successful
    :rtype: bool
    """
    if p_setDescrToThis == "":
        try:
            MetadataManagerL0.wipeDescr(p_filename)
        except Exception as e:
            print("MetadataManager2.setDescr() error: ", e)
            return False
    else:
        try:
            MetadataManagerL0.setDescr(p_filename, p_setDescrToThis)
        except Exception as e:
            print("MetadataManager2.setDescr() error: ", e)
            return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.setDescr() Mark error: ", e)
        return False
def addDescr(p_filename, p_addThisToDescr):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_addThisToDescr: string you will be appending to the description metadata
	:type p_addThisToDescr: string

	:return: True if operation was successful
    :rtype: bool
    """
    try:
        MetadataManagerL1.addDescr(p_filename, p_addThisToDescr)
    except Exception as e:
        print("MetadataManager2.addDescr() error: ", e)
        return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.addDescr() Mark error: ", e)
        return True

# ----- rating
def containsRating(p_filename):
    """!
    This will tell us if the file
    has any rating metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :return: True if file has rating metadata
    :rtype: bool
    """
    try:
        return MetadataManagerL0.containsRating(p_filename)
    except Exception as e:
        print("MetadataManager2.containsRating() error: ", e)
        return False
def getRating(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :return: rating if it exists. Else, -1
    :rtype: int
    """
    try:
        return MetadataManagerL0.getRating(p_filename)
    except Exception as e:
        print("MetadataManager2.getRating() error: ", e)
        return -1
def setRating(p_filename, p_setRatingToThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_setRatingToThis: rating metadata will be set to this
	:type p_setRatingToThis: int

	:return: True if operation was successful
    :rtype: bool
    """
    try:
        MetadataManagerL0.setRating(p_filename, p_setRatingToThis)
    except Exception as e:
        print("MetadataManager2.setRating() error: ", e)
        return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.setRating() Mark error: ", e)
        return True
def wipeRating(p_filename):
    """
    removes rating metadata from a file completely
    :param p_filename: name/path of the file
	:type p_filename: string

	:return: True if operation was successful
    :rtype: bool
    """
    try:
        MetadataManagerL0.wipeRating(p_filename)
    except Exception as e:
        print("MetadataManager2.wipeRating() error: ", e)
        return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.wipeRating() Mark error: ", e)
        return True

# ----- source url
def containsSource(p_filename):
    """!
    This will tell us if the file
    has any Source URL metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :return: True if file has source metadata
    :rtype: bool
    """
    try:
        return MetadataManagerL0.containsSource(p_filename)
    except Exception as e:
        print("MetadataManager2.containsSource() error: ", e)
        return False
def getSource(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :return: source url if it exists. Else, ""
    :rtype: string
    """
    try:
        return MetadataManagerL0.getSource(p_filename)
    except Exception as e:
        print("MetadataManager2.getSource() error: ", e)
        return ""
def setSource(p_filename, p_setSourceToThis):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_setSourceToThis: source url metadata will be set to this
	:type p_setSourceToThis: string

	:return: True if operation was successful
    :rtype: bool
    """
    if p_setSourceToThis == "":
        try:
            MetadataManagerL0.wipeSource(p_filename)
        except Exception as e:
            print("MetadataManager2.setSource() error: ", e)
            return False
    else:
        try:
            MetadataManagerL0.setSource(p_filename, p_setSourceToThis)
        except Exception as e:
            print("MetadataManager2.setSource() error: ", e)
            return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.setSource() Mark error: ", e)
        return False

# ----- orginal date
def containsOrgDate(p_filename):
    """!
    This will tell us if the file
    has any original date metadata.

    :param p_filename: name/path of the file
    :type p_filename: string

    :return: True if file has original date metadata
    :rtype: bool
    """
    try:
        return MetadataManagerL0.containsOrgDate(p_filename)
    except Exception as e:
        print("MetadataManager2.containsOrgDate() error: ", e)
        return False
def getOrgDate(p_filename):
    """
    if none exists, returns datetime.datetime(1, 1, 1)
    please don't use this as a magic number. It's just to keep consistent types
    since set and get should have the same requirements to work.
    :param p_filename: name/path of the file
    :type p_filename: string

    :return: original data if it exists. Else, datetime.datetime(1,1,1)
    :rtype: datetime
    """
    try:
        return MetadataManagerL0.getOrgDate(p_filename)
    except Exception as e:
        print("MetadataManager2.getOrgDate() error: ", e)
        return datetime.datetime(1, 1, 1)
def setOrgDate(p_filename, p_date):
    """:param p_filename: name/path of the file
	:type p_filename: string
	:param p_date: original date metadata will be set to this
	:type p_date: datetime

	:return: True if operation was successful
    :rtype: bool
    """
    try:
        MetadataManagerL0.setOrgDate(p_filename, p_date)
    except Exception as e:
        print("MetadataManager2.setOrgDate() error: ", e)
        return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.setOrgDate() Mark error: ", e)
        return True

# ----- series
def containsSeries(p_filename):
    """!
    This will tell us if the file
    has Series metadata.
    It must contain a series name and a series installent

    :param p_filename: name/path of the file
    :type p_filename: string

    :return: True if file has series name and series installment metadata
    :rtype: bool
    """
    try:
        return MetadataManagerL0.containsSeriesName(p_filename) \
               and MetadataManagerL0.containsSeriesInstallment(p_filename)
    except Exception as e:
        print("MetadataManager2.containsSeries() error: ", e)
        return False
def getSeries(p_filename):
    """!
    :param p_filename: name/path of the file
    :type p_filename: string

    :return: series if it exists. Else, ("", -1)
    :rtype: tuple (string, int)
    """
    try:
        f_seriesName = MetadataManagerL0.getSeriesName(p_filename)
        f_seriesInstallment = MetadataManagerL0.getSeriesInstallment(p_filename)
        return (f_seriesName, f_seriesInstallment)
    except Exception as e:
        print("MetadataManager2.getSeries() error: ", e)
        return ("", -1)
def setSeries(p_filename, p_name, p_ins):
    """
    :param p_filename: name/path of the file
	:type p_filename: string
	:param p_name: series name metadata will be set to this
	:type p_name: string
	:param p_ins: series installment metadata will be set to this
	:type p_ins: int

	:return: True if operation was successful
    :rtype: bool
    """
    try:
        MetadataManagerL1.setSeries(p_filename, p_name, p_ins)
    except Exception as e:
        print("MetadataManager2.setSeries() error: ", e)
        return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.setSeries() Mark error: ", e)
        return True
def wipeSeries(p_filename):
    """
    :param p_filename: name/path of the file
    :type p_filename: string

	:return: True if operation was successful
    :rtype: bool
    """
    try:
        MetadataManagerL1.wipeSeries(p_filename)
    except Exception as e:
        print("MetadataManager2.wipeSeries() error: ", e)
        return False
    try:
        MetadataManagerL1.placeMark(p_filename)
        return True
    except Exception as e:
        print("MetadataManager2.wipeSeries() Mark error: ", e)
        return True
