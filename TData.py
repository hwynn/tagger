import datetime
import MetadataManager
from TestStructures import TestFile, TestData
"""
TData.py
Testing Data
This file is for storing information about files for unit tests
"""

# ===========================================================================
# ----------------------Artist Metadata Test Data----------------------------
# ===========================================================================

g_getArtists_testData = {'fixingComputer': ["stockphotographer", "publisher: twitter"],
                         'catScreamPizza': ["photographer: idunno", "publisher: tumblrguy"],
                         'gregTwitterJoke': [],
                         'wikihowRat': ["volunteer tracer"],
                         'rippledotzero': ["penguindude"],
                         'oppusumBitesApple': ["VoteForPuff"],
                         'creepyCharger': [],
                         'princessAtDoor': []}
g_containsArtists_testData = {'fixingComputer': True,
                              'catScreamPizza': True,
                              'gregTwitterJoke': False,
                              'wikihowRat': True,
                              'rippledotzero': True,
                              'oppusumBitesApple': True,
                              'creepyCharger': False,
                              'princessAtDoor': False}
g_setArtists_testData = {'fixingComputer': ["stock photo", "funny", "bad stock photos of my job", "technology"],
                         'catScreamPizza': ["Phil"],
                         'gregTwitterJoke': ["Joe"],
                         'wikihowRat': ["volunteer"],
                         'rippledotzero': ["Simon"],
                         'oppusumBitesApple': ["Vote"],
                         'creepyCharger': [],
                         'princessAtDoor': []}
g_searchArtist_testData = {'fixingComputer': "twitter",
                           'catScreamPizza': "Phil",
                           'gregTwitterJoke': "Joe",
                           'wikihowRat': "volunteer",
                           'rippledotzero': "Simon",
                           'oppusumBitesApple': "Vote",
                           'creepyCharger': "",
                           'princessAtDoor': ""}
g_searchArtist_testResults = {'fixingComputer': True,
                              'catScreamPizza': False,
                              'gregTwitterJoke': False,
                              'wikihowRat': True,
                              'rippledotzero': True,
                              'oppusumBitesApple': True,
                              'creepyCharger': False,
                              'princessAtDoor': False}
g_addArtist_testData = {'fixingComputer': "model: crazyguy",
                        'catScreamPizza': "model: pizzadog",
                        'gregTwitterJoke': "Solomon Georgio",
                        'wikihowRat': "publisher: wikihow",
                        'rippledotzero': "Artist: Simon Stalenhag",
                        'oppusumBitesApple': "Model: opposum baby",
                        'creepyCharger': "",
                        'princessAtDoor': ""}

# ===========================================================================
# -----------------------Title Metadata Test Data----------------------------
# ===========================================================================
g_getTitle_testData = {'fixingComputer': "crazy man fixing computer",
                       'catScreamPizza': "",
                       'gregTwitterJoke': "greg throws knives",
                       'wikihowRat': "wikihow rat",
                       'rippledotzero': "rippledotzero cover",
                       'oppusumBitesApple': "too small for apple",
                       'creepyCharger': "",
                       'princessAtDoor': "", }
g_containsTitle_testData = {'fixingComputer': True,
                            'catScreamPizza': False,
                            'gregTwitterJoke': True,
                            'wikihowRat': True,
                            'rippledotzero': True,
                            'oppusumBitesApple': True,
                            'creepyCharger': False,
                            'princessAtDoor': False, }
g_setTitle_testData = {'fixingComputer': "stock image of me",
                       'catScreamPizza': "the pizza is here",
                       'gregTwitterJoke': "NITW joke",
                       'wikihowRat': "cool rat",
                       'rippledotzero': "flash game thing",
                       'oppusumBitesApple': "cute opposum",
                       'creepyCharger': "creepy charger",
                       'princessAtDoor': "cute dog gif", }
g_searchTitle_testData = {'fixingComputer': "computer",
                          'catScreamPizza': "dog",
                          'gregTwitterJoke': "greg",
                          'wikihowRat': "rat",
                          'rippledotzero': "game",
                          'oppusumBitesApple': "oppusum",
                          'creepyCharger': "charger",
                          'princessAtDoor': "dog", }
g_searchTitle_testResults = {'fixingComputer': True,
                             'catScreamPizza': False,
                             'gregTwitterJoke': True,
                             'wikihowRat': True,
                             'rippledotzero': False,
                             'oppusumBitesApple': False,
                             'creepyCharger': False,
                             'princessAtDoor': False, }

# ===========================================================================
# ------------------------Tag Metadata Test Data-----------------------------
# ===========================================================================
"""Note: The following variables have a mixed naming convention.
please forgive my deviation from proper naming style.
These names are used since they are used in a testing function which
tests a utility function. These names contain the utility function's name
for the sake of consistency and easy maintenance"""
g_containsTags_testData = {'squirrel': True,
                           'cat': False,
                           'boxcat': True,
                           "frogyellow": True,
                           "frogjump": True,
                           "titanmeme": True}
g_getTags_testData = {'squirrel': ['squirrel'],
                      'cat': [],
                      'boxcat': ['cat', 'animals', 'cat in a box'],
                      "frogyellow": ['frog'],
                      "frogjump": ['frog'],
                      "titanmeme": ['show screenshots']}
g_setTags_testData = {}
g_searchTags_testData = {'squirrel': 'pie',
                         'cat': "cat",
                         'boxcat': "ca",
                         "frogyellow": 'frog',
                         "frogjump": "jumping",
                         "titanmeme": 'show screenshots'}
g_searchTags_testResults = {'squirrel': False,
                            'cat': False,
                            'boxcat': False,
                            "frogyellow": True,
                            "frogjump": False,
                            "titanmeme": True}
g_addTag_testData = {'squirrel': 'animals',
                     'cat': "cat",
                     'boxcat': "cute",
                     "frogyellow": 'amphibian',
                     "frogjump": "jumping",
                     "titanmeme": 'anime'}
g_removeTag_testData = {'squirrel': 'squirrel',
                        'cat': "",
                        'boxcat': "animals",
                        "frogyellow": 'frog',
                        "frogjump": "frog",
                        "titanmeme": 'show screenshots'}

# ===========================================================================
# -----------------------------Google Files----------------------------------
# ===========================================================================
g_googlePics1 = {'squirrel': '1ZHDchSv9RMxJmdVeepJvvOtTx4T4am3U',
                 'cat': "1A1Nxr-1mWfFlk9hTVZtzSPfEt6ZC6uzg",
                 'boxcat': "1oxAPZSBKKTYjdXYYuwpvbKR5grK0aCZY",
                 'frogyellow': '1xMHPQrNyODWTIXQ-PxgWSPbwj7_tGerv',
                 'frogjump': '1nqFSb-hoc1c0-BlTETs0jQn3bzWeGg3T',
                 'titanmeme': "1kRybASv2UVde5wMitn_j1i4x3LklIh6s"}
g_googlePics2 = {'fixingComputer': '1pFEbWruySWWgNCShKP8qn8dJ9w7kXNKk',
                 'catScreamPizza': '1eED3AINVizIQV44DXxj91-s2Qa9EWsAX',
                 'gregTwitterJoke': '1PzDc70qhskQzUPtCgoRG3W10AisiP09W',
                 'wikihowRat': '18mFIgX2Na5DCdTO49fwamAMfdqJcjodP',
                 'rippledotzero': '1euq0D6OrdWVkdC4RZdFIrre7WsQ7N9do',
                 'oppusumBitesApple': '1EWTG-xgYGX_SdB4lPDFEs5veattK5Dxy',
                 'creepyCharger': '1MQgoUI6tIQhkNMg7KIDeRraVsGhPrx0H',
                 'princessAtDoor': '1TKjnok6DJuIHYhaeZiYFnS6RgPRcdJPK'}
g_outpath = '/home/hwynn/Pictures'


g_metadataTypes = ['Title', 'Description', 'Rating', 'Tags', 'Artist', 'Date Created']
g_metadataTypes2 = ['Title', 'Description', 'Rating', 'Tags', 'Artist', 'Date Created', 'Source',
                   'SeriesName', 'SeriesInstallment', 'MetadataDate', 'TaggerMark','VersionNum']

g_supportedFunctions = {
'Title': ['contains', 'get', 'set', 'search', 'wipe'],
'Artist': ['contains', 'get', 'set', 'search', 'add', 'remove','wipe'],
'Tags': ['contains', 'get', 'set', 'search', 'add', 'remove','wipe'],
'Description': ['contains', 'get', 'set', 'search', 'add', 'wipe'],
'Rating': ['contains', 'get', 'set', 'search', 'wipe'],
'Date Created': ['contains', 'get', 'set', 'search']
}
g_supportedFunctions2 = {
'Title': ['contains', 'get', 'set', 'search', 'wipe'],
'Artist': ['contains', 'get', 'set', 'search', 'add', 'remove','wipe'],
'Tags': ['contains', 'get', 'set', 'search', 'add', 'remove','wipe'],
'Description': ['contains', 'get', 'set', 'search', 'add', 'wipe'],
'Rating': ['contains', 'get', 'set', 'search', 'wipe'],
'Source': ['contains', 'get', 'set', 'search', 'wipe'],
'Date Created': ['contains', 'get', 'set', 'search'],
'SeriesName': ['contains', 'get', 'set', 'search', 'wipe'],
'SeriesInstallment': ['contains', 'get', 'set', 'search', 'wipe'],
'MetadataDate': ['contains', 'get', 'set', 'search'],
'TaggerMark': ['contains', 'get', 'set', 'search', 'wipe'],
'VersionNum': ['contains', 'get', 'set', 'search', 'wipe']
}

g_Func = {
'Title': {'contains': MetadataManager.containsTitle,
          'get': MetadataManager.getTitle,
          'set': MetadataManager.setTitle,
          'search': MetadataManager.searchTitle,
          'wipe':  MetadataManager.wipeTitle
          },
'Artist': {'contains': MetadataManager.containsArtists,
           'get': MetadataManager.getArtists,
           'set': MetadataManager.setArtists,
           'search': MetadataManager.searchArtists,
           'add': MetadataManager.addArtist,
           'remove': MetadataManager.removeArtist,
           'wipe':  MetadataManager.wipeArtists
           },
'Tags': {'contains': MetadataManager.containsTags,
         'get': MetadataManager.getTags,
         'set': MetadataManager.setTags,
         'search': MetadataManager.searchTags,
         'add': MetadataManager.addTag,
         'remove': MetadataManager.removeTag,
         'wipe':  MetadataManager.wipeTags
         },
'Description': {'contains': MetadataManager.containsDescr,
                'get': MetadataManager.getDescr,
                'set': MetadataManager.setDescr,
                'search': MetadataManager.searchDescr,
                'add': MetadataManager.addDescr,
                'wipe':  MetadataManager.wipeDescr
                },
'Rating': {'contains': MetadataManager.containsRating,
           'get': MetadataManager.getRating,
           'set': MetadataManager.setRating,
           'search': MetadataManager.searchRating,
           'wipe':  MetadataManager.wipeRating
           },
'Date Created': {'contains': MetadataManager.containsOrgDate,
                 'get': MetadataManager.getOrgDate,
                 'set': MetadataManager.setOrgDate,
                 'search':  MetadataManager.searchOrgDate
                 }
}

#metatype, operation
g_sampleValues = {
'Title': {'set': "sampleTitle", 'search': "sampleTitle"},
'Artist': {'set': ["thing1", "thing2"], 'search': "sampleArtist",
           'add': "jobtitle: sampleArtist", 'remove': "jobtitle: sampleArtist"},
'Tags': {'set': ["thing1", "thing2"], 'search': "sampleTag", 'add': "sampleTag", 'remove': "sampleTag"},
'Description': {'set': "sample of a file's\n description", 'search': "line from a description",
'add': "\nnew line for a description"},
'Rating': {'set': 3, 'search': 2},
'Date Created': {'set': datetime.datetime.today(), 'search': (datetime.datetime(2017, 1, 1), datetime.datetime(2018, 1, 1))}
}

#(filename, searchedItem, expectedResult)


#list of metadata types
#list of operations
#for each metadata type
#   is operation supported?
#   hasOperation{"metatype", True/False}

#for each file
#   value_givenMetaType = {"metatype", value}       for get value tests
#           value is None if file has no value          for containsVal tests
#   searches given metatype = {"metatype", [(sval1, True/False),(sval2, True/False)]}   for search tests
#   valuetoAdd = {"metatype", (valueToAdd, newValtoExpect)}
#           entry missing if metatype doesn't support operation
#   valuetoRemove = {"metatype", (valueToAdd, newValtoExpect, anything left? True/False)}
#           entry missing if metatype doesn't support operation


#Files used for error tests


g_allFiles =[]



g_sampleValues = {
'Title': {'set': "sampleTitle", 'search': "sampleTitle"},
'Artist': {'set': ["thing1", "thing2"], 'search': "sampleArtist",
           'add': "jobtitle: sampleArtist", 'remove': "jobtitle: sampleArtist"},
'Tags': {'set': ["thing1", "thing2"], 'search': "sampleTag", 'add': "sampleTag", 'remove': "sampleTag"},
'Description': {'set': "sample of a file's\n description", 'search': "line from a description",
'add': "\nnew line for a description"},
'Rating': {'set': 3, 'search': 2},
'Date Created': {'set': datetime.datetime.today(), 'search': (datetime.datetime(2017, 1, 1), datetime.datetime(2018, 1, 1))}
}

g_sampleSetValues = TestData("sampleTitle",
                             "sample of a file's\n description",
                             3,
                             ["thing1", "thing2"],
                             ["thing1", "thing2"],
                             datetime.datetime.today())
g_sampleSearchValues = TestData(p_title = "sampleTitle",
                                p_desc = "line from a description",
                                p_rating = 2,
                                p_tags = ["thing1", "thing2"],
                                p_artists = "sampleArtist",
                                p_date = (datetime.datetime(2017, 1, 1), datetime.datetime(2018, 1, 1)))





fixingComputer = TestFile('fixingComputer.jpg', '/home/hwynn/Pictures/fixingComputer.jpg',
                          '1pFEbWruySWWgNCShKP8qn8dJ9w7kXNKk', p_metadata = None)
catScreamPizza = TestFile('catScreamPizza.jpg', '/home/hwynn/Pictures/catScreamPizza.jpg',
                          '1eED3AINVizIQV44DXxj91-s2Qa9EWsAX', p_metadata = None)
rippledotzero = TestFile('rippledotzero.jpg', '/home/hwynn/Pictures/rippledotzero.jpg',
                          '1euq0D6OrdWVkdC4RZdFIrre7WsQ7N9do', p_metadata = None)
Toaster = TestFile('Toaster.pdf', '/home/hwynn/Pictures/Toaster.pdf',
                          '1ofFpQYKFTJ9NLGUMiCLtz3X5awyBAx99', p_metadata = None)
creepyCharger = TestFile('creepyCharger.gif', '/home/hwynn/Pictures/creepyCharger.gif',
                          '1MQgoUI6tIQhkNMg7KIDeRraVsGhPrx0H', p_metadata = None)
Makefile = TestFile('Makefile', '/home/hwynn/Pictures/Makefile',
                          '1vgX2S5-g-3jr1oJj5kJZnEFPtRdFsBG3', p_metadata = None)
squirrel = TestFile('Squirrel_Eating_a_peanut.jpg', '/home/hwynn/Pictures/Squirrel_Eating_a_peanut.jpg',
                    '1ZHDchSv9RMxJmdVeepJvvOtTx4T4am3U', p_metadata=None)
cat = TestFile('Cat.jpg', '/home/hwynn/Pictures/Cat.jpg',
               '1A1Nxr-1mWfFlk9hTVZtzSPfEt6ZC6uzg', p_metadata=None)
boxcat = TestFile('CatInBox.jpg', '/home/hwynn/Pictures/CatInBox.jpg',
                  '1oxAPZSBKKTYjdXYYuwpvbKR5grK0aCZY', p_metadata=None)
frogyellow = TestFile('yellowfrog.jpg', '/home/hwynn/Pictures/yellowfrog.jpg',
                      '1xMHPQrNyODWTIXQ-PxgWSPbwj7_tGerv', p_metadata=None)
frogjump = TestFile('JumpingFrog.jpg','/home/hwynn/Pictures/JumpingFrog.jpg',
                    '1nqFSb-hoc1c0-BlTETs0jQn3bzWeGg3T', p_metadata=None)
titanmeme = TestFile('attackontitancoupon.jpg', '/home/hwynn/Pictures/attackontitancoupon.jpg',
                     '1kRybASv2UVde5wMitn_j1i4x3LklIh6s', p_metadata=None)
gregTwitterJoke = TestFile('gregTwitterJoke.png', '/home/hwynn/Pictures/gregTwitterJoke.png',
                           '1PzDc70qhskQzUPtCgoRG3W10AisiP09W', p_metadata=None)
wikihowRat = TestFile('wikihowRat.jpg', '/home/hwynn/Pictures/wikihowRat.jpg',
                      '18mFIgX2Na5DCdTO49fwamAMfdqJcjodP', p_metadata=None)
oppusumBitesApple = TestFile('oppusumBitesApple.png', '/home/hwynn/Pictures/oppusumBitesApple.png',
                             '1EWTG-xgYGX_SdB4lPDFEs5veattK5Dxy', p_metadata=None)
princessAtDoor = TestFile('princessAtDoor.gif', '/home/hwynn/Pictures/princessAtDoor.gif',
                          '1TKjnok6DJuIHYhaeZiYFnS6RgPRcdJPK', p_metadata=None)
Missing = TestFile('Missing.jpg', '/home/hwynn/Pictures/Missing.jpg')


g_googlePics1 = [squirrel,
                 cat,
                 boxcat,
                 frogyellow,
                 frogjump,
                 titanmeme]
g_googlePics2 = [fixingComputer, catScreamPizza, gregTwitterJoke, wikihowRat,
                 rippledotzero, oppusumBitesApple, creepyCharger, princessAtDoor]
"""
g_fileList = ["fixingComputer.jpg",
              "catScreamPizza.jpg",
              "rippledotzero.jpg",
              "Missing.jpg",
              "Toaster.pdf",
              "Makefile"]
"""
g_fileList = [fixingComputer,
              catScreamPizza,
              rippledotzero,
              Missing,
              Toaster,
              Makefile]
g_files = {
    'fixingComputer.jpg': fixingComputer,
    'catScreamPizza.jpg': catScreamPizza,
    'rippledotzero.jpg': rippledotzero,
    'Toaster.pdf': Toaster,
    'creepyCharger.gif': creepyCharger,
    'Makefile': Makefile
           }
