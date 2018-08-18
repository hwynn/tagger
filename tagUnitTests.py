import unittest
import TestingManager
import MetadataManager

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

class fileType(unittest.TestCase):
    """this checks the file type checking
    We don't even need files to check this stuff"""

class fileRemovalProblem(unittest.TestCase):
    """This is when you're supposed to remove some metadata
    but there is no metadata to remove
    These are for raising errors"""


class fileChecks(unittest.TestCase):
    """This will contain the tests needed
    to test file related exceptions.
    No operations in this class will alter files.
    So we'll download all our files upfront."""
    c_outpath = TestingManager.g_outpath    #this is where all our pictures will be saved.

    c_missingFileName = c_outpath + '/' + 'Missing.jpg' #This is the name of a file that doesn't exist
    c_fileList = [c_missingFileName]
    for i_key, i_value in TestingManager.g_googlePics2:
        i_filename = TestingManager.getGoogleDrivePicture(i_value, c_outpath)
        c_fileList.insert(0, i_filename)
    #at this point, all files should be downloaded.
    # And c_fileList should have a list with each filename.
    # the last entry of c_fileList is a file we don't have.
    # to iterate through all real files, use: for i in range(len(c_fileList)-1):
    def test_file_not_found(self):
        '''All functions should raise FileNotFoundError exception
        if we pass the name of a file that doesn't exist'''
        self.assertRaises(FileNotFoundError, MetadataManager.containsTitle, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.getTitle, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.setTitle, "Missing.jpg", "sampleTitle")
        self.assertRaises(FileNotFoundError, MetadataManager.searchTitle, "Missing.jpg", "sampleTitle")
        self.assertRaises(FileNotFoundError, MetadataManager.removeTitle, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.containsArtists, "Missing.jpg")
        self.assertRaises(FileNotFoundError, MetadataManager.setArtists, "Missing.jpg", ["thing1", "thing2"])
        self.assertRaises(FileNotFoundError, MetadataManager.searchArtists, "Missing.jpg", "sampleArtist")
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



#test for rating. must be int
#number must be between 1 and 5
#two similar tests for searchRating



if __name__ == '__main__':
    unittest.main()
