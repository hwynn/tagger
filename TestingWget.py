#!/usr/bin/env python3
import wget
import os
url = 'https://i.kym-cdn.com/entries/icons/original/000/025/212/isopodsss.jpg'
outpath = '/home/hwynn/Pictures'
filename = wget.download(url,outpath)
print(filename)
os.remove(filename)


def tagSetTest(p_filename, p_fileURL, p_tag, p_postExpt):
    return