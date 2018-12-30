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
    print("exif:")
    for key in f_metadata.exif_keys:
        print("key:",key)
        keys.append(key)
    print("iptc:")
    for key in f_metadata.iptc_keys:
        print("key:",key)
        keys.append(key)
    print("xmp:")
    for key in f_metadata.xmp_keys:
        print("key:",key)
        keys.append(key)
    print()
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
"""
print()
g_newfile = testFileManager.singleClone(g_png1)
print(allKeys(g_newfile))
g_key1 = 'Xmp.xmpDM.Series/SeriesName'
g_key2 = 'Xmp.xmpDM.Series/SeriesIdentifier'
g_key = 'Xmp.xmpDM.Series'
g_metadata = pyexiv2.ImageMetadata(g_newfile)
g_metadata.read()
g_newvalue1 = "horse vacation"
g_newvalue2 = str(2)
g_metadata[g_key1] = pyexiv2.XmpTag(g_key1, g_newvalue1)
g_metadata[g_key2] = pyexiv2.XmpTag(g_key2, g_newvalue2)
g_metadata.write()
g_metadata.read()
print(g_metadata[g_key1])
print(type(g_metadata[g_key1]))
print(g_metadata[g_key2])
print(type(g_metadata[g_key2]))
print(type(g_metadata[g_key2].value))
print(allKeys(g_newfile))
testFileManager.singleRelease(g_newfile)

print()
g_newfile = testFileManager.singleClone(g_png1)
print(allKeys(g_newfile))
g_key = 'Xmp.xmpDM.Series'
g_metadata = pyexiv2.ImageMetadata(g_newfile)
g_metadata.read()
g_newvalue = "horse vacation"
g_metadata[g_key] = pyexiv2.XmpTag(g_key, g_newvalue)
g_metadata.write()
g_metadata.read()
print(g_metadata[g_key])
print(type(g_metadata[g_key]))
print(type(g_metadata[g_key].value))
print(allKeys(g_newfile))
testFileManager.singleRelease(g_newfile)
"""


"""
print()
g_newfile = testFileManager.singleClone(g_png1)
print(allKeys(g_newfile))
g_key1 = 'Xmp.xmpDM.Series[1]/Iptc4xmpExt:SeriesName'
g_key2 = 'Xmp.xmpDM.Series[1]/Iptc4xmpExt:SeriesIdentifier'
g_key = 'Xmp.xmpDM.Series'
g_metadata = pyexiv2.ImageMetadata(g_newfile)
g_metadata.read()
g_newvalue1 = "horse vacation"
g_newvalue2 = str(2)
g_metadata[g_key1] = pyexiv2.XmpTag(g_key1, g_newvalue1)
g_metadata[g_key2] = pyexiv2.XmpTag(g_key2, g_newvalue2)
g_metadata.write()
g_metadata.read()
print(g_metadata[g_key1])
print(type(g_metadata[g_key1]))
print(g_metadata[g_key2])
print(type(g_metadata[g_key2]))
print(type(g_metadata[g_key2].value))
print(allKeys(g_newfile))
testFileManager.singleRelease(g_newfile)
#this didn't work.
"""

print()
g_newfile = testFileManager.singleClone(g_png1)
print(allKeys(g_newfile))
#g_key = 'Xmp.iptcExt.AboutCvTerm'                       #kinda works
#g_key = 'Xmp.iptcExt.AboutCvTerm[1]/Iptc4xmpExt:CvId'  #error
#g_key = 'Xmp.iptcExt.AboutCvTerm[1]/Iptc4xmpExt:CvId'
#g_key = 'Xmp.xmpDM.videoFrameSize/stDim:w'             #totally works
#g_key = 'Xmp.xmpDM.videoFrameSize'                     #NotImplementedError: XMP conversion for type [Dimensions]
g_key = 'Xmp.iptcExt.Series'                           #kinda works
#g_key = 'Xmp.iptcExt.Series/Iptc4xmpExt:Name'           #error. tag not set
#g_key = 'Xmp.iptcExt.Series[1]'                         #error tag not set
g_key = 'Xmp.iptcExt.Series.Iptc4xmpExt'                #kinda works
g_key = 'Xmp.iptcExt.Series.Iptc4xmpExt:Name'           #error tag not set
g_key = 'Xmp.iptcExt.Series:Name'                       #error tag not set
g_key = 'Xmp.iptcExt.Series.Name'                       #kinda works
g_key = 'Xmp.iptcExt.Series.Identifier'
pyexiv2.xmp.register_namespace('mdEditorName/', 'taggerMark')
#pyexiv2.xmp.register_namespace('mdEditorVersion/', 'taggerMark') #causes error. we don't need to register second time
g_key = 'Xmp.taggerMark.mdEditorName'
g_key = 'Xmp.taggerMark.mdEditorVersion'
#g_key = 'Xmp.iptcExt.Series/Name'                       #error tag not set
#g_key = 'Xmp.iptcExt.Series.cheese'                     #kinda works
g_metadata = pyexiv2.ImageMetadata(g_newfile)
g_metadata.read()
#g_newvalue = "horse vacation"
g_newvalue = '7'
g_metadata[g_key] = pyexiv2.XmpTag(g_key, g_newvalue)

g_metadata.write()
g_metadata = pyexiv2.ImageMetadata(g_newfile)
g_metadata.read()
print("g_metadata[g_key]",g_metadata[g_key])
print(g_metadata[g_key].value)
print(type(g_metadata[g_key]))
print(type(g_metadata[g_key].value))
print(allKeys(g_newfile))

g_newfile2 = testFileManager.singleClone(g_newfile)
g_metadata = pyexiv2.ImageMetadata(g_newfile2)
g_metadata.read()
print("g_metadata[g_key]",g_metadata[g_key])
print(g_metadata[g_key].value)
print(type(g_metadata[g_key]))
print(type(g_metadata[g_key].value))
print(allKeys(g_newfile))
testFileManager.singleRelease(g_newfile2)
testFileManager.singleRelease(g_newfile)





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
g_key = 'Exif.Image.ImageDescription'
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

def pngSetSeries(p_filename, p_seriesName, p_num):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_metadata['Xmp.xmpDM.Series/SeriesName'] = p_seriesName
    f_metadata['Xmp.xmpDM.Series/SeriesIdentifier'] = str(p_num)
    f_metadata.write()
    return

def pngGetSeries(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_value1 = f_metadata['Xmp.xmpDM.Series/SeriesName'].value
    f_value2 = int(f_metadata['Xmp.xmpDM.Series/SeriesIdentifier'].value)
    return (f_value1, f_value2)
