#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import codecs
import sys
from build import buildPosts

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
buildPosts("static", "static", "static", "")