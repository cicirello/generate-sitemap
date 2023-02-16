#!/usr/bin/env -S python3 -B
#
# generate-sitemap: Github action for automating sitemap generation
# 
# Copyright (c) 2020-2023 Vincent A Cicirello
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
from datetime import datetime

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

INDEX_FILENAMES = { "index.html", "index.shtml" }

def sortname(f, dropExtension=False) :
    """Partial url to sort by, which strips out the filename
    if the filename is index.html.

    Keyword arguments:
    f - Filename with path
    dropExtension - true to drop extensions of .html from the filename when sorting
    """
    slash = f.rfind("/")
    if slash >= 0 and slash < len(f)-1 and f[slash+1:] in INDEX_FILENAMES :
        return f[:slash+1]
    elif f in INDEX_FILENAMES :
        return ""
    elif dropExtension and len(f) >= 5 and f[-5:] == ".html" :
        return f[:-5]
    else :
        return f

def urlsort(files, dropExtension=False) :
    """Sorts the urls with a primary sort by depth in the website,
    and a secondary sort alphabetically.

    Keyword arguments:
    files - list of files to include in sitemap
    dropExtension - true to drop extensions of .html from the filename when sorting
    """
    files.sort(key = lambda f : sortname(f, dropExtension))
    files.sort(key = lambda f : f.count("/"))


RE_FLAGS = re.I | re.M | re.S
RE_META_TAG = re.compile(r"<meta([^>]*)>", flags=RE_FLAGS)

def hasMetaRobotsNoindex(f) :
    """Checks whether an html file contains
    <meta name="robots" content="noindex"> or
    any equivalent directive including a noindex.
    Only checks head of html since required to be
    in the head if specified.

    Keyword arguments:
    f - Filename including path
    """
    try:
        with open(f, "r", errors="surrogateescape") as file :
            contents = file.read()
            m = re.search("</head>", contents, flags=re.I)
            if not m :
                m = re.search("<body>", contents, flags=re.I)
            all_meta_tags = RE_META_TAG.findall(contents, endpos=m.start()) if m else RE_META_TAG.findall(contents)
            for tag in all_meta_tags :
                if re.search("name\s*=\s*\"\s*robots", tag, flags=re.I) and re.search("content\s*=\s*\".*noindex", tag, flags=re.I) :
                    return True
            return False
    except OSError:
        print("WARNING: OS error while checking for noindex directive in:", f)
        print("Assuming", f, "doesn't have noindex directive.")
    return False


def getFileExtension(f) :
    """Gets the file extension, and returns it (in all
    lowercase). Returns None if file has no extension.

    Keyword arguments:
    f - file name possibly with path
    """
    i = f.rfind(".")
    return f[i+1:].lower() if i >= 0 and f.rfind("/") < i else None

HTML_EXTENSIONS = { "html", "htm", "shtml" }

def isHTMLFile(f) :
    """Checks if the file is an HTML file,
    which currently means has an extension of html
    or htm.

    Keyword arguments:
    f - file name including path relative from the root of the website.
    """
    return getFileExtension(f) in HTML_EXTENSIONS

def createExtensionSet(includeHTML, includePDF, additionalExt) :
    """Creates a set of file extensions for the file types to include
    in the sitemap.

    Keyword arguments:
    includeHTML - boolean, which if true indicates that all html related extensions
        should be included.
    includePDF - boolean, which if true results in inclusion of the extension pdf
    additionalExt - a set of additional file extensions to include
    """
    if includeHTML :
        fileExtensionsToInclude = additionalExt | HTML_EXTENSIONS
    else :
        fileExtensionsToInclude = additionalExt
        
    if includePDF :
        fileExtensionsToInclude.add("pdf")
    
    return fileExtensionsToInclude
    
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
    try:
        if os.path.isfile(robotsFile) :
            with open(robotsFile, "r", errors="surrogateescape") as robots :
                foundBlock = False
                rulesStart = False
                for line in robots :
                    commentStart = line.find("#")
                    if commentStart > 0 :
                        line = line[:commentStart]
                    line = line.strip()
                    lineLow = line.lower()
                    if lineLow.startswith("user-agent:") :
                        if len(line)>11 and line[11:].strip() == "*" :
                            foundBlock = True
                            rulesStart = False
                        elif rulesStart :
                            foundBlock = False
                            rulesStart = False
                    elif foundBlock :
                        if lineLow.startswith("allow:") :
                            rulesStart = True
                        elif lineLow.startswith("disallow:") :
                            rulesStart = True
                            if len(line) > 9 :
                                path = line[9:].strip()
                                if len(path) > 0 and " " not in path and "\t" not in path:
                                    blockedPaths.append(path)
    except OSError:
        print("WARNING: OS error while parsing robots.txt")
        print("Assuming nothing disallowed.")
    return blockedPaths

def lastmod(f) :
    """Determines the date when the file was last modified and
    returns a string with the date formatted as required for
    the lastmod tag in an xml sitemap.

    Keyword arguments:
    f - filename
    """
    mod = subprocess.run(['git', 'log', '-1', '--format=%cI', f],
                    stdout=subprocess.PIPE,
                    universal_newlines=True).stdout.strip()
    if len(mod) == 0 :
        mod = datetime.now().astimezone().replace(microsecond=0).isoformat()
    return mod

def urlstring(f, baseUrl, dropExtension=False) :
    """Forms a string with the full url from a filename and base url.

    Keyword arguments:
    f - filename
    baseUrl - address of the root of the website
    dropExtension - true to drop extensions of .html from the filename in urls
    """
    if f[0]=="." :
        u = f[1:]
    else :
        u = f
    u = sortname(u, dropExtension)
    if len(u) >= 1 and u[0]=="/" and len(baseUrl) >= 1 and baseUrl[-1]=="/" :
        u = u[1:]
    elif (len(u)==0 or u[0]!="/") and (len(baseUrl)==0 or baseUrl[-1]!="/") :
        u = "/" + u
    return baseUrl + u

xmlSitemapEntryTemplate = """<url>
<loc>{0}</loc>
<lastmod>{1}</lastmod>
</url>"""	

def removeTime(dateString) :
    """Removes the time from a date-time.

    Keyword arguments:
    dateString - The date-time.
    """
    return dateString[:10]

def xmlSitemapEntry(f, baseUrl, dateString, dropExtension=False, dateOnly=False) :
    """Forms a string with an entry formatted for an xml sitemap
    including lastmod date.

    Keyword arguments:
    f - filename
    baseUrl - address of the root of the website
    dateString - lastmod date correctly formatted
    dropExtension - true to drop extensions of .html from the filename in urls
    """
    return xmlSitemapEntryTemplate.format(
        urlstring(f, baseUrl, dropExtension),
        removeTime(dateString) if dateOnly else dateString
    )

def writeTextSitemap(files, baseUrl, dropExtension=False) :
    """Writes a plain text sitemap to the file sitemap.txt.

    Keyword Arguments:
    files - a list of filenames
    baseUrl - the base url to the root of the website
    dropExtension - true to drop extensions of .html from the filename in urls
    """
    with open("sitemap.txt", "w") as sitemap :
        for f in files :
            sitemap.write(urlstring(f, baseUrl, dropExtension))
            sitemap.write("\n")
            
def writeXmlSitemap(files, baseUrl, dropExtension=False, dateOnly=False) :
    """Writes an xml sitemap to the file sitemap.xml.

    Keyword Arguments:
    files - a list of filenames
    baseUrl - the base url to the root of the website
    dropExtension - true to drop extensions of .html from the filename in urls
    """
    with open("sitemap.xml", "w") as sitemap :
        sitemap.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        sitemap.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for f in files :
            sitemap.write(xmlSitemapEntry(f, baseUrl, lastmod(f), dropExtension, dateOnly))
            sitemap.write("\n")
        sitemap.write('</urlset>\n')

def set_outputs(names_values) :
    """Sets the GitHub Action outputs.

    Keyword arguments:
    names_values - Dictionary of output names with values
    """
    if "GITHUB_OUTPUT" in os.environ :
        with open(os.environ["GITHUB_OUTPUT"], "a") as f :
            for name, value in names_values.items() :
                print("{0}={1}".format(name, value), file=f)
    else : # Fall-back to deprecated set-output for non-updated runners
        for name, value in names_values.items() :
            print("::set-output name={0}::{1}".format(name, value))

def main(
        websiteRoot,
        baseUrl,
        includeHTML,
        includePDF,
        sitemapFormat,
        additionalExt,
        dropExtension,
        dateOnly
    ) :
    """The main function of the generate-sitemap GitHub Action.

    Keyword arguments:
    websiteRoot - The path to the root of the website relative
            to the root of the repository.
    baseUrl - The URL of the website.
    includeHTML - A boolean that controls whether to include HTML
            files in the sitemap.
    includePDF - A boolean that controls whether to include PDF
            files in the sitemap.
    sitemapFormat - A string either: xml or txt.
    additionalExt - A set of additional user-defined filename
            extensions for inclusion in the sitemap.
    dropExtension - A boolean that controls whether to drop .html from
            URLs that are to html files (e.g., GitHub Pages will serve
            an html file if URL doesn't include the .html extension).
    """
    repo_root = os.getcwd()
    safe_path = os.path.realpath(websiteRoot)
    prefix = os.path.commonpath([repo_root, safe_path])
    if prefix == repo_root :
        os.chdir(safe_path)
    else :
        print("ERROR: Specified website root directory appears to be outside of current working directory. Exiting....")
        exit(1)
    blockedPaths = parseRobotsTxt()
    
    allFiles = gatherfiles(createExtensionSet(includeHTML, includePDF, additionalExt))
    files = [ f for f in allFiles if not robotsBlocked(f, blockedPaths) ]
    urlsort(files, dropExtension)

    pathToSitemap = websiteRoot
    if pathToSitemap[-1] != "/" :
        pathToSitemap += "/"
    if sitemapFormat == "xml" :
        writeXmlSitemap(files, baseUrl, dropExtension, dateOnly)
        pathToSitemap += "sitemap.xml"
    else :
        writeTextSitemap(files, baseUrl, dropExtension)
        pathToSitemap += "sitemap.txt"

    set_outputs({
        "sitemap-path" : pathToSitemap,
        "url-count" : len(files),
        "excluded-count" : len(allFiles)-len(files)
    })

if __name__ == "__main__" :
    main(
        websiteRoot = sys.argv[1],
        baseUrl = sys.argv[2],
        includeHTML = sys.argv[3].lower() == "true",
        includePDF = sys.argv[4].lower() == "true",
        sitemapFormat = sys.argv[5],
        additionalExt = set(sys.argv[6].lower().replace(",", " ").replace(".", " ").split()),
        dropExtension = sys.argv[7].lower() == "true",
        dateOnly = sys.argv[8].lower() == "true"
    )

    
