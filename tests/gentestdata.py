# generate-sitemap: Github action for automating sitemap generation
# 
# Copyright (c) 2020-2022 Vincent A Cicirello
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

if __name__ == "__main__" :
    
    beginning = """<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=utf-8>
<link rel="canonical" href="https://SOME.WEBSITE.WOULD.GO.HERE....">

"""
    
    ending = """

<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="title" content="Title Goes HERE">
</head>
<body>
</body>
</html>
"""
    
    noindex = """

<meta name="robots" content="noindex">

"""

    nonCharData = [ x for x in range(128, 256) ]

    with open("badCharsNoindex1.html", "w") as f :
        f.write(beginning)
        f.write(noindex)
    with open("badCharsNoindex1.html", "ab") as f :
        f.write(bytes(nonCharData))
    with open("badCharsNoindex1.html", "a") as f :
        f.write(ending)

    with open("badCharsNoindex2.html", "w") as f :
        f.write(beginning)
    with open("badCharsNoindex2.html", "ab") as f :
        f.write(bytes(nonCharData))
    with open("badCharsNoindex2.html", "a") as f :
        f.write(noindex)
        f.write(ending)

    with open("badCharsDoIndex.html", "w") as f :
        f.write(beginning)
    with open("badCharsDoIndex.html", "ab") as f :
        f.write(bytes(nonCharData))
    with open("badCharsDoIndex.html", "a") as f :
        f.write(ending)
