#!/usr/bin/env python3
import pyexiv2
import MetadataManager


key5 = 'Xmp.dc.title'
key6 = 'Xmp.dc.description'
key7 = 'Xmp.dc.creator'
key8 = 'Xmp.dc.subject'
#despite warnings to avoid the following tags. I'm going to use them anyways
key9 = 'Xmp.acdsee.Caption'
key10 = 'Xmp.xmp.Rating'
key11 = 'Xmp.xmp.Keywords'


def pngSetTitle(p_filename, p_string):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key5
    f_value = p_string
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetTitle(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key5
    return f_metadata[key5].value['x-default']
def pngSetDescription(p_filename, p_string):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key6
    f_value = p_string
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetDescription(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key6
    return f_metadata[key6].value['x-default']
def pngSetCreator(p_filename, p_list):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key7
    f_value = p_list
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetCreator(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key7
    return f_metadata[key7].value
def pngSetSubject(p_filename, p_list):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key8
    f_value = p_list
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetSubject(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key8
    return f_metadata[key8].value
def pngSetCaption(p_filename, p_string):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key9
    f_value = p_string
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetCaption(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key9
    return f_metadata[key9].value
def pngSetRating(p_filename, p_num):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key10
    f_value = p_num
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetRating(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key10
    return f_metadata[key10].value
def pngSetKeywords(p_filename, p_list):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key11
    f_value = MetadataManager.cleanList2cleanStr(p_list)
    f_metadata[f_key] = pyexiv2.XmpTag(f_key, f_value)
    f_metadata.write()
    return
def pngGetKeywords(p_filename):
    f_metadata = pyexiv2.ImageMetadata(p_filename)
    f_metadata.read()
    f_key = key11
    return f_metadata[key11].value
