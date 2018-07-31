import datetime
import pyexiv2

metadata = pyexiv2.ImageMetadata('Olympus_C8080WZ.jpg')

print(metadata.read())
print(metadata.exif_keys)
exifTags = metadata.exif_keys


#for tag in exifTags:
#    print(tag)

key = 'Exif.Photo.UserComment'
print(metadata[key])
value = "This is a useful comment."
metadata[key] = pyexiv2.ExifTag(key,value)
metadata.write()

print(metadata[key])


#tag = metadata['Exif.Image.DateTime']
#print(tag)


metadata2 = pyexiv2.ImageMetadata('Cat.jpg')
#metadata2['Exif.Image.Model'] = "C77777"
#metadata2['Exif.Image.XPKeywords'] = bytelist
