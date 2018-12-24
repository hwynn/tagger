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


g_emptyjpg = "/media/sf_tagger/windowstesting/skull.jpg"
g_fulljpg = "/media/sf_tagger/windowstesting/skullA.jpg"
g_png1 = "/media/sf_tagger/windowstesting/dan1.png"

emptyXMLkey = 'Exif.Image.XMLPacket'

g_newfilel = testFileManager.shadowClones(g_png1, 1)
testFileManager.jutsu(g_png1, g_newfilel)  # this actually makes the new files
g_newfile = g_newfilel[0]
print(allKeys(g_png1))
print(allKeys(g_newfile))
print(g_newfilel)
print()

g_key = 'Xmp.MicrosoftPhoto.DateAcquired'
#test setting, retrieving, and using g_key

g_metadata = pyexiv2.ImageMetadata(g_png1)
g_metadata.read()
g_newvalue = datetime.datetime(2017, 3, 6, 11, 34, 5)
g_metadata[g_key] = pyexiv2.XmpTag(g_key, g_newvalue)
g_metadata.write()
g_metadata.read()
print()
print(g_metadata[g_key])
print(type(g_metadata[g_key]))
print()
g_rawdate = g_metadata[g_key].raw_value

print(g_rawdate)
print(type(g_rawdate))

g_parsedVal= MetadataManager.Iso8601_to_date(g_rawdate)
print(g_parsedVal)
print(type(g_parsedVal))

g_unparsedVal= MetadataManager.valTranslateNone(g_parsedVal)
print(g_unparsedVal)
print(type(g_unparsedVal))




testFileManager.release(g_newfilel)

#f_metadata[f_key] = pyexiv2.ExifTag(f_key, f_value)
#metadata[key] = pyexiv2.XmpTag(key, value)