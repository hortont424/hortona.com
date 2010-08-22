#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import datetime
import os
import json
import codecs
import string
import re
import sys
from genshi.template import TemplateLoader
from genshi.core import Markup
from settings import *

loader = TemplateLoader('templates', variable_lookup='lenient')

def generatePostName(title):
    return re.sub("^-*", "", re.sub("--+", "-", re.sub("[^a-z0-9\-]", "", re.sub("\s","-", re.sub("<[^>]*>", "", re.sub(u"α ↔ ω", "alphaomega", title.lower()))))))

def readFileContents(fn):
    fileHandle = codecs.open(fn, encoding='utf-8')
    fileContents = unicode(fileHandle.read())
    fileHandle.close()
    return fileContents

def resolveCategoryList(cats):
    cats.sort()
    return [("<a href='" + os.path.join(blog_prefix, "topics/", categoryURLFromName(cat)) + "'>" + categoryDisplayName(cat) + "</a>") for cat in cats]

def joinCategoryList(cats):
    if len(cats) <= 2:
        return string.join(cats, " and ")
    else:
        return string.join(cats[:-2], ", ") + ", " + string.join(cats[-2:], ", and ")

def renderPost(f, template, rss=False):
    metadata = json.loads(readFileContents(f), encoding='utf-8')
    contents = readFileContents(f.replace(".control",""))
    contents = re.sub('\n\s*\n', "<br/><br/>", contents)

    if "template" not in metadata:
        metadata["template"] = template

    try:
        metadata["categories"] = joinCategoryList(resolveCategoryList(metadata["categories"]))
    except:
        metadata["categories"] = ""

    metadata["content"] = contents

    pubDate = metadata["date"]

    if "post-name" not in metadata:
        metadata["post-name"] = generatePostName(metadata["title"])

    if template is not "static":
        metadata["url"] = os.path.join(blog_prefix, metadata["post-name"])
    else:
        metadata["url"] = os.path.join(blog_prefix, f.replace(".control",".html"))

    metadata["id"] = re.sub("[^0-9]", "", metadata["date"])
    metadata["date"] = datetime.datetime.strptime(pubDate, "%Y.%m.%d %H:%M:%S").strftime("%Y.%m.%d")

    metadata["shortContent"] = re.sub("<(.*?)>","",contents[0:500]) + "..."

    if "pubDate" not in metadata:
        metadata["pubDate"] = datetime.datetime.strptime(pubDate, "%Y.%m.%d %H:%M:%S").strftime("%a, %d %b %Y %H:%M:%S +0000")

    if "guid" not in metadata:
        metadata["guid"] = metadata["url"]

    if "noChrome" not in metadata:
        metadata["noChrome"] = 0

    try:
        comments = metadata["comments"]
    except:
        metadata["comments"] = comments = []

    for c in comments:
        c["content"] = re.sub('\\n', "<br/>", c["content"])

    postfix = doctype = "html"
    if rss:
        postfix = "xml"
        doctype = None

    tmpl = loader.load(metadata["template"] + '.' + postfix, encoding='utf-8')
    return tmpl.generate(post=metadata,
                         baseurl=www_prefix,
                         staticurl=static_prefix,
                         blogurl=blog_prefix).render(postfix, doctype=doctype)

def renderArchive(c, template, next, prev, rss=False, category=None):
    postfix = doctype = "html"
    if rss:
        postfix = "xml"
        doctype = None

    buildDate = datetime.datetime.today().strftime("%a, %d %b %Y %H:%M:%S +0000")

    title = u"hortona &middot; blog"
    if category:
        title = u"hortona &middot; blog &middot; " + categoryDisplayName(category)

    showTitle = (category != None)

    rssurl = os.path.join(blog_prefix, "feed/rss.xml")
    if category:
        rssurl = os.path.join(blog_prefix, "topics", category, "feed/rss.xml")

    tmpl = loader.load(template + '.' + postfix, encoding='utf-8')
    return tmpl.generate(content=c.decode("utf-8","ignore"),
                         baseurl=www_prefix,
                         staticurl=static_prefix,
                         blogurl=blog_prefix,
                         nextPage=next,
                         previousPage=prev,
                         buildDate=buildDate,
                         title=title,
                         showTitle=showTitle,
                         rssurl=rssurl).render(postfix, doctype=doctype)