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

import unittest
import generatesitemap as gs
import os

class TestGenerateSitemap(unittest.TestCase) :

    def test_sortname(self) :
        files = [ "/dir/dir/z.pdf", 
                    "/dir/yoohoo.html",
                    "/x.pdf",
                    "/2.html",
                    "/dir/dir/b.html",
                    "/index.html",
                    "/dir/dir/a.html",
                    "/dir/y.pdf",
                    "/dir/hello.html",
                    "/1.html",
                    "/dir/dir/index.html",
                    "/dir/index.html",
                    "/dir/dir/d.html",
                    "/dir/goodbye.html",
                    "/dir/dir/c.html" ]
        expected = [ "/dir/dir/z.pdf", 
                    "/dir/yoohoo.html",
                    "/x.pdf",
                    "/2.html",
                    "/dir/dir/b.html",
                    "/",
                    "/dir/dir/a.html",
                    "/dir/y.pdf",
                    "/dir/hello.html",
                    "/1.html",
                    "/dir/dir/",
                    "/dir/",
                    "/dir/dir/d.html",
                    "/dir/goodbye.html",
                    "/dir/dir/c.html" ]
        for i, f in enumerate(files) :
            self.assertEqual(gs.sortname(f), expected[i])

    def test_urlsort(self) :
        files = [ "/dir/dir/z.pdf", 
                    "/dir/yoohoo.html",
                    "/x.pdf",
                    "/2.html",
                    "/dir/dir/b.html",
                    "/index.html",
                    "/dir/dir/a.html",
                    "/dir/y.pdf",
                    "/dir/hello.html",
                    "/1.html",
                    "/dir/dir/index.html",
                    "/dir/index.html",
                    "/dir/dir/d.html",
                    "/dir/goodbye.html",
                    "/dir/dir/c.html" ]
        expected = [ "/index.html",
                     "/1.html",
                     "/2.html",
                     "/x.pdf",
                     "/dir/index.html",
                     "/dir/goodbye.html",
                     "/dir/hello.html",
                     "/dir/y.pdf",
                     "/dir/yoohoo.html",
                     "/dir/dir/index.html",
                     "/dir/dir/a.html",
                     "/dir/dir/b.html",
                     "/dir/dir/c.html",
                     "/dir/dir/d.html",
                     "/dir/dir/z.pdf" ]
        gs.urlsort(files)
        self.assertEqual(files, expected)
        
    def test_robotsBlocked(self) :
        unblocked = [ "/x.pdf",
                      "/dir/y.pdf",
                      "/dir/dir/z.pdf",
                      "tests/unblocked1.html",
                      "tests/unblocked2.html",
                      "tests/unblocked3.html",
                      "tests/unblocked4.html" ]
        blocked = [ "tests/blocked1.html",
                    "tests/blocked2.html",
                    "tests/blocked3.html",
                    "tests/blocked4.html" ]
        for f in unblocked :
            self.assertFalse(gs.robotsBlocked(f))
        for f in blocked :
            self.assertTrue(gs.robotsBlocked(f))

    def test_hasMetaRobotsNoindex(self) :
        unblocked = [ "tests/unblocked1.html",
                      "tests/unblocked2.html",
                      "tests/unblocked3.html",
                      "tests/unblocked4.html" ]
        blocked = [ "tests/blocked1.html",
                    "tests/blocked2.html",
                    "tests/blocked3.html",
                    "tests/blocked4.html" ]
        for f in unblocked :
            self.assertFalse(gs.hasMetaRobotsNoindex(f))
        for f in blocked :
            self.assertTrue(gs.hasMetaRobotsNoindex(f))

    def test_gatherfiles(self) :
        os.chdir("tests")
        allfiles = gs.gatherfiles(True, False)
        os.chdir("..")
        asSet = set(allfiles)
        print(asSet)
        expected = { "./blocked1.html", "./blocked2.html",
                     "./blocked3.html", "./blocked4.html",
                     "./unblocked1.html", "./unblocked2.html",
                     "./unblocked3.html", "./unblocked4.html",
                     "./subdir/a.html", "./subdir/subdir/b.html"}
        self.assertEqual(asSet, expected)

