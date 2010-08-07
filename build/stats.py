import os
from settings import *
from build import generateCategoryMap

def getOutputStats():
    totalSize = totalCount = 0
    for root, dirs, files in os.walk("output"):
        for filename in files:
            f = os.path.join(root, filename)
            totalSize += os.stat(f).st_size
            totalCount += 1
    return (totalSize, totalCount)

size, count = getOutputStats()
catMap = generateCategoryMap("posts")
cats = [(len(catMap[x]), categoryDisplayName(x)) for x in catMap]
cats.sort(reverse=True)

print "----------------------"
print "                totals"
print "----------------------"
print "%19d KB" % (size / 1024)
print "%16d files" % count
print "----------------------"
print "            categories"
print "----------------------"
print "\n".join(["%16s (%3d)" % (c, s) for (s, c) in cats])