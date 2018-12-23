#!/usr/bin/env python3
import pyexiv2
import MetadataManager
import testFileManager
import dateutil.parser
import datetime
"""
This is a place to test individual keys
Reading and writing values in certain files
"""

def allKeys(p_file_1):
    #prints all keys from file
    keys = []
    f_metadata = pyexiv2.ImageMetadata(p_file_1)
    f_metadata.read()
    #print("exif:")
    for key in f_metadata.exif_keys:
        #print("key:",key)
        keys.append(key)
    #print("iptc:")
    for key in f_metadata.iptc_keys:
        #print("key:",key)
        keys.append(key)
    #print("xmp:")
    for key in f_metadata.xmp_keys:
        #print("key:",key)
        keys.append(key)
    #print()
    return keys

def Iso86012date(p_isodate):
    """
    :param p_isodate: the date in ISO 8601 string format
    :type p_isodate: string

    :return: a date
    :rtype: datetime object
    """
    f_parsedDate = dateutil.parser.parse(p_isodate)
    return f_parsedDate
def date2Iso8601(p_date):
    """
    :param p_date: a date
    :type p_date: datetime object

    :return: the date in ISO 8601 string format
    :rtype: string
    """
    f_unparsedDate = p_date.isoformat()
    return f_unparsedDate


g_emptyjpg = "/media/sf_tagger/windowstesting/skull.jpg"
g_fulljpg = "/media/sf_tagger/windowstesting/skullA.jpg"

xmpErrorKeys = ['Xmp.MicrosoftPhoto.DateAcquired', 'Xmp.xmp.CreateDate']

emptyXMLkey = 'Exif.Image.XMLPacket'

g_newfilel = testFileManager.shadowClones(g_emptyjpg, 1)
testFileManager.jutsu(g_emptyjpg, g_newfilel)  # this actually makes the new files
g_newfile = g_newfilel[0]
print(allKeys(g_fulljpg))
print(allKeys(g_newfile))
print(g_newfilel)
print()

g_metadata = pyexiv2.ImageMetadata(g_fulljpg)
g_metadata.read()
print(g_metadata['Exif.Image.Rating'].value)
print(g_metadata['Xmp.dc.title'].value)
print(type(g_metadata['Xmp.dc.title']))
print(g_metadata['Xmp.dc.title'])
print(g_metadata['Xmp.xmp.CreateDate'])
print(type(g_metadata['Xmp.xmp.CreateDate']))
print(g_metadata['Xmp.xmp.CreateDate'].raw_value)
g_rawdate = g_metadata['Xmp.xmp.CreateDate'].raw_value
#https://codeyarns.com/2017/10/12/how-to-convert-datetime-to-and-from-iso-8601-string/
print(g_rawdate)
print(type(g_rawdate))


g_parsedDate = Iso86012date(g_rawdate)
print(g_parsedDate)
print(type(g_parsedDate))


g_unparsedDate = date2Iso8601(g_parsedDate)
print(g_unparsedDate)
print(type(g_unparsedDate))

g_newvalue = datetime.datetime(2017, 3, 6, 11, 34, 5)
print(g_newvalue)




testFileManager.release(g_newfilel)

#f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
#metadata[key] = pyexiv2.XmpTag(key, value)