import pyexiv2
import MetadataManager

#g_file_1 = "/media/sf_tagger/windowstesting/skull.jpg"
#g_file_2 = "/media/sf_tagger/windowstesting/skull1.jpg"
g_file_1 = "/media/sf_tagger/windowstesting/dan.png"
g_file_2 = "/media/sf_tagger/windowstesting/dan1.png"
#g_file_1 = "/media/sf_tagger/windowstesting/tiny.tiff"
#g_file_2 = "/media/sf_tagger/windowstesting/tiny1.tiff"




#control test
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



#modify test
def compAllVals(p_file_1, p_file_2):
    #Prints each key/value pair that differs between the two files
    #print("Value comparison")
    f_metadata1 = pyexiv2.ImageMetadata(p_file_1)
    f_metadata1.read()
    f_metadata2 = pyexiv2.ImageMetadata(p_file_2)
    f_metadata2.read()
    diffVals = []
    #print("exif:")
    for key1 in f_metadata1.exif_keys:
        if key1 in f_metadata2.exif_keys:
            if f_metadata1[key1].value!=f_metadata2[key1].value:
                #print(key1)
                #print(f_metadata1[key1].value)
                #print(f_metadata2[key1].value)
                diffVals.append((key1, f_metadata1[key1].value, f_metadata2[key1].value))
    #print("iptc:")
    for key1 in f_metadata1.iptc_keys:
        if key1 in f_metadata2.iptc_keys:
            if f_metadata1[key1].value!=f_metadata2[key1].value:
                #print(key1)
                #print(f_metadata1[key1].value)
                #print(f_metadata2[key1].value)
                diffVals.append((key1, f_metadata1[key1].value, f_metadata2[key1].value))
    #print("xmp:")
    for key1 in f_metadata1.xmp_keys:
        if key1 in f_metadata2.xmp_keys:
            if f_metadata1[key1].value!=f_metadata2[key1].value:
                #print(key1)
                #print(f_metadata1[key1].value)
                #print(f_metadata2[key1].value)
                diffVals.append((key1, f_metadata1[key1].value, f_metadata2[key1].value))
    return diffVals


# init keys test
def newKeys(p_file_1, p_file_2):
    #print("missing keys")
    #prints keys that are in file2, but not in file1
    f_metadata1 = pyexiv2.ImageMetadata(p_file_1)
    f_metadata1.read()
    f_metadata2 = pyexiv2.ImageMetadata(p_file_2)
    f_metadata2.read()
    newkeys = []
    #print("exif:")
    for key1 in f_metadata2.exif_keys:
        if key1 not in f_metadata1.exif_keys:
            #print(key1)
            newkeys.append(key1)
    #print("iptc:")
    for key1 in f_metadata2.iptc_keys:
        if key1 not in f_metadata1.iptc_keys:
            #print(key1)
            newkeys.append(key1)
    #print("xmp:")
    for key1 in f_metadata2.xmp_keys:
        if key1 not in f_metadata1.xmp_keys:
            #print(key1)
            newkeys.append(key1)
    return newkeys
# prints keys that file2 has but file1 doesn't have

# init format test
def freshKeys(p_file_1, p_file_2):
    # prints the values of file2 that are in file2's newKeys
    f_metadata1 = pyexiv2.ImageMetadata(p_file_1)
    f_metadata1.read()
    f_metadata2 = pyexiv2.ImageMetadata(p_file_2)
    f_metadata2.read()
    f_newkeys = newKeys(p_file_1, p_file_2)
    f_vals = []
    for key in f_newkeys:
        if key=='Exif.Photo.0xea1c' or key=='Exif.Image.0xea1c':    #these values are too long
            #f_vals.append((key, "..."))
            f_vals.append("...")
        elif key=='Xmp.xmp.CreateDate' or key=='Xmp.MicrosoftPhoto.DateAcquired':
        #if key=='Xmp.xmp.CreateDate' or key=='Xmp.MicrosoftPhoto.DateAcquired':
            #f_vals.append((key, "pyexiv2.xmp.XmpValueError")) #these can't be parsed by pyexiv2 for some reason.
            f_vals.append("pyexiv2.xmp.XmpValueError")
        else:
            #f_vals.append((key, f_metadata2[key].value))
            f_vals.append(f_metadata2[key].value)
            #f_vals.append(type(f_metadata2[key].value))
    return f_vals

def freshVals(p_file_1, p_file_2):
    # prints the values of file2 that are in file2's newKeys
    f_metadata1 = pyexiv2.ImageMetadata(p_file_1)
    f_metadata1.read()
    f_metadata2 = pyexiv2.ImageMetadata(p_file_2)
    f_metadata2.read()
    f_newkeys = newKeys(p_file_1, p_file_2)
    f_vals = []
    for key in f_newkeys:
        if key=='Exif.Photo.0xea1c' or key=='Exif.Image.0xea1c':    #these values are too long
            #f_vals.append((key, "..."))
            f_vals.append("...")
        elif key=='Xmp.xmp.CreateDate' or key=='Xmp.MicrosoftPhoto.DateAcquired':
        #if key=='Xmp.xmp.CreateDate' or key=='Xmp.MicrosoftPhoto.DateAcquired':
            #f_vals.append((key, "pyexiv2.xmp.XmpValueError")) #these can't be parsed by pyexiv2 for some reason.
            f_vals.append("pyexiv2.xmp.XmpValueError")
        else:
            #f_vals.append((key, f_metadata2[key].value))
            f_vals.append(f_metadata2[key].value)
            #f_vals.append(type(f_metadata2[key].value))
    return f_vals

def freshTypes(p_file_1, p_file_2):
    # prints the values of file2 that are in file2's newKeys
    f_metadata1 = pyexiv2.ImageMetadata(p_file_1)
    f_metadata1.read()
    f_metadata2 = pyexiv2.ImageMetadata(p_file_2)
    f_metadata2.read()
    f_newkeys = newKeys(p_file_1, p_file_2)
    f_vals = []
    for key in f_newkeys:
        if key=='Exif.Photo.0xea1c' or key=='Exif.Image.0xea1c':    #these values are too long
            #f_vals.append((key, "..."))
            f_vals.append("...")
        elif key=='Xmp.xmp.CreateDate' or key=='Xmp.MicrosoftPhoto.DateAcquired':
        #if key=='Xmp.xmp.CreateDate' or key=='Xmp.MicrosoftPhoto.DateAcquired':
            #f_vals.append((key, "pyexiv2.xmp.XmpValueError")) #these can't be parsed by pyexiv2 for some reason.
            f_vals.append("pyexiv2.xmp.XmpValueError")
        else:
            #f_vals.append((key, f_metadata2[key].value))
            f_vals.append(f_metadata2[key].value)
            #f_vals.append(type(f_metadata2[key].value))
    return f_vals


def bruteParse(p_file_1, p_file_2):
    # prints value in file2 using all potential parsing methods
    f_metadata1 = pyexiv2.ImageMetadata(p_file_1)
    f_metadata1.read()
    f_metadata2 = pyexiv2.ImageMetadata(p_file_2)
    f_metadata2.read()
    f_newkeys = newKeys(p_file_1, p_file_2)
    f_vals = []
    for key in f_newkeys:
        if key=='Exif.Photo.0xea1c' or key=='Exif.Image.0xea1c':    #these values are too long and worthless
            f_vals.append("useless")
        elif key=='Xmp.xmpMM.InstanceID' or key=='Exif.Image.ExifTag':  # these values are also useless
            f_vals.append("useless")
        elif key=='Xmp.xmp.CreateDate' or key=='Xmp.MicrosoftPhoto.DateAcquired':
            f_vals.append("pyexiv2.xmp.XmpValueError")
        elif key=='Exif.Image.XPComment' or \
                key=='Exif.Image.XPSubject' or \
                key=='Exif.Image.XPTitle' or \
                key=='Exif.Image.XPKeywords' or \
                key=='Exif.Image.XPAuthor':
            f_vals.append(MetadataManager.raw_to_cleanStr(f_metadata2[key].value))
        elif key=='Xmp.dc.description' or \
                key=='Xmp.dc.title':
            f_vals.append(f_metadata2[key].value['x-default'])
        else:
            f_vals.append(f_metadata2[key].value)
    return f_vals

def whichParser(p_file_1, p_file_2):
    # prints value in file2 using all potential parsing methods
    f_metadata1 = pyexiv2.ImageMetadata(p_file_1)
    f_metadata1.read()
    f_metadata2 = pyexiv2.ImageMetadata(p_file_2)
    f_metadata2.read()
    f_newkeys = newKeys(p_file_1, p_file_2)
    f_vals = []
    for key in f_newkeys:
        if key=='Exif.Photo.0xea1c' or key=='Exif.Image.0xea1c':    #these values are too long and worthless
            f_vals.append("useless")
        elif key=='Xmp.xmpMM.InstanceID' or key=='Exif.Image.ExifTag':  # these values are also useless
            f_vals.append("useless")
        elif key=='Xmp.xmp.CreateDate' or key=='Xmp.MicrosoftPhoto.DateAcquired':
            f_vals.append("???")
        elif key=='Exif.Image.XPComment' or \
                key=='Exif.Image.XPSubject' or \
                key=='Exif.Image.XPTitle' or \
                key=='Exif.Image.XPKeywords' or \
                key=='Exif.Image.XPAuthor':
            f_vals.append("MetadataManager.raw_to_cleanStr(f_metadata2[key].value)")
        elif key=='Xmp.dc.description' or \
                key=='Xmp.dc.title':
            f_vals.append("f_metadata2[key].value['x-default']")
        else:
            f_vals.append("f_metadata2[key].value")
    return f_vals

#remove/wipe test
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
#also run compAllVals

#wipe key test
#run missingKeys
#def niaveFetch(p_file_1, p_file_2, p_keynum):
    #tries to print a value from a missing key as if it still exists
#def refreshCheck(p_file_1, p_file_2, p_keynum):
    #adds single-char/blank value then prints it


#control test
#allKeys(g_file_1)
#allMeta(g_file_1)
#compAllVals(g_file_1, g_file_2)
#missingKeys(g_file_1, g_file_2)
def printlist(p_list):
    for item in p_list:
        print(item)



print("\ninit format jpeg test 1")
printlist(compAllVals("/media/sf_tagger/windowstesting/skull1.jpg", "/media/sf_tagger/windowstesting/skull1m.jpg"))
print("\ninit format jpeg test 2")
printlist(compAllVals("/media/sf_tagger/windowstesting/skull2.jpg", "/media/sf_tagger/windowstesting/skull2m.jpg"))
print("\ninit format jpeg test 3")
printlist(compAllVals("/media/sf_tagger/windowstesting/skull3.jpg", "/media/sf_tagger/windowstesting/skull3m.jpg"))
print("\ninit format jpeg test 4")
printlist(compAllVals("/media/sf_tagger/windowstesting/skull4.jpg", "/media/sf_tagger/windowstesting/skull4m.jpg"))
print("\ninit format jpeg test 5")
printlist(compAllVals("/media/sf_tagger/windowstesting/skull5.jpg", "/media/sf_tagger/windowstesting/skull5m.jpg"))
print("\ninit format jpeg test 6")
printlist(compAllVals("/media/sf_tagger/windowstesting/skull6.jpg", "/media/sf_tagger/windowstesting/skull6m.jpg"))
print("\ninit format jpeg test 7")
printlist(compAllVals("/media/sf_tagger/windowstesting/skull7.jpg", "/media/sf_tagger/windowstesting/skull7m.jpg"))
print("\ninit format jpeg test 8")
printlist(compAllVals("/media/sf_tagger/windowstesting/skull8.jpg", "/media/sf_tagger/windowstesting/skull8m.jpg"))

"""
g_key = "Xmp.xmpMM.InstanceID"
g_file_1 = "/media/sf_tagger/windowstesting/skull.jpg"
g_file_2 = "/media/sf_tagger/windowstesting/skull7.jpg"

g_metadata1 = pyexiv2.ImageMetadata(g_file_1)
g_metadata1.read()
g_metadata2 = pyexiv2.ImageMetadata(g_file_2)
g_metadata2.read()
print((g_key, g_metadata2[g_key].value))
"""




