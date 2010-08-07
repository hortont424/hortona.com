#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import os
import sys
import codecs

from settings import *
from renderer import readFileContents

for root, dirs, files in os.walk(sys.argv[1]):
    for filename in files:
        f = os.path.join(root, filename)
        
        if filename.startswith("."):
            continue
        
        data = readFileContents(f)
        data = data.replace("${baseurl}", www_prefix)
        data = data.replace("${staticurl}", static_prefix)
        
        out = codecs.open(f, encoding='utf-8', mode='w+')
        out.write(data)
        out.close()