#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# I LOVE IT WHEN I USE REGEX TO "PARSE" XML. OH WAIT NO.

# THIS FILE IS VOODOO

import sys
import os
import codecs
import re
import datetime
import time
import string
import json

def readFileContents(fn):
    fileHandle = codecs.open(fn, encoding='utf-8')
    fileContents = fileHandle.read()
    fileHandle.close()
    return fileContents

def parseItemCategories(s):
    while True:
        cat = re.search("<category domain=\"category\" nicename=\"(.*)\">", s)
        if cat == None:
            break
        else:
            s = s[:cat.start()] + s[cat.end():]
            yield cat.groups(1)[0]

def parseWordpressExport(filename):
    for post in readFileContents(filename).split("<item>"):
        title = re.search("<title>([^\<]*)</title>", post).groups(1)[0]
        content = ""
        
        try:
            content = re.compile("<content:encoded><!\[CDATA\[(.*)\]\]></content:encoded>", re.M | re.S).search(post).groups(1)[0]
        except:
            print "Skipped One..."
            continue
        
        pubDate = date = re.compile("<pubDate>(.*)......</pubDate>").search(post).groups(1)[0]
        date = datetime.datetime.strptime(date, "%a, %d %b %Y %H:%M:%S").strftime("%Y.%m.%d %H:%M:%S")
        
        if re.search("1999", date) != None: # special case
            continue
        
        postName = re.compile("<wp:post_name>(.*)</wp:post_name>").search(post).groups(1)[0]
        guid = re.compile("<guid.*>(.*)</guid>").search(post).groups(1)[0]
        author = "Tim"
        template = "single-column"
        categories = list(parseItemCategories(post))
        
        # Comment parsing
        
        comments = re.compile("<wp:comment>(.*?)</wp:comment>", re.M | re.S).search(post)
        commentList = []
        while comments is not None:
            commentstr = comments.groups(1)[0]
            commentAuthor = re.search("<wp:comment_author><!\[CDATA\[(.*)\]\]></wp:comment_author>", commentstr).groups(1)[0]
            commentAuthorURLS = re.search("<wp:comment_author_url>(.*)</wp:comment_author_url>", commentstr)
            commentAuthorURL = ""
            if commentAuthorURLS is not None:
                commentAuthorURL = commentAuthorURLS.groups(1)[0]
            commentContent = re.compile("<wp:comment_content><!\[CDATA\[(.*)\]\]></wp:comment_content>", re.M | re.S).search(commentstr).groups(1)[0]
            commentList.append({"author":commentAuthor, "authorURL": commentAuthorURL, "content": commentContent})
            comments = re.compile("<wp:comment>(.*?)</wp:comment>", re.M | re.S).search(post, comments.end())
    
        yield {"title": title, "content": content, "date": date, "post-name": postName, "guid": guid, "categories": categories, "author": author, "template": template, "pubDate": pubDate, "comments": commentList}

def savePost(p):
    content = p["content"]
    del p["content"]
    filename = p["date"]
    filename = os.path.join("posts", re.sub(":","", re.sub("[\.\s]","/", filename)))
    
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    
    controlFile = codecs.open(filename + ".control", encoding='utf-8', mode='w+')
    json.dump(p, controlFile, indent=4)
    controlFile.close()
    dataFile = codecs.open(filename, encoding='utf-8', mode='w+')
    dataFile.write(content)
    dataFile.close()

def main(argv):
    map(savePost, list(parseWordpressExport(argv[0])))

if __name__ == "__main__":
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main(sys.argv[1:])