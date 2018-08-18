import unittest
import MetadataManager
import os
import wget
import requests

g_outpath = '/home/hwynn/Pictures'
# several functions below found from: https://stackoverflow.com/a/39225272
def download_file_from_google_drive(id, destination):
    """downloads files from google drive.
    Found from https://stackoverflow.com/a/39225272"""
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)
    session.close()

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None
def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
def getGoogleDrivePicture(p_picID, p_outpath):
    """if __name__ == "__main__":
        file_id = 'TAKE ID FROM SHAREABLE LINK'
        destination = 'DESTINATION FILE ON YOUR DISK'
        download_file_from_google_drive(file_id, destination)"""
    f_downloadURL = 'https://drive.google.com/uc?authuser=0&id=' + p_picID + '&export=download'
    f_filename = wget.download(f_downloadURL, p_outpath)
    download_file_from_google_drive(p_picID, f_filename)
    return f_filename
# I made everything from this point on

g_fileList = ["fixingComputer.jpg",
              "catScreamPizza.jpg",
              "rippledotzero.jpg",
              "Missing.jpg",
              "Toaster.pdf",
              "Makefile"]

g_files = {
    'fixingComputer.jpg': '1pFEbWruySWWgNCShKP8qn8dJ9w7kXNKk',
    'catScreamPizza.jpg': '1eED3AINVizIQV44DXxj91-s2Qa9EWsAX',
    'rippledotzero.jpg': '1euq0D6OrdWVkdC4RZdFIrre7WsQ7N9do',
    'Toaster.pdf': '1ofFpQYKFTJ9NLGUMiCLtz3X5awyBAx99',
    'creepyCharger.gif': '1MQgoUI6tIQhkNMg7KIDeRraVsGhPrx0H',
    'Makefile': '1vgX2S5-g-3jr1oJj5kJZnEFPtRdFsBG3'
           }

def downloadGooglePicture(p_file):
    f_downloadedFileName = getGoogleDrivePicture(g_files[p_file], g_outpath)
    return f_downloadedFileName

def removeAllFiles():
    f_file = ''
    for item in g_fileList:
        f_file = g_outpath + '/' + item
        if os.path.exists(f_file):
            os.remove(f_file)
    return

class ErrorCheck_FileAlteringTests(unittest.TestCase):
    def test_fileNotFound(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertRaises(MetadataManager.DuplicateDataError, MetadataManager.addArtist, f_filename, "stockphotographer")
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertRaises(MetadataManager.DuplicateDataError, MetadataManager.addArtist, f_filename,
                         "photographer: idunno")
        os.remove(f_filename)
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertRaises(MetadataManager.NoSuchItemError, MetadataManager.removeArtist, f_filename, "twitter")
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertRaises(MetadataManager.NoSuchItemError, MetadataManager.removeArtist, f_filename, "cat")
        os.remove(f_filename)
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertRaises(MetadataManager.DuplicateDataError, MetadataManager.addTag, f_filename, "funny")
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertRaises(MetadataManager.DuplicateDataError, MetadataManager.addTag, f_filename, "cat")
        os.remove(f_filename)
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertRaises(MetadataManager.NoSuchItemError, MetadataManager.removeTag, f_filename, "bird")
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertRaises(MetadataManager.NoSuchItemError, MetadataManager.removeTag, f_filename, "bird")
        os.remove(f_filename)


class ErrorCheck_DelicateTests(unittest.TestCase):
    def test_fileNotFound(self):
        removeAllFiles()
        self.assertRaises(FileNotFoundError, MetadataManager.containsTitle, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.getTitle, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.setTitle, "Missing.jpg", "sampleTitle")
        self.assertRaises(FileNotFoundError, MetadataManager.searchTitle, "Missing.jpg", "sampleTitle")
        self.assertRaises(FileNotFoundError, MetadataManager.removeTitle, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.getArtists, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.setArtists, "Missing.jpg", ["thing1", "thing2"])
        self.assertRaises(FileNotFoundError, MetadataManager.searchArtists, "Missing.jpg", "sampleArtist")
        self.assertRaises(FileNotFoundError, MetadataManager.addArtist, "Missing.jpg", "jobtitle: sampleArtist")
        self.assertRaises(FileNotFoundError, MetadataManager.removeArtist, "Missing.jpg", "jobtitle: sampleArtist")
        self.assertRaises(FileNotFoundError, MetadataManager.containsTags, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.getTags, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.setTags, "Missing.jpg", ["thing1", "thing2"])
        self.assertRaises(FileNotFoundError, MetadataManager.searchTags, "Missing.jpg", "sampleTag")
        self.assertRaises(FileNotFoundError, MetadataManager.addTag, "Missing.jpg", "sampleTag")
        self.assertRaises(FileNotFoundError, MetadataManager.removeTag, "Missing.jpg", "sampleTag")
        self.assertRaises(FileNotFoundError, MetadataManager.containsDescr, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.getDescr, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.setDescr, "Missing.jpg", "sample of a file's\n description")
        self.assertRaises(FileNotFoundError, MetadataManager.searchDescr, "Missing.jpg", "line from a description")
        self.assertRaises(FileNotFoundError, MetadataManager.addDescr, "Missing.jpg", "\nnew line for a description")
        self.assertRaises(FileNotFoundError, MetadataManager.removeDescr, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.containsRating, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.getRating, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.setRating, "Missing.jpg", 3)
        self.assertRaises(FileNotFoundError, MetadataManager.searchRating, "Missing.jpg", 2)
        self.assertRaises(FileNotFoundError, MetadataManager.containsSrc, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.getSrc, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.addSrc, "Missing.jpg", "sampleurl")
        self.assertRaises(FileNotFoundError, MetadataManager.searchSrc, "Missing.jpg", "sampleurl")
        self.assertRaises(FileNotFoundError, MetadataManager.containsOrgDate, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.getOrgDate, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.setOrgDate, "Missing.jpg", "2017-Jun-20 11:13 PM")
        self.assertRaises(FileNotFoundError, MetadataManager.searchOrgDate, "Missing.jpg", "2000-Jan-10 11:13 PM")


    def test_metadataMissing(self):
        removeAllFiles()
        """Hopefully none of these tests actually alter the files"""
        f_filename = downloadGooglePicture("rippledotzero.jpg")
        self.assertRaises(MetadataManager.MetadataMissingError, MetadataManager.removeTitle, f_filename)
        self.assertRaises(MetadataManager.MetadataMissingError, MetadataManager.removeArtist, f_filename, "tumblr")
        self.assertRaises(MetadataManager.MetadataMissingError, MetadataManager.removeTag, f_filename, "penguin")
        self.assertRaises(MetadataManager.MetadataMissingError, MetadataManager.removeDescr, f_filename, "a video game cover")
        os.remove(f_filename)


    def test_noSupport(self):
        removeAllFiles()
        """We don't support .gif files yet. So we have this error"""
        f_filename = downloadGooglePicture("creepyCharger.gif")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.containsTitle, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.getTitle, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.setTitle, f_filename, "sampleTitle")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.searchTitle, f_filename, "sampleTitle")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.removeTitle, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.getArtists, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.setArtists, f_filename, ["thing1", "thing2"])
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.searchArtists, f_filename, "sampleArtist")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.addArtist, f_filename, "jobtitle: sampleArtist")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.removeArtist, f_filename, "jobtitle: sampleArtist")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.containsTags, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.getTags, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.setTags, f_filename, ["thing1", "thing2"])
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.searchTags, f_filename, "sampleTag")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.addTag, f_filename, "sampleTag")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.removeTag, f_filename, "sampleTag")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.containsDescr, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.getDescr, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.setDescr, f_filename, "sample of a file's\n description")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.searchDescr, f_filename, "line from a description")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.addDescr, f_filename, "\nnew line for a description")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.removeDescr, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.containsRating, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.getRating, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.setRating, f_filename, 3)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.searchRating, f_filename, 2)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.containsSrc, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.getSrc, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.addSrc, f_filename, "sampleurl")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.searchSrc, f_filename, "sampleurl")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.containsOrgDate, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.getOrgDate, f_filename)
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.setOrgDate, f_filename, "2017-Jun-20 11:13 PM")
        self.assertRaises(MetadataManager.SupportNotImplementedError, MetadataManager.searchOrgDate, f_filename, "2000-Jan-10 11:13 PM")
        os.remove(f_filename)


    def test_weCantTakeThat(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("Toaster.pdf")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.containsTitle, "Toaster.pdf")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.getTitle, "Toaster.pdf")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.setTitle, "Toaster.pdf", "sampleTitle")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.searchTitle, "Toaster.pdf", "sampleTitle")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.removeTitle, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.getArtists, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.setArtists, f_filename, ["thing1", "thing2"])
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.searchArtists, f_filename, "sampleArtist")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.addArtist, f_filename,  "jobtitle: sampleArtist")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.removeArtist, f_filename, "jobtitle: sampleArtist")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.containsTags, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.getTags, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.setTags, f_filename, ["thing1", "thing2"])
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.searchTags, f_filename, "sampleTag")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.addTag, f_filename, "sampleTag")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.removeTag, f_filename, "sampleTag")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.containsDescr, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.getDescr, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.setDescr, f_filename, "sample of a file's\n description")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.searchDescr, f_filename, "line from a description")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.addDescr, f_filename, "\nnew line for a description")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.removeDescr, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.containsRating, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.getRating, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.setRating, f_filename, 3)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.searchRating, f_filename, 2)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.containsSrc, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.getSrc, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.addSrc, f_filename, "sampleurl")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.searchSrc, f_filename, "sampleurl")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.containsOrgDate, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.getOrgDate, f_filename)
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.setOrgDate, f_filename, "2017-Jun-20 11:13 PM")
        self.assertRaises(MetadataManager.UnsupportedFiletypeError, MetadataManager.searchOrgDate, f_filename, "2000-Jan-10 11:13 PM")
        os.remove(f_filename)


    def test_whatEvenIsThat(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("Makefile")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.containsTitle, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.getTitle, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.setTitle, f_filename, "sampleTitle")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.searchTitle, f_filename, "sampleTitle")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.removeTitle, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.getArtists, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.setArtists, f_filename, ["thing1", "thing2"])
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.searchArtists, f_filename, "sampleArtist")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.addArtist, f_filename, "jobtitle: sampleArtist")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.removeArtist, f_filename, "jobtitle: sampleArtist")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.containsTags, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.getTags, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.setTags, f_filename, ["thing1", "thing2"])
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.searchTags, f_filename, "sampleTag")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.addTag, f_filename, "sampleTag")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.removeTag, f_filename, "sampleTag")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.containsDescr, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.getDescr, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.setDescr, f_filename, "sample of a file's\n description")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.searchDescr, f_filename, "line from a description")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.addDescr, f_filename, "\nnew line for a description")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.removeDescr, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.containsRating, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.getRating, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.setRating, f_filename, 3)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.searchRating, f_filename, 2)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.containsSrc, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.getSrc, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.addSrc, f_filename, "sampleurl")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.searchSrc, f_filename, "sampleurl")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.containsOrgDate, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.getOrgDate, f_filename)
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.setOrgDate, f_filename, "2017-Jun-20 11:13 PM")
        self.assertRaises(MetadataManager.UnknownFiletypeError, MetadataManager.searchOrgDate, f_filename, "2000-Jan-10 11:13 PM")
        os.remove(f_filename)


class ResultsCheck_DelicateTests(unittest.TestCase):
    def test_metadataResults(self):
        removeAllFiles()
        f_filename1 = downloadGooglePicture("fixingComputer.jpg")
        f_filename2 = downloadGooglePicture("catScreamPizza.jpg")
        f_filename3 = downloadGooglePicture("rippledotzero.jpg")
        self.assertEqual(True, MetadataManager.containsTitle(f_filename1))
        self.assertEqual(True, MetadataManager.containsTitle(f_filename2))
        self.assertEqual(False, MetadataManager.containsTitle(f_filename3))
        self.assertEqual("crazy man fixing computer", MetadataManager.getTitle(f_filename1))
        self.assertEqual("cat", MetadataManager.getTitle(f_filename2))
        self.assertEqual("", MetadataManager.getTitle(f_filename3))
        self.assertEqual(True, MetadataManager.searchTitle(f_filename1, "computer"))
        self.assertEqual(False, MetadataManager.searchTitle(f_filename2, "pizza"))
        self.assertEqual(False, MetadataManager.searchTitle(f_filename3, "penguin"))
        self.assertEqual(True, MetadataManager.containsArtists(f_filename1))
        self.assertEqual(True, MetadataManager.containsArtists(f_filename2))
        self.assertEqual(False, MetadataManager.containsArtists(f_filename3))
        self.assertEqual(["stockphotographer", "publisher: twitter"], MetadataManager.getArtists(f_filename1))
        self.assertEqual(["photographer: idunno"], MetadataManager.getArtists(f_filename2))
        self.assertEqual([], MetadataManager.getArtists(f_filename3))
        self.assertEqual(True, MetadataManager.searchArtists(f_filename1, "twitter"))
        self.assertEqual(False, MetadataManager.searchArtists(f_filename2, "Phil"))
        self.assertEqual(False, MetadataManager.searchArtists(f_filename3, "Simon"))
        self.assertEqual(True, MetadataManager.containsTags(f_filename1))
        self.assertEqual(True, MetadataManager.containsTags(f_filename2))
        self.assertEqual(False, MetadataManager.containsTags(f_filename3))
        self.assertEqual(["stock photo", "funny", "bad stock photos of my job", "technology"], MetadataManager.getTags(f_filename1))
        self.assertEqual(["cat"], MetadataManager.getTags(f_filename2))
        self.assertEqual([], MetadataManager.getTags(f_filename3))
        self.assertEqual(False, MetadataManager.searchTags(f_filename1, "photo"))
        self.assertEqual(True, MetadataManager.searchTags(f_filename2, "cat"))
        self.assertEqual(False, MetadataManager.searchTags(f_filename3, "video games"))
        self.assertEqual(True, MetadataManager.containsDescr(f_filename1))
        self.assertEqual(True, MetadataManager.containsDescr(f_filename2))
        self.assertEqual(False, MetadataManager.containsDescr(f_filename3))
        self.assertEqual("Bad stock photo of my job found on twitter.", MetadataManager.getDescr(f_filename1))
        self.assertEqual("a cat screaming at the camera in front of a dog wearing a pizza box", MetadataManager.getDescr(f_filename2))
        self.assertEqual("", MetadataManager.getDescr(f_filename3))
        self.assertEqual(True, MetadataManager.searchDescr(f_filename1, "stock photo"))
        self.assertEqual(False, MetadataManager.searchDescr(f_filename2, "funny"))
        self.assertEqual(False, MetadataManager.searchDescr(f_filename3, "ripple dot zero"))
        self.assertEqual(True, MetadataManager.containsRating(f_filename1))
        self.assertEqual(True, MetadataManager.containsRating(f_filename2))
        self.assertEqual(False, MetadataManager.containsRating(f_filename3))
        self.assertEqual(2, MetadataManager.getRating(f_filename1))
        self.assertEqual(4, MetadataManager.getRating(f_filename2))
        self.assertEqual(-1, MetadataManager.getRating(f_filename3))
        self.assertEqual(True, MetadataManager.searchRating(f_filename1, 2))
        self.assertEqual(False, MetadataManager.searchRating(f_filename2, 3))
        self.assertEqual(False, MetadataManager.searchRating(f_filename3, 3))
        os.remove(f_filename1)
        os.remove(f_filename2)
        os.remove(f_filename3)


class ResultsCheck_FileAlteringTests(unittest.TestCase):
    def test_setTitleResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual("I found the problem", MetadataManager.setTitle(f_filename, "I found the problem"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual("He ate the pizza man", MetadataManager.setTitle(f_filename, "He ate the pizza man"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("rippledotzero.jpg")
        self.assertEqual("video game cover", MetadataManager.setTitle(f_filename, "video game cover"))
        os.remove(f_filename)


    def test_removeTitleResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual(False, MetadataManager.removeTitle(f_filename))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual(False, MetadataManager.removeTitle(f_filename))
        os.remove(f_filename)


    def test_setArtistsResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual(["twitter"], MetadataManager.setArtists(f_filename, ["twitter"]))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual(["Phil"], MetadataManager.setArtists(f_filename, ["Phil"]))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("rippledotzero.jpg")
        self.assertEqual(["penguindude", "Artist: Simon Stalenhag"],
             MetadataManager.setArtists(f_filename, ["penguindude", "Artist: Simon Stalenhag"]))
        os.remove(f_filename)


    def test_addArtistResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual(["stockphotographer", "publisher: twitter", "model: crazyguy"], MetadataManager.addArtist(f_filename, "model: crazyguy"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual(["photographer: idunno", "model: pizzadog"], MetadataManager.addArtist(f_filename, "model: pizzadog"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("rippledotzero.jpg")
        self.assertEqual(["Artist: Simon Stalenhag"], MetadataManager.addArtist(f_filename, "Artist: Simon Stalenhag"))
        os.remove(f_filename)


    def test_removeArtistResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual(["stockphotographer"], MetadataManager.removeArtist(f_filename, "publisher: twitter"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual([], MetadataManager.removeArtist(f_filename, "photographer: idunno"))
        os.remove(f_filename)


    def test_setTagsResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual(["stock photo", "funny", "bad stock photos of my job", "technology"], MetadataManager.setTags(f_filename, ["stock photo", "funny", "bad stock photos of my job", "technology"]))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual(["funny", "cat", "dog", "dog wearing pizza box", "screaming"], MetadataManager.setTags(f_filename, ["funny", "cat", "dog", "dog wearing pizza box", "screaming"]))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("rippledotzero.jpg")
        self.assertEqual(["video games", "penguin", "browser games", "rippledotzero", "cover art"], MetadataManager.setTags(f_filename, ["video games", "penguin", "browser games", "rippledotzero", "cover art"]))
        os.remove(f_filename)


    def test_addTagResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual(["stock photo", "funny", "bad stock photos of my job", "technology", "computer"], MetadataManager.addTag(f_filename, "computer"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual(["funny", "cat", "dog", "dog wearing pizza box", "screaming", "dramatic"], MetadataManager.addTag(f_filename, "dramatic"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("rippledotzero.jpg")
        self.assertEqual(["video games"], MetadataManager.addTag(f_filename, "video games"))
        os.remove(f_filename)


    def test_removeTagResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual(["stock photo", "bad stock photos of my job", "technology", "computer"], MetadataManager.removeTag(f_filename, "funny"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual(["funny", "dog", "dog wearing pizza box", "screaming"], MetadataManager.removeTag(f_filename, "cat"))
        os.remove(f_filename)


    def test_setDescrResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual("This is basically me building my gaming pc", MetadataManager.setDescr(f_filename, "This is basically me building my gaming pc"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual("Picture of a cat\n and a dog", MetadataManager.setDescr(f_filename, "Picture of a cat\n and a dog"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("rippledotzero.jpg")
        self.assertEqual("art of a flash game about a penguin", MetadataManager.setDescr(f_filename, "art of a flash game about a penguin"))
        os.remove(f_filename)


    def test_addDescrResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual("Bad stock photo of my job found on twitter.\nThis is basically me building my gaming pc", MetadataManager.addDescr(f_filename, "\nThis is basically me building my gaming pc"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual("Picture of a cat\n and a dog\nCrazy cat picture", MetadataManager.addDescr(f_filename, "\nCrazy cat picture"))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("rippledotzero.jpg")
        self.assertEqual("The game is about a penguin", MetadataManager.addDescr(f_filename, "The game is about a penguin"))
        os.remove(f_filename)


    def test_removeDescrResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual(False, MetadataManager.removeDescr(f_filename))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual(False, MetadataManager.removeDescr(f_filename))
        os.remove(f_filename)


    def test_setRatingResults(self):
        removeAllFiles()
        f_filename = downloadGooglePicture("fixingComputer.jpg")
        self.assertEqual(1, MetadataManager.setRating(f_filename, 1))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("catScreamPizza.jpg")
        self.assertEqual(2, MetadataManager.setRating(f_filename, 2))
        os.remove(f_filename)
        f_filename = downloadGooglePicture("rippledotzero.jpg")
        self.assertEqual(2, MetadataManager.setRating(f_filename, 2))
        os.remove(f_filename)


if __name__ == '__main__':
    unittest.main()
