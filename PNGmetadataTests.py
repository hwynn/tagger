#!/usr/bin/env python3
import pyexiv2
import MetadataManager
import TestingManager

def pngSetSubject(p_filename, p_list):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.dc.subject'
    f_value = p_list
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetSubject(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.dc.subject'
    return f_metadata[f_key].value
def pngSetCaption(p_filename, p_string):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.acdsee.Caption'
    f_value = p_string
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetCaption(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.acdsee.Caption'
    return f_metadata[f_key].value










def pngSetTitle(p_filename, p_string):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.dc.title'
    f_value = p_string
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetTitle(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.dc.title'
    return f_metadata[f_key].value['x-default']



def pngSetDescription(p_filename, p_string):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.dc.description'
    f_value = p_string
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetDescription(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.dc.description'
    return f_metadata[f_key].value['x-default']
def pngSetCreator(p_filename, p_list):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.dc.creator'
    f_value = p_list
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetCreator(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.dc.creator'
    return f_metadata[f_key].value
def pngSetRating(p_filename, p_num):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.xmp.Rating'
    f_value = p_num
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetRating(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.xmp.Rating'
    return f_metadata[f_key].value
def pngSetKeywords(p_filename, p_list):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.xmp.Label'
    f_value = MetadataManager.cleanList2cleanStr(p_list)
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetKeywords(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = 'Xmp.xmp.Label'
    return f_metadata[f_key].value



"""
Title
+'Xmp.dc.title'
Artist
+'Xmp.dc.creator'
Tags
+'Xmp.xmp.Label'
Description
+'Xmp.dc.description'
Rating
+'Xmp.xmp.Rating'
SourceURL
+Xmp.iptcExt.ArtworkSourceInvURL
+Xmp.xmp.BaseURL
metadataEditHistory
+Xmp.xmp.MetadataDate
+Xmp.xmp.CreatorTool
Original Date created
+Xmp.iptcExt.ArtworkDateCreated
series info:
    name of series
    +'Xmp.xmpDM.Series/SeriesName'
    number in series
    +'Xmp.xmpDM.Series/SeriesIdentifier'

Xmp.iptcExt.ExternalMetadataLink ??
"""
