import datetime
import pyexiv2

detailedData = pyexiv2.ImageMetadata('Olympus_C8080WZ.jpg')

print(detailedData.read())
print(detailedData.exif_keys)
print("check0")
exifTags = detailedData.exif_keys
"""
print("Exif.Image.Make")
print((detailedData['Exif.Image.Make']).value)
print("Exif.Image.Model")
print((detailedData['Exif.Image.Model']).value)
print("Exif.Image.Artist")
print((detailedData['Exif.Image.Artist']).value)
print("Exif.Image.Software")
print((detailedData['Exif.Image.Software']).value)
print("Exif.Image.ExifTag")
print((detailedData['Exif.Image.ExifTag']).value)
print("Exif.Photo.ExifVersion")
print((detailedData['Exif.Photo.ExifVersion']).value)
print("Exif.Photo.UserComment")
print((detailedData['Exif.Photo.UserComment']).value)
print("Exif.Photo.FileSource")
print((detailedData['Exif.Photo.FileSource']).value)
print("Exif.Image.XPKeywords")"""
#print((detailedData['Exif.Image.XPKeywords']).value) #throws 'Tag not set' error

keyd = 'Exif.Photo.UserComment'
print(detailedData[keyd])
value = "This is a useful comment."
detailedData[keyd] = pyexiv2.ExifTag(keyd,value)
#metadata.write()

#tag = metadata['Exif.Image.DateTime']
#print(tag)

emptyData = pyexiv2.ImageMetadata('Cat.jpg')

print(emptyData.read())
#metadata2['Exif.Image.Model'] = "C77777"
#metadata2['Exif.Image.XPKeywords'] = bytelist

print("Exif.Image.Make")
emptyData['Exif.Image.Make'] = pyexiv2.ExifTag('Exif.Image.Make', 'sampleMake')
print((emptyData['Exif.Image.Make']).value)

print("Exif.Image.Model")
emptyData['Exif.Image.Model'] = pyexiv2.ExifTag('Exif.Image.Model','sampleModel')
print((emptyData['Exif.Image.Model']).value)

print("Exif.Image.Artist")
emptyData['Exif.Image.Artist'] = pyexiv2.ExifTag('Exif.Image.Artist','sampleArtist')
print(emptyData['Exif.Image.Artist'])

print("Exif.Image.Software")
emptyData['Exif.Image.Software'] = pyexiv2.ExifTag('Exif.Image.Software','sampleSoftware')
print((emptyData['Exif.Image.Software']).value)

print("Exif.Image.ExifTag")
#emptyData['Exif.Image.ExifTag'] = pyexiv2.ExifTag('Exif.Image.ExifTag','sampleExifTag')
#print((emptyData['Exif.Image.ExifTag']).value)

print("Exif.Photo.ExifVersion")
emptyData['Exif.Photo.ExifVersion'] = pyexiv2.ExifTag('Exif.Photo.ExifVersion','sampleVersion')
print((emptyData['Exif.Photo.ExifVersion']).value)


print("Exif.Photo.UserComment")
keyUC = 'Exif.Photo.UserComment'
valueUC = "This is a useful comment."
emptyData[keyUC] = pyexiv2.ExifTag(keyUC,valueUC)
print((emptyData['Exif.Photo.UserComment']).value)

#keyd = 'Exif.Photo.UserComment'
#print(detailedData[keyd])
#value = "This is a useful comment."
#detailedData[keyd] = pyexiv2.ExifTag(keyd,value)
#metadata.write()

print("Exif.Photo.FileSource")
emptyData['Exif.Photo.FileSource'] = pyexiv2.ExifTag('Exif.Photo.FileSource','sampleSoure')
print((emptyData['Exif.Photo.FileSource']).value)

print("Exif.Image.XPKeywords")
emptyData['Exif.Image.XPKeywords'] = pyexiv2.ExifTag('Exif.Image.XPKeywords','sampleKeywords')
##print((detailedData['Exif.Image.XPKeywords']).value) #throws 'Tag not set' error

emptyData.write()