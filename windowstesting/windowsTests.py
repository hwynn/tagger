import pyexiv2

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

#init keys test
#def newKeys(p_file_1, p_file_2):
    #prints keys that file2 has but file1 doesn't have

#init format test
#def freshVals(p_file_1, p_file_2):
    #prints the values of file2 that are in file2's newKeys
#def bruteParse(p_file_1, p_file_2):
    #prints value in file2 using all potential parsing methods

#modify test
def compAllVals(p_file_1, p_file_2):
    #Prints each key/value pair that differs between the two files
    print("Value comparison")
    f_metadata1 = pyexiv2.ImageMetadata(p_file_1)
    f_metadata1.read()
    f_metadata2 = pyexiv2.ImageMetadata(p_file_2)
    f_metadata2.read()
    diffVals = []
    print("exif:")
    for key1 in f_metadata1.exif_keys:
        if key1 in f_metadata2.exif_keys:
            if f_metadata1[key1].value!=f_metadata2[key1].value:
                print(key1)
                print(f_metadata1[key1].value)
                print(f_metadata2[key1].value)
                diffVals.append((f_metadata1[key1].value, f_metadata2[key1].value))
    print("iptc:")
    for key1 in f_metadata1.iptc_keys:
        if key1 in f_metadata2.iptc_keys:
            if f_metadata1[key1].value!=f_metadata2[key1].value:
                print(key1)
                print(f_metadata1[key1].value)
                print(f_metadata2[key1].value)
                diffVals.append((f_metadata1[key1].value, f_metadata2[key1].value))
    print("xmp:")
    for key1 in f_metadata1.xmp_keys:
        if key1 in f_metadata2.xmp_keys:
            if f_metadata1[key1].value!=f_metadata2[key1].value:
                print(key1)
                print(f_metadata1[key1].value)
                print(f_metadata2[key1].value)
                diffVals.append((f_metadata1[key1].value, f_metadata2[key1].value))
    return diffVals

#remove/wipe test
def missingKeys(p_file_1, p_file_2):
    print("missing keys")
    #prints keys that are in file1, but not in file2
    f_metadata1 = pyexiv2.ImageMetadata(p_file_1)
    f_metadata1.read()
    f_metadata2 = pyexiv2.ImageMetadata(p_file_2)
    f_metadata2.read()
    missingkeys = []
    print("exif:")
    for key1 in f_metadata1.exif_keys:
        if key1 not in f_metadata2.exif_keys:
            print(key1)
            missingkeys.append(key1)
    print("iptc:")
    for key1 in f_metadata1.iptc_keys:
        if key1 not in f_metadata2.iptc_keys:
            print(key1)
            missingkeys.append(key1)
    print("xmp:")
    for key1 in f_metadata1.xmp_keys:
        if key1 not in f_metadata2.xmp_keys:
            print(key1)
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
compAllVals(g_file_1, g_file_2)
missingKeys(g_file_1, g_file_2)