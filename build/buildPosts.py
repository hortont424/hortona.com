#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import codecs
import sys
import os
from build import buildPosts, buildBackwardsCompatibilityLinks
from settings import *

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
buildPosts("posts", "post", "post", os.path.join(blog_dir, "posts"))
buildBackwardsCompatibilityLinks("posts")