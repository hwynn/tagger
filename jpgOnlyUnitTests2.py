import unittest
import MetadataManager

import os
from TestStructures import TestFile, TestData
from TestingManager import downloadGooglePicture, removeAllFiles, loadFiles, cloneThese, releaseAllClones, singleClone

#import TData
from TData import g_metadataTypes, g_supportedFunctions, g_Func, g_sampleValues
from TData import g_outpath
from TData import creepyCharger
from TData import rippledotzero
from TData import Toaster
from TData import squirrel
from TData import boxcat
from TData import wikihowRat
from TData import frogyellow
g_allfiles = [creepyCharger, rippledotzero, Toaster, squirrel, boxcat, wikihowRat, frogyellow]

#print("outpath:", g_outpath)
g_loadednames = loadFiles(g_allfiles)
#print("loaded names:", g_loadednames)
g_clonenames = cloneThese(g_loadednames)

class ErrorCheck_DelicateTests(unittest.TestCase):
    def test_noSupport(self):
        """We don't support .gif files yet. So we have this error"""
        releaseAllClones(g_clonenames)
        #f_filename = downloadGooglePicture(creepyCharger)
        f_filename = singleClone(creepyCharger.fullname)
        for mtype in g_metadataTypes:
            for oper in g_supportedFunctions[mtype]:
                #check if this function has more than 1 argument
                if mtype in g_Func:
                    if oper in g_sampleValues[mtype]:#does this function have extra values?
                        if isinstance(g_sampleValues[mtype][oper], tuple):#are the extra values in a tuple?
                            if len(g_sampleValues[mtype][oper])==2:#check if this function has 2 extra arguments
                                # runs test with 2 extra provided arguments
                                self.assertRaises(MetadataManager.UnsupportedFiletypeError,
                                                  g_Func[mtype][oper], f_filename,
                                                  g_sampleValues[mtype][oper][0], g_sampleValues[mtype][oper][1])
                            else:
                                print("this shouldn't happen.")
                        else: #there's only 1 extra argument
                            # runs test with a provided sample value
                            self.assertRaises(MetadataManager.UnsupportedFiletypeError, g_Func[mtype][oper],
                                          f_filename, g_sampleValues[mtype][oper])
                    else: #function has no extra values
                        #run functions with only the filename
                        self.assertRaises(MetadataManager.UnsupportedFiletypeError, g_Func[mtype][oper],
                                          f_filename)
        #print("ErrorCheck_DelicateTests() removing", f_filename)
        os.remove(f_filename)

releaseAllClones(g_clonenames)