#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
import codecs
import string
import datetime
from renderer import *
from build import *
import settings

controlTemplate = """{
    "author": "Amy",
    "title": "",
    "date": "%(y)04d.%(m)02d.%(d)02d %(hr)02d:%(min)02d:%(sec)02d",
    "categories": [
    ]
}"""

def writeFile(filename, data):
    out = codecs.open(filename, encoding='utf-8', mode='w+')
    out.write(data)
    out.close()

def touchFile(filename):
    if not os.path.exists(filename):
        open(filename, 'w').close()

def createNewPost():
    (y,m,d,hr,min,sec,wday,yday,dst) = datetime.datetime.now().timetuple()

    filename = os.path.join("posts", str(y), "%(m)02d" % { "m":m },
                            "%(d)02d" % { "d":d },
                            "%(hr)02d%(min)02d%(sec)02d" % { "hr":hr, "min":min, "sec":sec })

    controlFileData = controlTemplate % {
        "hr":hr, "min":min, "sec":sec,
        "y":y, "m":m, "d":d
    }

    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))

    touchFile(filename)
    writeFile(filename + ".control", controlFileData)
    os.system("git add " + os.path.dirname(filename))
    os.system("$EDITOR " + filename + " " + filename + ".control")

if __name__ == "__main__":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    createNewPost()