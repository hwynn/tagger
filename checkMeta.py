#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import pyexiv2
import ByteString


detailedData = pyexiv2.ImageMetadata('/home/hwynn/Pictures/CatInBox2.jpg')

print(detailedData.read()) #works
print("test1")
print(detailedData.exif_keys)
#print("Exif.Image.XPKeywords") #works
#print(type(detailedData['Exif.Image.XPKeywords'])) #works
#print(detailedData['Exif.Image.XPKeywords']) #works
keywords = detailedData['Exif.Image.XPKeywords'];
#print(keywords.value) #works

checkthis = detailedData['Exif.Image.XPComment'];
print(pyexiv2.utils.undefined_to_string(checkthis.value))
print()
#pyexiv2.utils.undefined_to_string((keywords.value).encode('utf-16'))
#pyexiv2.utils.string_to_undefined((keywords.value).encode('utf-16'))
#print(type(pyexiv2.utils.undefined_to_string(keywords.value))) #works
print(pyexiv2.utils.undefined_to_string(keywords.value)) #works
print(type(b'cute'))
print(b'cute')
print(type(bytes("cute", 'utf-16')))
print(bytes("cute", 'utf-16'))
print(chr(0))
#data = bytes(b'cute')
#print(type(data))
#print(type(bytesprefix'cute')))
#print(type(shortbytes'cute'))

key = 'Exif.Image.XPKeywords'
value = ByteString.freshExifTags(keywords,'cute')
detailedData[key] = pyexiv2.ExifTag(key, value)

#detailedData['Exif.Image.XPComment'] = pyexiv2.ExifTag('Exif.Image.XPComment', value)
detailedData.write()
keywords = detailedData['Exif.Image.XPKeywords'];
value = ByteString.removeExifTag(keywords,'cute')
detailedData[key] = pyexiv2.ExifTag(key, value)
detailedData.write()

#newKeywords = ByteString.freshExifTags(keywords,'cute')



#detailedData['Exif.Image.XPKeywords'] = newKeywords;
#detailedData.write()
detailedData = pyexiv2.ImageMetadata('/home/hwynn/Pictures/CatInBox2.jpg')
detailedData.read()
keywords = detailedData['Exif.Image.XPKeywords'];
key = 'Exif.Image.XPKeywords'
value = ByteString.freshExifTags(keywords,'cute')

def addExifTag(keywords, p_tag):
    """takes an ExifTag object and a string with a tag.
    Returns a new ExifTag object with the new tag added to it."""
    f_bustedTagString = pyexiv2.utils.undefined_to_string(keywords.value)
    #print("freshExifTags. file has these tags:", stringHexTrim(f_bl))
    if p_tag in ByteString.stringHexTrim(f_bustedTagString):
        print("This file already has the tag \"", p_tag ,"\"", sep='')
        value = keywords.value
        #or we could just exit the function here
    f_newTagString = ByteString.stringHexify(p_tag) + ";\x00" + f_bustedTagString
    #print("freshExifTags. file will now have these tags:", stringHexTrim(f_newTagString))
    value = pyexiv2.utils.string_to_undefined(f_newTagString)


detailedData[key] = pyexiv2.ExifTag(key, value)
detailedData.write()
#print("\x00") #prints rectangel
print()
#pyexiv2.utils.string_to_undefined((keywords.value))
#pyexiv2.utils.string_to_undefined(value.encode('utf-16')) #nope
#pyexiv2.utils.string_to_undefined(value) #nope
#pyexiv2.utils.undefined_to_string(value)

