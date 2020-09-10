#!/usr/bin/env python3
#
# generate-sitemap: Github action for automating sitemap generation
# 
# Copyright (c) 2020 Vincent A Cicirello
# https://www.cicirello.org/
#
# MIT License
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

import sys
import re
import os

def gatherfiles(html, pdf) :
    if not html and not pdf :
        return []
    allfiles = []
    for root, dirs, files in os.walk(".") :
        for f in files :
            if html and len(f) >= 5 and ".html" == f[-5:] :
                allfiles.append(os.path.join(root, f))
            elif html and len(f) >= 4 and ".htm" == f[-4:] :
                allfiles.append(os.path.join(root, f))
            elif pdf and len(f) >= 4 and ".pdf" == f[-4:] :
                allfiles.append(os.path.join(root, f))
    return allfiles

def sortname(f) :
    """Partial url to sort by, which strips out the filename
    if the filename is index.html.

    Keyword arguments:
    f - Filename with path
    """
    if len(f) >= 10 and f[-10:] == "index.html" :
        return f[:-10]
    else :
        return f

def urlsort(files) :
    """Sorts the urls with a primary sort by depth in the website,
    and a secondary sort alphabetically.

    Keyword arguments:
    files - list of files to include in sitemap
    """
    files.sort(key = lambda f : sortname(f))
    files.sort(key = lambda s : s.count("/"))

def hasMetaRobotsNoindex(f) :
    """Checks whether an html file contains
    <meta name="robots" content="noindex"> or
    any equivalent directive including a noindex.
    Only checks head of html since required to be
    in the head if specified.

    Keyword arguments:
    f - Filename including path
    """
    with open(f,"r") as file :
        for line in file :
            # Check line for <meta name="robots" content="noindex">, etc
            if re.search("<meta\s+name.+robots.+content.+noindex", line) != None :
                return True
            # We can stop searching once no longer in head of file.
            # <meta name="robots"> directives required to be in head
            if "<body>" in line or "</head>" in line :
                return False
    return False

def robotsBlocked(f) :
    """Checks if robots are blocked from acessing the
    url.

    Keyword arguments:
    f - file name including path relative from the root of the website.
    """
    # For now, we let all pdfs through if included
    # since we are not yet parsing robots.txt.
    # Once robots.txt is supported, we'll check pdfs
    # against robots.txt.
    if len(f) >= 4 and f[-4:] == ".pdf" :
        return False
    return hasMetaRobotsNoindex(f)

if __name__ == "__main__" :
    allFiles = gatherfiles(sys.argv[1]=="true", sys.argv[2]=="true")
    files = [ f for f in allFiles if not robotsBlocked(f) ]
    urlsort(files)
    for f in files :
        print(f)
    print("RobotsBlockedCount:",len(allFiles)-len(files))
