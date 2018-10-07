#!/usr/bin/env python3


# -------stashing utility functions
"""Note: 'stashing' is a term I made up
which refers to storing several types of
metadata into a single large string.
This should let us store a variety of
metadata in file types that only have
a few metadata tags"""


def containsStash(p_filename):
    """
    TODO
    :param p_filename: name/path of the file
	:type p_filename: string
	:return: True if we have added a stash string
	:rtype: bool
    """
    return


def getStashIndex(p_filename):
    """
    assuming containsStash() is true
    returns a list of the metadata
    similar to: metadata.exif_keys
    TODO
    """
    return


def searchStashIndex(p_filename, p_key):
    """
    assuming containsStash() is true
    this function checks whether or not
    a type of metadata is present in
    the stash index and the stash string
    returns bool

    :return: true if p_key is in the metadata
    :rtype: bool
    """
    return


def addItemToStashIndex(p_filename, p_key):
    """
    assuming searchStashIndex() returns false
    this function adds a new kind of metadata
    to the stash string. Only certain values of p_key
    are allowed to keep metadata consistent across filetypes
    this also adds a blank metadata entry to the stash string
    TODO
    """
    return


def removeItemFromStashIndex(p_filename, p_key):
    """
    assuming searchStashIndex() returns true
    this function removes a type of metadata
    from the stash string and the stash index
    TODO
    """
    return


def setStashData(p_filename, p_key, p_value):
    """
    assuming searchStashIndex() returns true
    this function stores data of a given type
    into the appropriate place in the stash string
    note: this will completely rewrite a type of stash data
    there is no addStashData function. That must be done
    by the individual metadata functions
    TODO
    """
    return


def getStashData(p_filename, p_key):
    """
    assuming searchStashIndex() returns true
    this function returns the value of the given
    metadata type as a string.
    the individual metadata functions
    are responsible for parsing this string
    TODO
    """
    return

