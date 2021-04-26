#!/usr/bin/env python3
#
# generate-sitemap: Github action for automating sitemap generation
# 
# Copyright (c) 2021 Vincent A Cicirello
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
import os.path
import subprocess

def gatherfiles(extensionsToInclude) :
    """Walks the directory tree discovering
    files of specified types for inclusion in
    sitemap.

    Keyword arguments:
    extensionsToInclude - a set of the file extensions to include in sitemap
    """
    if len(extensionsToInclude) == 0 :
        return []
    allfiles = []
    for root, dirs, files in os.walk(".") :
        for f in files :
            if getFileExtension(f) in extensionsToInclude :
                allfiles.append(os.path.join(root, f))
    return allfiles

def sortname(f) :
    """Partial url to sort by, which strips out the filename
    if the filename is index.html.

    Keyword arguments:
    f - Filename with path
    """
    if len(f) >= 11 and f[-11:] == "/index.html" :
        return f[:-10]
    elif f == "index.html" :
        return ""
    else :
        return f

def urlsort(files) :
    """Sorts the urls with a primary sort by depth in the website,
    and a secondary sort alphabetically.

    Keyword arguments:
    files - list of files to include in sitemap
    """
    files.sort(key = lambda f : sortname(f))
    files.sort(key = lambda f : f.count("/"))

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

def getFileExtension(f) :
    """Gets the file extension, and returns it (in all
    lowercase). Returns None if file has no extension.

    Keyword arguments:
    f - file name possibly with path
    """
    i = f.rfind(".")
    return f[i+1:] if i >= 0 and f.rfind("/") < i else None

HTML_EXTENSIONS = { "html", "htm" }

def isHTMLFile(f) :
    """Checks if the file is an HTML file,
    which currently means has an extension of html
    or htm.

    Keyword arguments:
    f - file name including path relative from the root of the website.
    """
    return getFileExtension(f) in HTML_EXTENSIONS
    
def robotsBlocked(f, blockedPaths=[]) :
    """Checks if robots are blocked from acessing the
    url.

    Keyword arguments:
    f - file name including path relative from the root of the website.
    blockedPaths - a list of paths blocked by robots.txt
    """
    if len(blockedPaths) > 0 :
        f2 = f
        if f2[0] == "." :
            f2 = f2[1:]
        for b in blockedPaths :
            if f2.startswith(b) :
                return True
    if not isHTMLFile(f) : 
        return False
    return hasMetaRobotsNoindex(f)

def parseRobotsTxt(robotsFile="robots.txt") :
    """Parses a robots.txt if present in the root of the
    site, and returns a list of disallowed paths. It only
    includes paths disallowed for *.

    Keyword arguments:
    robotsFile - the name of the robots.txt, which in production
    must be robots.txt (the default). The parameter is to enable
    unit testing with different robots.txt files."""
    blockedPaths = []
    if os.path.isfile(robotsFile) :
        with open(robotsFile,"r") as robots :
            foundBlock = False
            rulesStart = False
            for line in robots :
                commentStart = line.find("#")
                if commentStart > 0 :
                    line = line[:commentStart]
                line = line.strip()
                lineLow = line.lower()
                if foundBlock :
                    if rulesStart and lineLow.startswith("user-agent:") :
                        foundBlock = False
                    elif not rulesStart and lineLow.startswith("allow:") :
                        rulesStart = True
                    elif lineLow.startswith("disallow:") :
                        rulesStart = True
                        if len(line) > 9 :
                            path = line[9:].strip()
                            if len(path) > 0 and " " not in path and "\t" not in path:
                                blockedPaths.append(path)
                elif lineLow.startswith("user-agent:") and len(line)>11 and line[11:].strip() == "*" :
                    foundBlock = True
                    rulesStart = False
    return blockedPaths

def lastmod(f) :
    """Determines the date when the file was last modified and
    returns a string with the date formatted as required for
    the lastmod tag in an xml sitemap.

    Keyword arguments:
    f - filename
    """
    return subprocess.run(['git', 'log', '-1', '--format=%cI', f],
                    stdout=subprocess.PIPE,
                    universal_newlines=True).stdout.strip()

def urlstring(f, baseUrl) :
    """Forms a string with the full url from a filename and base url.

    Keyword arguments:
    f - filename
    baseUrl - address of the root of the website
    """
    if f[0]=="." :
        u = f[1:]
    else :
        u = f
    if len(u) >= 11 and u[-11:] == "/index.html" :
        u = u[:-10]
    elif u == "index.html" :
        u = ""
    if len(u) >= 1 and u[0]=="/" and len(baseUrl) >= 1 and baseUrl[-1]=="/" :
        u = u[1:]
    elif (len(u)==0 or u[0]!="/") and (len(baseUrl)==0 or baseUrl[-1]!="/") :
        u = "/" + u
    return baseUrl + u

xmlSitemapEntryTemplate = """<url>
<loc>{0}</loc>
<lastmod>{1}</lastmod>
</url>"""	
	
def xmlSitemapEntry(f, baseUrl, dateString) :
    """Forms a string with an entry formatted for an xml sitemap
    including lastmod date.

    Keyword arguments:
    f - filename
    baseUrl - address of the root of the website
    dateString - lastmod date correctly formatted
    """
    return xmlSitemapEntryTemplate.format(urlstring(f, baseUrl), dateString)

def writeTextSitemap(files, baseUrl) :
    """Writes a plain text sitemap to the file sitemap.txt.

    Keyword Arguments:
    files - a list of filenames
    baseUrl - the base url to the root of the website
    """
    with open("sitemap.txt", "w") as sitemap :
        for f in files :
            sitemap.write(urlstring(f, baseUrl))
            sitemap.write("\n")
            
def writeXmlSitemap(files, baseUrl) :
    """Writes an xml sitemap to the file sitemap.xml.

    Keyword Arguments:
    files - a list of filenames
    baseUrl - the base url to the root of the website
    """
    with open("sitemap.xml", "w") as sitemap :
        sitemap.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        sitemap.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for f in files :
            sitemap.write(xmlSitemapEntry(f, baseUrl, lastmod(f)))
            sitemap.write("\n")
        sitemap.write('</urlset>\n')

if __name__ == "__main__" :
    websiteRoot = sys.argv[1]
    baseUrl = sys.argv[2]
    includeHTML = sys.argv[3]=="true"
    includePDF = sys.argv[4]=="true"
    sitemapFormat = sys.argv[5]

    fileExtensionsToInclude = HTML_EXTENSIONS.copy() if includeHTML else set()
    if includePDF :
        fileExtensionsToInclude.add("pdf")

    os.chdir(websiteRoot)
    blockedPaths = parseRobotsTxt()
    
    allFiles = gatherfiles(fileExtensionsToInclude)
    files = [ f for f in allFiles if not robotsBlocked(f, blockedPaths) ]
    urlsort(files)

    pathToSitemap = websiteRoot
    if pathToSitemap[-1] != "/" :
        pathToSitemap += "/"
    if sitemapFormat == "xml" :
        writeXmlSitemap(files, baseUrl)
        pathToSitemap += "sitemap.xml"
    else :
        writeTextSitemap(files, baseUrl)
        pathToSitemap += "sitemap.txt"

    print("::set-output name=sitemap-path::" + pathToSitemap)
    print("::set-output name=url-count::" + str(len(files)))
    print("::set-output name=excluded-count::" + str(len(allFiles)-len(files)))
