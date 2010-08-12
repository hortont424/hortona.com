import os

page_size = 10

www_prefix = "http://www.hortona.com/"
static_prefix = "http://files.hortona.com/www/"

if os.getcwd() == "/Users/hortona/Sites":
    www_prefix = "http://localhost/~hortona/output/"
    static_prefix = "http://localhost/~hortona/output/"

if os.getcwd() == "/Users/hortont/src/hortona.com":
    www_prefix = "http://localhost/~hortont/amy/"
    static_prefix = "http://localhost/~hortont/amy/"

blog_dir = ""

blog_prefix = www_prefix + blog_dir

def w(u):
    return www_prefix + u

def categoryURLFromName(n):
    return n

def categoryDisplayName(n):
    return n.replace("-"," ")