#!/usr/bin/env python3
import pyexiv2
import shutil
import os
from pathlib import PurePosixPath
from pathlib import PureWindowsPath
import MetadataManager
"""
This libraryhas functions that will allow us to easily
create and manage files for metadata testing
"""
def getExtension(p_filepathname):
    """!
    this function checks the type of the file.
    Used for png and gif

    :param p_filepathname: the path/name of the file
    :type p_filepathname: string

    :return: the file extension
    :rtype: string
    """
    if os.name == 'nt':
        # this filepath is from windows
        return PureWindowsPath(p_filepathname).suffix
    # assume posix otherwise
    return PurePosixPath(p_filepathname).suffix

def shadowClones(p_filename, p_howmany, p_mod=''):
    #creates several copies of a file if possible.
    ext = getExtension(p_filename)
    f_name = p_filename[:-len(ext)]
    f_newfiles = []
    for i in range(p_howmany):
        f_newfiles.append(f_name+str(i+1)+p_mod+ext)
    return f_newfiles

def jutsu(p_filename, p_files):
    for file in p_files:
        if os.path.isfile(file)==True:
            print("File already exists")
            return
    for file in p_files:
        shutil.copy(p_filename, file)

def release(p_files):
    for file in p_files:
        os.remove(file)

def missingKeys(p_file_1, p_file_2):
    #print("missing keys")
    #prints keys that are in file1, but not in file2
    f_metadata1 = pyexiv2.ImageMetadata(p_file_1)
    f_metadata1.read()
    f_metadata2 = pyexiv2.ImageMetadata(p_file_2)
    f_metadata2.read()
    missingkeys = []
    #print("exif:")
    for key1 in f_metadata1.exif_keys:
        if key1 not in f_metadata2.exif_keys:
            #print(key1)
            missingkeys.append(key1)
    #print("iptc:")
    for key1 in f_metadata1.iptc_keys:
        if key1 not in f_metadata2.iptc_keys:
            #print(key1)
            missingkeys.append(key1)
    #print("xmp:")
    for key1 in f_metadata1.xmp_keys:
        if key1 not in f_metadata2.xmp_keys:
            #print(key1)
            missingkeys.append(key1)
    return missingkeys

def allMeta(p_file_1):
    #prints all keys and associated values
    f_metadata = pyexiv2.ImageMetadata(p_file_1)
    f_metadata.read()
    print("exif:")
    for key in f_metadata.exif_keys:
        print("key:",key)
        #print(f_metadata[key])
        print(f_metadata[key].value)
    print("iptc:")
    for key in f_metadata.iptc_keys:
        print("key:",key)
        #print(f_metadata[key])
        print(f_metadata[key].value)
    print("xmp:")
    for key in f_metadata.xmp_keys:
        print("key:",key)
        #print(f_metadata[key])
        print(f_metadata[key].value)
    print()


g_mainfile = "/media/sf_tagger/windowstesting/skull.jpg"

g_files = shadowClones(g_mainfile, 5)
jutsu(g_mainfile,g_files)
print(g_files)

print(allMeta(g_mainfile))

for file in g_files:
    print()
    print(file)
    #print(missingKeys("/media/sf_tagger/windowstesting/skull.jpg",file))
    print(allMeta(file))

MetadataManager.setTitle(g_files[0], "whatme")

MetadataManager.setDescr(g_files[1], "I hate it when this happens\nI know")

MetadataManager.setRating(g_files[2], 4)

MetadataManager.setTags(g_files[3], ["cats","bones","hobbies"])

MetadataManager.setArtists(g_files[4], ["arnold", "clown: Bozo", "the pope"])


for file in g_files:
    print()
    print(file)
    #print(missingKeys("/media/sf_tagger/windowstesting/skull.jpg",file))
    print(allMeta(file))







release(g_files)