#!/usr/bin/env python3

class TestData:
    """
    This is a full set of metadata for a given file.
    It can be data a file has or data we want to give a file
    """

    def __init__(self,
                 p_title = None,
                 p_desc = None,
                 p_rating = None,
                 p_tags = None,
                 p_artists = None,
                 p_date = None,
                 p_src = None,
                 p_series = None,
                 p_installment = None,
                 p_metadate = None,
                 p_taggermark = None,
                 p_version = None):
        self.title = p_title
        self.desc  = p_desc
        self.rating = p_rating
        self.tags = p_tags
        self.artists = p_artists
        self.date = p_date
        self.src = p_src
        self.series = p_series
        self.installment = p_installment
        self.metadate = p_metadate
        self.taggermark = p_taggermark
        self.version = p_version
    def getItem(self, p_metatype):
        if p_metatype == 'Title':
            return self.title
        elif p_metatype == 'Description':
            return self.desc
        elif p_metatype=='Rating':
            return self.rating
        elif p_metatype=='Tags':
            return self.tags
        elif p_metatype=='Artist':
            return self.artists
        elif p_metatype=='Date Created':
            return self.date
        elif p_metatype=='Source':
            return self.src
        elif p_metatype=='SeriesName':
            return self.series
        elif p_metatype=='SeriesInstallment':
            return self.installment
        elif p_metatype=='MetadataDate':
            return self.installment
        elif p_metatype=='SeriesInstallment':
            return self.metadate
        elif p_metatype=='TaggerMark':
            return self.taggermark
        elif p_metatype=='VersionNum':
            return self.version
        else:
            raise ValueError("This isn't a real type of metadata.")

class TestFile:
    """
    This class should contain everything we need for a single file
    that's going to be used for testing
    """
    def __init__(self, p_filename, p_fullname, p_googleID = None, p_metadata = None):
        self.filename = p_filename
        self.fullname = p_fullname
        self.googleID = p_googleID
        self.metadata = p_metadata


