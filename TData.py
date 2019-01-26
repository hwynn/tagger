import datetime
import MetadataManagerL0
import MetadataManagerL1
from TestStructures import TestFile, TestData
"""
TData.py
Testing Data
This file is for storing information about files for unit tests
"""

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
'Title': {'contains': MetadataManagerL0.containsTitle,
          'get': MetadataManagerL0.getTitle,
          'set': MetadataManagerL0.setTitle,
          'search': MetadataManagerL1.searchTitle,
          'wipe':  MetadataManagerL0.wipeTitle
          },
'Artist': {'contains': MetadataManagerL0.containsArtists,
           'get': MetadataManagerL0.getArtists,
           'set': MetadataManagerL0.setArtists,
           'search': MetadataManagerL1.searchArtists,
           'add': MetadataManagerL1.addArtist,
           'remove': MetadataManagerL1.removeArtist,
           'wipe':  MetadataManagerL0.wipeArtists
           },
'Tags': {'contains': MetadataManagerL0.containsTags,
         'get': MetadataManagerL0.getTags,
         'set': MetadataManagerL0.setTags,
         'search': MetadataManagerL1.searchTags,
         'add': MetadataManagerL1.addTag,
         'remove': MetadataManagerL1.removeTag,
         'wipe':  MetadataManagerL0.wipeTags
         },
'Description': {'contains': MetadataManagerL0.containsDescr,
                'get': MetadataManagerL0.getDescr,
                'set': MetadataManagerL0.setDescr,
                'search': MetadataManagerL1.searchDescr,
                'add': MetadataManagerL1.addDescr,
                'wipe':  MetadataManagerL0.wipeDescr
                },
'Rating': {'contains': MetadataManagerL0.containsRating,
           'get': MetadataManagerL0.getRating,
           'set': MetadataManagerL0.setRating,
           'search': MetadataManagerL1.searchRating,
           'wipe':  MetadataManagerL0.wipeRating
           },
'Date Created': {'contains': MetadataManagerL0.containsOrgDate,
                 'get': MetadataManagerL0.getOrgDate,
                 'set': MetadataManagerL0.setOrgDate,
                 'search': MetadataManagerL1.searchOrgDate
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

g_testfile0 = "/home/hwynn/Pictures/psyduck.jpg"
g_testfile1 = "/home/hwynn/Pictures/salamence.tif"
g_testfile2 = "/home/hwynn/Pictures/paras.png"
g_testfile3 = "/home/hwynn/Pictures/onix.png"
g_testfile4 = "/home/hwynn/Pictures/snorlax.tif"
g_testfile5 = "/home/hwynn/Pictures/pichu.tif"
g_testfile6 = "/home/hwynn/Pictures/charmander.tif"
g_testfile7 = "/home/hwynn/Pictures/lapras.png"
g_testfile8 = "/home/hwynn/Pictures/vulpix.png"
g_testfile9 = "/home/hwynn/Pictures/lugia.png"


psyduck = TestFile('psyduck.jpg', '/home/hwynn/Pictures/psyduck.jpg',
p_googleID = '1KymIHB7ASeRPwPFpLolv8CmeAseL6Qrn', p_metadata = None)

salamence = TestFile('salamence.tif', '/home/hwynn/Pictures/salamence.tif',
p_googleID = '1BVrEONGdTXtFTmyhShccM2I8uQjP1dd0', p_metadata = None)

paras = TestFile('paras.png', '/home/hwynn/Pictures/paras.png',
p_googleID = '1cnVPBqKo6nwIQvbtvBpJ-V2oDvzrOEvw', p_metadata = None)

onix = TestFile('onix.png', '/home/hwynn/Pictures/onix.png',
p_googleID = '1FP5wrzq8yk6jchHcqcE6ypDLkx-IvTdy', p_metadata = None)

snorlax = TestFile('snorlax.tif', '/home/hwynn/Pictures/snorlax.tif',
p_googleID = '1SXSdqZn5NEQkU9jWKgfpKRRfw_TPmFfJ', p_metadata = None)

pichu = TestFile('pichu.tif', '/home/hwynn/Pictures/pichu.tif',
p_googleID = '1uyQReOoZ0bYpKTgVd_UTQPmtFrEyuB0d', p_metadata = None)

charmander = TestFile('charmander.tif', '/home/hwynn/Pictures/charmander.tif',
p_googleID = '13Xgu-fsH9TsflkiH8ZCCo1nz3Kvn0Psp', p_metadata = None)

lapras = TestFile('lapras.png', '/home/hwynn/Pictures/lapras.png',
p_googleID = '1dMHjUMNZVVX1ESnEc_cojdgcuLC0yK3G', p_metadata = None)

vulpix = TestFile('vulpix.png', '/home/hwynn/Pictures/vulpix.png',
p_googleID = None, p_metadata = None)
'1TIbeLIobSS-arr6Xyxdtbz5ofwS_co8b'
lugia = TestFile('lugia.png', '/home/hwynn/Pictures/lugia.png',
p_googleID = None, p_metadata = None)
'1Re2GJB48UsOBkUYOujsGtBoIlA6Jr1SV'

g_files2 = {
    'pokefile0': psyduck,
    'pokefile1': salamence,
    'pokefile2': paras,
    'pokefile3': onix,
    'pokefile4': snorlax,
    'pokefile5': pichu,
	'pokefile6': charmander,
	'pokefile7': lapras,
	'pokefile8': vulpix,
	'pokefile9': lugia
           }


g_title0 = "Best Gift"
g_title1 = "Everyone party"
g_title3 = 'Fancy video game fanart'
g_title6 = 'bullet wave'
g_title8 = 'weird cat drawing'
g_desc3 = 'It\'s super vampire gungirl holding a giant knife. Very stylish'
g_desc4 = 'screenshot from a great letsplay'
g_desc7 = 'This is a picture of famous man.\n\mIt was really cool meeting him.\nYolo'
g_desc8 = 'Some fast drawing of a weird cat. It\'s staring at a pizza like it wants to sit on it. I found this online a long time ago.'
g_rating0 = 3
g_rating1 = 2
g_rating2 = 2
g_rating4 = 1
g_rating5 = 4
g_rating7 = 5
g_rating8 = 1
g_tags0 = ['socks', 'famous']
g_tags2 = ['mspaint', 'internet jokes']
g_tags4 = ['screenshot']
g_tags5 = ['internet jokes']
g_tags8 = ['drawing', 'cat', 'mspaint']
g_artist0 = ['Actor: Danny Devito']
g_artist2 = ['anonymous']
g_artist4 = ['xX_KillerZ5_Xx', 'Player: Matt Mcmuscles']
g_artist6 = ['lineart: angelWood', 'character: DarkDork45']
g_artist7 = ['Dr.Mc.DrD..E']
g_artist8 = ['9566215387126']
g_date0 = datetime.datetime(2017, 7, 20, 11, 32)
g_date2 = datetime.datetime(2011, 3, 5)
g_date4 = datetime.datetime(2019, 1, 9, 5, 20)
g_date5 = datetime.datetime(2009, 8, 1)
g_date8 = datetime.datetime(2019, 1, 18, 18, 32)
g_source4 = 'https//youtube.com/333243/'
g_source7 = 'https//photobucket.com/221443'
g_source8 = 'tinyu.rl/1jv345'
g_seriesname0 = 'surprise party 2017'
g_seriesname2 = 'funnydumbo'
g_seriesname4 = 'deadfart super friend spark scene'
g_seriesname5 = 'dog fart collection'
g_seriesname8 = 'cat pizza meme'
g_seriesins0 = 11
g_seriesins3 = 3
g_seriesins4 = 4
g_seriesins5 = 8
g_seriesins8 = 2
g_mdate0 = datetime.datetime(2019, 1, 9, 5, 20)
g_mdate1 = datetime.datetime(2019, 1, 9, 5, 24)
g_mdate5 = datetime.datetime(2019, 1, 9, 6, 15)
g_mdate6 = datetime.datetime(2019, 1, 10, 2, 9)
g_mdate7 = datetime.datetime(2019, 1, 10, 2, 20)
g_mdate8 = datetime.datetime(2019, 1, 10, 3, 41)
g_mdate9 = datetime.datetime(2019, 1, 9, 5, 20)
g_mark0 = 'taggerMark'
g_mark1 = 'taggerMark'
g_mark3 = 'taggerMark'
g_mark4 = 'taggerMark'
g_mark6 = 'taggerMark'
g_mark7 = 'taggerMark'
g_mark8 = 'taggerMark'
g_mark9 = 'taggerMark'
g_vers0 = "0.03"
g_vers1 = "0.10"
g_vers2 = "1.03"
g_vers4 = "1.03"
g_vers5 = "1.03"
g_vers7 = "1.05"
g_vers8 = "1.03"
g_vers9 = "0.50"




g_title0 = "Best Gift"
g_rating0 = 3
g_tags0 = ['socks', 'famous']
g_artist0 = ['Actor: Danny Devito']
g_date0 = datetime.datetime(2017, 7, 20, 11, 32)
g_seriesname0 = 'surprise party 2017'
g_seriesins0 = 11
g_mdate0 = datetime.datetime(2019, 1, 9, 5, 20)
g_mark0 = 'taggerMark'
g_vers0 = "0.03"

g_title1 = "Everyone party"
g_rating1 = 2
g_mdate1 = datetime.datetime(2019, 1, 9, 5, 24)
g_mark1 = 'taggerMark'
g_vers1 = "0.10"

g_rating2 = 2
g_tags2 = ['mspaint', 'internet jokes']
g_artist2 = ['anonymous']
g_date2 = datetime.datetime(2011, 3, 5)
g_seriesname2 = 'funnydumbo'
g_vers2 = "1.03"

g_title3 = 'Fancy video game fanart'
g_desc3 = 'It\'s super vampire gungirl holding a giant knife. Very stylish'
g_seriesins3 = 3
g_mark3 = 'taggerMark'

g_desc4 = 'screenshot from a great letsplay'
g_rating4 = 1
g_tags4 = ['screenshot']
g_artist4 = ['xX_KillerZ5_Xx', 'Player: Matt Mcmuscles']
g_date4 = datetime.datetime(2019, 1, 9, 5, 20)
g_source4 = 'https//youtube.com/333243/'
g_seriesname4 = 'deadfart super friend spark scene'
g_seriesins4 = 4
g_mark4 = 'taggerMark'
g_vers4 = "1.03"

g_rating5 = 4
g_tags5 = ['internet jokes']
g_date5 = datetime.datetime(2009, 8, 1)
g_seriesname5 = 'dog fart collection'
g_seriesins5 = 8
g_mdate5 = datetime.datetime(2019, 1, 9, 6, 15)
g_vers5 = "1.03"

g_title6 = 'bullet wave'
g_artist6 = ['lineart: angelWood', 'character: DarkDork45']
g_mdate6 = datetime.datetime(2019, 1, 10, 2, 9)
g_mark6 = 'taggerMark'

g_desc7 = 'This is a picture of famous man.\n\mIt was really cool meeting him.\nYolo'
g_rating7 = 5
g_artist7 = ['Dr.Mc.DrD..E']
g_source7 = 'https//photobucket.com/221443'
g_mdate7 = datetime.datetime(2019, 1, 10, 2, 20)
g_mark7 = 'taggerMark'
g_vers7 = "1.05"

g_title8 = 'weird cat drawing'
g_desc8 = 'Some fast drawing of a weird cat. It\'s staring at a pizza like it wants to sit on it. I found this online a long time ago.'
g_rating8 = 1
g_tags8 = ['drawing', 'cat', 'mspaint']
g_artist8 = ['9566215387126']
g_date8 = datetime.datetime(2019, 1, 18, 18, 32)
g_source8 = 'tinyu.rl/1jv345'
g_seriesname8 = 'cat pizza meme'
g_seriesins8 = 2
g_mark8 = 'taggerMark'
g_vers8 = "1.03"

g_mdate9 = datetime.datetime(2019, 1, 9, 5, 20)
g_mark9 = 'taggerMark'
g_vers9 = "0.50"
g_mdate8 = datetime.datetime(2019, 1, 10, 3, 41)

"""
MetadataManagerL0.allMeta(g_testfile0)
MetadataManagerL0.allMeta(g_testfile1)
MetadataManagerL0.allMeta(g_testfile2)
MetadataManagerL0.allMeta(g_testfile3)
MetadataManagerL0.allMeta(g_testfile4)
MetadataManagerL0.allMeta(g_testfile5)
MetadataManagerL0.allMeta(g_testfile6)
MetadataManagerL0.allMeta(g_testfile7)
MetadataManagerL0.allMeta(g_testfile8)
MetadataManagerL0.allMeta(g_testfile9)
"""

sampleData = TestData(p_title="Sample Title", p_desc="Sample description of our\nfile",
                      p_rating= 2,
                      p_tags=["test tag", "funny"],
                      p_artists=["Artist: Dave Dude", "Writer: Sally Smith"],
                      p_date= datetime.datetime(2012, 1, 5, 7, 30),
                      p_src="https://www.sampleURl.com",
                      p_series="Sample Series",
                      p_installment=12,
                      p_metadate= datetime.datetime(2012, 4, 13),
                      p_taggermark="SampleMark",
                      p_version='1.66'
)