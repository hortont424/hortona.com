#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import sys
import string
import urllib2
from BaseHTTPServer import *
from renderer import *
from BeautifulSoup import *

def urlResponseCode(url):
    req = urllib2.Request(url)
    req.add_header("User-agent", "Mozilla/5.0") # Silly wikipedia blocks urllib2
    try:
        urllib2.urlopen(req)
    except urllib2.URLError, e:
        try:
            return e.code
        except AttributeError, f:
            return None # mailto, js, etc.
    except ValueError, e:
        #print "Unknown URL type:", url
        return None # relative URLs. might be good to fix at some point
    return None

def testLinks():
    for root, dirs, files in os.walk("output/blog"):
        for filename in files:
            f = os.path.join(root, filename)
            if not f.endswith(".html"):
                continue

            soup = BeautifulSoup(readFileContents(f))
            anchors = soup.findAll('a')
            for a in anchors:
                link = a['href']
                rc = urlResponseCode(link)
                if rc:
                    print link, rc, f

testLinks()