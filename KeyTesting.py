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

g_metadataTypes = ['Title', 'Description', 'Rating', 'Tags', 'Artist', 'Date Created']

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
g_gif1 = "/media/sf_tagger/windowstesting/pikachus.gif"

emptyXMLkey = 'Exif.Image.XMLPacket'
"""
#starting generic file set testing. 
g_newfilel = testFileManager.shadowClones(g_png1, 1)
testFileManager.jutsu(g_png1, g_newfilel)  # this actually makes the new files
g_newfile = g_newfilel[0]
print(allKeys(g_png1))
print(allKeys(g_newfile))
print(g_newfilel)
print()
"""


#possible errors:
#KeyError: "No namespace info available for XMP prefix `iTXt'"


g_understoodkeys = ['Xmp.xmp.CreateDate']
g_useablekeys =['Xmp.xmp.Label','Xmp.xmp.MetadataDate','Xmp.xmp.BaseURL','Xmp.xmp.Rating',
                'Xmp.xmp.Disclaimer','Xmp.xmp.Author','Xmp.xmp.Collection','Xmp.xmp.Comment',
                'Xmp.xmp.CreationTime','Xmp.xmp.Description','Xmp.xmp.PNGWarning','Xmp.xmp.Source', 'Xmp.xmp.Title',
                'Exif.Image.ImageDescription']

"""
#the actual generic testing
#Exif data tags seem to work for some reason...
#g_key = 'Xmp.xmp.CreateDate'
#g_key = 'Xmp.xmp.Title'
g_key= 'Exif.Image.ImageDescription'
#test setting, retrieving, and using g_key
g_metadata = pyexiv2.ImageMetadata(g_newfile)
g_metadata.read()
#g_newvalue = datetime.datetime(2017, 3, 6, 11, 34, 5)
g_newvalue = "Johny Boy"
#g_newvalue = "https://sno.phy.queensu.ca/~phil/exiftool/TagNames/XMP.html"
#g_newvalue = 2
#g_metadata[g_key] = pyexiv2.XmpTag(g_key, g_newvalue)
g_metadata[g_key] = pyexiv2.ExifTag(g_key, g_newvalue)
g_metadata.write()
g_metadata.read()
print()
print(g_metadata[g_key])
print(type(g_metadata[g_key]))
print()
g_rawdate = g_metadata[g_key].raw_value

print("g_rawdate:",g_rawdate)
print(type(g_rawdate))
print(allKeys(g_newfile))
#g_parsedVal= MetadataManager.Iso8601_to_date(g_rawdate)
#print(g_parsedVal)
#print(type(g_parsedVal))

#g_unparsedVal= MetadataManager.valTranslateNone(g_parsedVal)
#print(g_unparsedVal)
#print(type(g_unparsedVal))
"""

#finish generic testing
#testFileManager.release(g_newfilel)

#g_result1 = testFileManager.isThisLikeJpeg(g_fulljpg, g_gif1, "Title")
#Note: writing to GIF files is commpletely unsupported by my API.
# I get this error:   self._image._writeMetadata()
#                   OSError: Writing to GIF images is not supported
# Not sure why yet.



