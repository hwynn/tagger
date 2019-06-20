#!/usr/bin/env python3
import unittest
import datetime
import os
import MetadataManagerL1
import MetadataManagerL0
import configManagement
from TestingManager import loadFiles, cloneThese, releaseAllClones, singleClone
from TData import g_files, g_files2, sampleData

g_allfiles = [
    g_files["fixingComputer.jpg"],
    g_files["catScreamPizza.jpg"],
    g_files["rippledotzero.jpg"],
    g_files["creepyCharger.gif"],
    g_files["Toaster.pdf"],
    g_files["Makefile"],
	g_files2['pokefile0'],
	g_files2['pokefile1'],
	g_files2['pokefile2'],
	g_files2['pokefile3'],
	g_files2['pokefile4'],
	g_files2['pokefile5'],
	g_files2['pokefile6'],
	g_files2['pokefile7'],
	g_files2['pokefile8'],
	g_files2['pokefile9']]
g_loadednames = loadFiles(g_allfiles)
g_clonenames = cloneThese(g_loadednames)

class ErrorCheck_FileAlteringTests(unittest.TestCase):

    def test_ratingInputCheck(self):
        releaseAllClones(g_clonenames)
        f_filename = singleClone(g_files["fixingComputer.jpg"].fullname)
        self.assertRaises(MetadataManagerL0.OutOfRangeError, MetadataManagerL0.setRating, f_filename, 6)
        self.assertRaises(MetadataManagerL0.OutOfRangeError, MetadataManagerL0.setRating, f_filename, 0)
        self.assertRaises(MetadataManagerL0.OutOfRangeError, MetadataManagerL0.setRating, f_filename, -1)
        # OutOfRangeError conditions are checked before NotIntegerError conditons
        self.assertRaises(MetadataManagerL0.OutOfRangeError, MetadataManagerL0.setRating, f_filename, 0.1)
        self.assertRaises(MetadataManagerL0.NotIntegerError, MetadataManagerL0.setRating, f_filename, 1.0)
        self.assertRaises(MetadataManagerL0.NotIntegerError, MetadataManagerL0.setRating, f_filename, 1.3)
        self.assertRaises(MetadataManagerL0.NotIntegerError, MetadataManagerL0.setRating, f_filename, 4.9)
        os.remove(f_filename)
        f_filename = singleClone(g_files["fixingComputer.jpg"].fullname)
        self.assertRaises(MetadataManagerL0.OutOfRangeError, MetadataManagerL1.searchRating, f_filename, 6)
        self.assertRaises(MetadataManagerL0.OutOfRangeError, MetadataManagerL1.searchRating, f_filename, -1.3)
        self.assertRaises(MetadataManagerL0.OutOfRangeError, MetadataManagerL1.searchRating, f_filename, -3)
        self.assertRaises(MetadataManagerL0.NotIntegerError, MetadataManagerL1.searchRating, f_filename, 1.0)
        self.assertRaises(MetadataManagerL0.NotIntegerError, MetadataManagerL1.searchRating, f_filename, 0.0)
        self.assertRaises(MetadataManagerL0.NotIntegerError, MetadataManagerL1.searchRating, f_filename, 1.3)
        self.assertRaises(MetadataManagerL0.NotIntegerError, MetadataManagerL1.searchRating, f_filename, 4.9)
        os.remove(f_filename)

class ErrorCheck_DelicateTests(unittest.TestCase):
    def test_metadataMissing(self):
        releaseAllClones(g_clonenames)
        """Hopefully none of these tests actually alter the files"""
        f_filename = singleClone(g_files["rippledotzero.jpg"].fullname)
        self.assertRaises(MetadataManagerL0.MetadataMissingError, MetadataManagerL0.wipeTitle, f_filename)
        self.assertRaises(MetadataManagerL0.MetadataMissingError, MetadataManagerL1.removeArtist, f_filename, "tumblr")
        self.assertRaises(MetadataManagerL0.MetadataMissingError, MetadataManagerL1.removeTag, f_filename, "penguin")
        self.assertRaises(MetadataManagerL0.MetadataMissingError, MetadataManagerL0.wipeDescr, f_filename)
        os.remove(f_filename)

class ResultsCheck_DelicateTests(unittest.TestCase):
    def test_metadataResults(self):
        releaseAllClones(g_clonenames)
        f_filename1 = singleClone(g_files["fixingComputer.jpg"].fullname)
        f_filename2 = singleClone(g_files["catScreamPizza.jpg"].fullname)
        f_filename3 = singleClone(g_files["rippledotzero.jpg"].fullname)
        self.assertEqual(True, MetadataManagerL1.searchTitle(f_filename1, "computer"))
        self.assertEqual(False, MetadataManagerL1.searchTitle(f_filename2, "pizza"))
        self.assertEqual(False, MetadataManagerL1.searchTitle(f_filename3, "penguin"))
        self.assertEqual(True, MetadataManagerL1.searchArtists(f_filename1, "twitter"))
        self.assertEqual(False, MetadataManagerL1.searchArtists(f_filename2, "Phil"))
        self.assertEqual(False, MetadataManagerL1.searchArtists(f_filename3, "Simon"))
        self.assertEqual(False, MetadataManagerL1.searchTags(f_filename1, "photo"))
        self.assertEqual(True, MetadataManagerL1.searchTags(f_filename2, "cat"))
        self.assertEqual(False, MetadataManagerL1.searchTags(f_filename3, "video games"))
        self.assertEqual(True, MetadataManagerL1.searchDescr(f_filename1, "stock photo"))
        self.assertEqual(False, MetadataManagerL1.searchDescr(f_filename2, "funny"))
        self.assertEqual(False, MetadataManagerL1.searchDescr(f_filename3, "ripple dot zero"))
        self.assertEqual(True, MetadataManagerL1.searchRating(f_filename1, 2))
        self.assertEqual(False, MetadataManagerL1.searchRating(f_filename2, 3))
        self.assertEqual(False, MetadataManagerL1.searchRating(f_filename3, 3))
        self.assertEqual(False, MetadataManagerL1.searchSource(f_filename1, "sampleSrc"))
        self.assertEqual(False, MetadataManagerL1.searchSource(f_filename2, "sampleSrc"))
        self.assertEqual(False, MetadataManagerL1.searchSource(f_filename3, "sampleSrc"))
        self.assertEqual(True, MetadataManagerL1.searchOrgDate(f_filename1, datetime.datetime(2017, 1, 1), datetime.datetime(2018, 1, 1)))
        self.assertEqual(False, MetadataManagerL1.searchOrgDate(f_filename2, datetime.datetime(2017, 1, 1), datetime.datetime(2018, 1, 1)))
        self.assertEqual(False, MetadataManagerL1.searchOrgDate(f_filename3, datetime.datetime(2017, 1, 1), datetime.datetime(2018, 1, 1)))

        os.remove(f_filename1)
        os.remove(f_filename2)
        os.remove(f_filename3)


    def test_addArtistResults(self):
        releaseAllClones(g_clonenames)

        f_value = "model: crazyguy"
        f_expected = ["model: crazyguy", "stockphotographer", "publisher: twitter"]
        f_filename = singleClone(g_files["fixingComputer.jpg"].fullname)
        MetadataManagerL1.addArtist(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getArtists(f_filename))
        os.remove(f_filename)

        f_value = "model: pizzadog"
        f_expected = ["model: pizzadog", "photographer: idunno"]
        f_filename = singleClone(g_files["catScreamPizza.jpg"].fullname)
        MetadataManagerL1.addArtist(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getArtists(f_filename))
        os.remove(f_filename)
        f_value = "Artist: Simon Stalenhag"
        f_expected = ["Artist: Simon Stalenhag"]
        f_filename = singleClone(g_files["rippledotzero.jpg"].fullname)
        MetadataManagerL1.addArtist(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getArtists(f_filename))
        os.remove(f_filename)

    def test_removeArtistResults(self):
        releaseAllClones(g_clonenames)
        f_value = "publisher: twitter"
        f_expected = ["stockphotographer"]
        f_filename = singleClone(g_files["fixingComputer.jpg"].fullname)
        MetadataManagerL1.removeArtist(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getArtists(f_filename))
        os.remove(f_filename)

        f_value = "photographer: idunno"
        f_expected = []
        f_filename = singleClone(g_files["catScreamPizza.jpg"].fullname)
        MetadataManagerL1.removeArtist(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getArtists(f_filename))
        os.remove(f_filename)

    def test_addTagResults(self):
        releaseAllClones(g_clonenames)
        f_value = "computer"
        f_expected = ["computer", "stock photo", "funny", "bad stock photos of my job", "technology"]
        f_filename = singleClone(g_files["fixingComputer.jpg"].fullname)
        MetadataManagerL1.addTag(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getTags(f_filename))
        os.remove(f_filename)
        f_value = "dramatic"
        f_expected = ["dramatic", "cat"]
        f_filename = singleClone(g_files["catScreamPizza.jpg"].fullname)
        MetadataManagerL1.addTag(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getTags(f_filename))
        os.remove(f_filename)
        f_value = "video games"
        f_expected = ["video games"]
        f_filename = singleClone(g_files["rippledotzero.jpg"].fullname)
        MetadataManagerL1.addTag(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getTags(f_filename))
        os.remove(f_filename)

    def test_removeTagResults(self):
        releaseAllClones(g_clonenames)
        f_value = "funny"
        f_expected = ["stock photo", "bad stock photos of my job", "technology"]
        f_filename = singleClone(g_files["fixingComputer.jpg"].fullname)
        MetadataManagerL1.removeTag(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getTags(f_filename))
        os.remove(f_filename)

        f_value = "cat"
        f_expected = []
        f_filename = singleClone(g_files["catScreamPizza.jpg"].fullname)
        MetadataManagerL1.removeTag(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getTags(f_filename))
        os.remove(f_filename)

    def test_addDescrResults(self):
        releaseAllClones(g_clonenames)
        f_value = "\nThis is basically me building my gaming pc"
        f_expected = "Bad stock photo of my job found on twitter.\nThis is basically me building my gaming pc"
        f_filename = singleClone(g_files["fixingComputer.jpg"].fullname)
        MetadataManagerL1.addDescr(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getDescr(f_filename))
        os.remove(f_filename)
        f_value = "\nCrazy cat picture"
        f_expected = "a cat screaming at the camera in front of a dog wearing a pizza box\nCrazy cat picture"
        f_filename = singleClone(g_files["catScreamPizza.jpg"].fullname)
        MetadataManagerL1.addDescr(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getDescr(f_filename))
        os.remove(f_filename)
        f_value = "The game is about a penguin"
        f_expected = "The game is about a penguin"
        f_filename = singleClone(g_files["rippledotzero.jpg"].fullname)
        MetadataManagerL1.addDescr(f_filename, f_value)
        self.assertEqual(f_expected, MetadataManagerL0.getDescr(f_filename))
        os.remove(f_filename)

    def hiddenMarkTest(self):
        f_mark = configManagement.getSoftwareName()
        f_version = configManagement.currentVersion()
        f_filename = singleClone(g_files2['pokefile0'].fullname)
        MetadataManagerL1.placeMark(f_filename)
        self.assertEqual(True, MetadataManagerL0.containsMetadataDate(f_filename))
        self.assertEqual(True, MetadataManagerL0.containsTaggerMark(f_filename))
        self.assertEqual(f_mark, MetadataManagerL0.getTaggerMark(f_filename))
        self.assertEqual(True, MetadataManagerL0.containsVersionNum(f_filename))
        self.assertEqual(f_version, MetadataManagerL0.getVersionNum(f_filename))
        os.remove(f_filename)


#test for rating. must be int
#number must be between 1 and 5
#two similar tests for searchRating

if __name__ == '__main__':
    unittest.main()
