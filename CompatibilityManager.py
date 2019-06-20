#!/usr/bin/env python3

import configManagement

def isMarked(f_filename):
	#before we check versions, lets see if this file is even marked by our software
	pass
	
def isFutureVersion(f_filename):
	#compares version of a file to the current version of the software
	pass

def isOldVersion(f_filename):
	#compares version of a file to the current version of the software
	pass
	
def getCompatCheck():
	#format, type
	pass

def setCompatCheck(p_metatype, p_ver1, p_ver2):
	"""
    Note: if any changes occur to a set function in a future version, even if it's just an extra key,
	   setCompatCheck should absolutely return false. 
	Old versions of the software cannot predict what changes would occur to a metadata type
	New versions of the software cannot predict what old version of a software made a "compatible set" to
	therefore, letting old versions set values with different rules introduces uncertainty into the system.
	EXAMPLE:
	version 3:
	 _______________title___________________   
	| dc.title | exif.title |  exif.subject | exif.desc`
	
	version 8:
	 ________title__________  ______description_________
	| dc.title | exif.title || exif.subject | exif.desc |
	
	 ====================================================================
	||	 ________title__________  ______description___________          ||
	|| | dc.title | exif.title || exif.subject |  exif.desc   |  vers 8 ||
	|| |   NULL   |   NULL     || My first cat | My first cat |         ||
	 ====================================================================
	      |  version 3 setTitle('Sassy')
	      V
	 ====================================================================
	||	 ________title__________  ______description___________          ||
	|| | dc.title | exif.title || exif.subject |  exif.desc   |  vers 8 ||
	|| |   Sassy  |   Sassy    ||    Sassy     | My first cat |         ||
	 ====================================================================
	 Now we have an inconsistent description. This is just one of many possible
	 problems we could run into if we let old versions set metadata that has had
	 even the slightest of changes behaviour.
	"""
	
	
def tryDownGradeVersion(p_filename):
	"""
	exception handling: could lose data from imcompatible metadata
	"""
	pass

def upgradeVersion(p_filename, p_oldvers):
	#should always work
	#p_oldvers is the old version of the software. This should be detected by the caller of this function
	#if the file has no version, the caller of this function should set this to the first version of the software
	#there should be an option to attempt to recover data in case a file was previously downgraded.
	#however, the user will have to make this choice on a file by file basis. 
	#And the ability to do so is turned off by default
	#The default behaviour will be to wipe any new keys introduced by a version when upgrading to that version
	#For each type of metadata that did not (or could not) have a stored value,
	#  all associated keys (for the old version) with that metadata type will be wiped
	#For every type of metadata that did have a previous value, that value is stored.
	#  all associated keys (for the old version) with that metadata type are wiped.
	#  then a new set operation is performed to put that stored value into its new appropriate keys
	"""
	EXAMPLE:
	version 3:
	 _______________title___________________   
	| dc.title | exif.title |  exif.subject | exif.desc
	
	version 8:
	 ________title__________  ______description_________
	| dc.title | exif.title || exif.subject | exif.desc |
	
	 ====================================================================
	||	 _______________title__________________                         ||
	|| | dc.title | exif.title |  exif.subject | exif.desc  vers 3      ||
	|| |  Sassy   |   Sassy    |     Sassy     |   Null   |             ||
	 ====================================================================
	      |  upgradeVersion(filename, '3.00') with current version 8
	      V
	 ====================================================================
	||	 ________title__________  ______description___________          ||
	|| | dc.title | exif.title || exif.subject |  exif.desc   |  vers 8 ||
	|| |   Sassy  |   Sassy    ||    Null      |    Null      |         ||
	 ====================================================================
	"""
	pass
	
def compareKeyValues(p_filename): 		#merge?
	#in case of leftover key/val from downgrade
	#check during upgrade
	pass

def futureCompatibleMark():
	#I don't even know if this should be it's own function
	#this is just a reminder that if you're editting a compatible tag of a future version'd file.
	#This is why level 0 should not add a mark with the current version after every set operation



#versionNotFound		exception		for when file has an invalid version (one we don't know about )