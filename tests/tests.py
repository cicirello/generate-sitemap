# generate-sitemap: Github action for automating sitemap generation
# 
# Copyright (c) 2020-2024 Vincent A Cicirello
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

def validateDate(s) :
    if len(s) < 25 :
        return False
    if not s[0:4].isdigit() or s[4]!="-" or not s[5:7].isdigit() :
        return False
    if s[7]!="-" or not s[8:10].isdigit() or s[10]!="T" :
        return False
    if not s[11:13].isdigit() or s[13]!=":" or not s[14:16].isdigit() :
        return False
    if s[16]!=":" or not s[17:19].isdigit() or (s[19]!="-" and s[19]!="+"):
        return False
    if not s[20:22].isdigit() or s[22]!=":" or not s[23:25].isdigit() :
        return False
    return  True

class TestGenerateSitemap(unittest.TestCase) :

    def test_createExtensionSet_htmlOnly(self):
        self.assertEqual({"html", "htm", "shtml"}, gs.createExtensionSet(True, False, set()))

    def test_createExtensionSet_pdfOnly(self):
        self.assertEqual({"pdf"}, gs.createExtensionSet(False, True, set()))

    def test_createExtensionSet_htmlAndPdf(self):
        self.assertEqual({"html", "htm", "shtml", "pdf"}, gs.createExtensionSet(True, True, set()))

    def test_createExtensionSet_html_and_more(self):
        self.assertEqual({"html", "htm", "shtml", "abc"}, gs.createExtensionSet(True, False, {"abc"}))

    def test_createExtensionSet_pdf_and_more(self):
        self.assertEqual({"pdf", "abc", "def"}, gs.createExtensionSet(False, True, {"abc", "def"}))

    def test_createExtensionSet_htmlAndPdf_and_more(self):
        self.assertEqual({"html", "htm", "shtml", "pdf", "abc"}, gs.createExtensionSet(True, True, {"abc"}))

    def test_createExtensionSet_only_additional(self):
        self.assertEqual({"abc", "def"}, gs.createExtensionSet(False, False, {"abc", "def"}))

    def test_createExtensionSet_none(self):
        self.assertEqual(set(), gs.createExtensionSet(False, False, set()))

    def test_getFileExtension(self) :
        cases = [ ".html", ".htm",
                  "a.html", "a.htm",
                  "/.html", "/.htm",
                  "/a.html", "/a.htm",
                  "b/a.html", "b/a.htm",
                  "b/index.html", "b/index.htm",
                  "html", "htm",
                  "ahtml", "ahtm",
                  "/html", "/htm",
                  "/ahtml", "/ahtm",
                  "b/ahtml", "b/ahtm",
                  "b/indexhtml", "b/indexhtm",
                  ".something/somethingElse",
                  "some.thing/somethingElse",
                  "some.html/somethingElse",
                  ".something/somethingElse.doc",
                  "some.thing/somethingElse.doc",
                  "some.html/somethingElse.doc",
                  ".HTML", ".HTM",
                  "a.HTML", "a.HTM",
                  "/.HTML", "/.HTM",
                  "/a.HTML", "/a.HTM",
                  "b/a.HTML", "b/a.HTM",
                  "b/index.HTML", "b/index.HTM",
                  ".shtml",
                  "a.shtml",
                  "/.shtml",
                  "/a.shtml",
                  "b/a.shtml",
                  "b/index.shtml"
                  ]
        ext = [ "html", "htm",
                "html", "htm",
                "html", "htm",
                "html", "htm",
                "html", "htm",
                "html", "htm",
                None, None, None, None, None, None,
                None, None, None, None, None, None,
                None, None, None,
                "doc", "doc", "doc",
                "html", "htm",
                "html", "htm",
                "html", "htm",
                "html", "htm",
                "html", "htm",
                "html", "htm",
                "shtml", "shtml", "shtml", "shtml", "shtml", "shtml"
                ]
        for i, f in enumerate(cases) :
            self.assertEqual(ext[i], gs.getFileExtension(f), msg="failed on filename: "+f)

    def test_isHTMLFile(self) :
        htmlFilenames = [ ".html",
                          ".htm",
                          "a.html",
                          "a.htm",
                          "index.html",
                          "index.htm",
                          "/.html",
                          "/.htm",
                          "/a.html",
                          "/a.htm",
                          "/index.html",
                          "/index.htm",
                          "b/.html",
                          "b/.htm",
                          "b/a.html",
                          "b/a.htm",
                          "b/index.html",
                          "b/index.htm",
                          ".shtml",
                          "a.shtml",
                          "index.shtml",
                          "/.shtml",
                          "/a.shtml",
                          "/index.shtml",
                          "b/.shtml",
                          "b/a.shtml",
                          "b/index.shtml"
                          ]
        nonHtmlFilenames = [ ".0html",
                          ".0htm",
                          "indexhtml",
                          "indexhtm",
                          "html",
                          "htm",
                          "/html",
                          "/htm",
                          "a/html",
                          "a/htm",
                          "a.0html",
                          "a.0htm",
                          "a/b.0html",
                          "a/b.0htm",
                          "b/a.html0",
                          "b/a.htm0",
                          "b/index.html0",
                          "b/index.htm0"
                          ]
        for f in htmlFilenames :
            self.assertTrue(gs.isHTMLFile(f))
        for f in nonHtmlFilenames :
            self.assertFalse(gs.isHTMLFile(f))

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
                    "/dir/dir/c.html",
                    "/aindex.html",
                    "/dir/aindex.html",
                    "/dir/xyz.shtml",
                    "/3.shtml",
                    "/dir/dir/abc.shtml"
                  ]
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
                    "/dir/dir/c.html",
                    "/aindex.html",
                    "/dir/aindex.html",
                    "/dir/xyz.shtml",
                    "/3.shtml",
                    "/dir/dir/abc.shtml"
                  ]
        expectedDropHtml = [ "/dir/dir/z.pdf", 
                    "/dir/yoohoo",
                    "/x.pdf",
                    "/2",
                    "/dir/dir/b",
                    "/",
                    "/dir/dir/a",
                    "/dir/y.pdf",
                    "/dir/hello",
                    "/1",
                    "/dir/dir/",
                    "/dir/",
                    "/dir/dir/d",
                    "/dir/goodbye",
                    "/dir/dir/c",
                    "/aindex",
                    "/dir/aindex",
                    "/dir/xyz.shtml",
                    "/3.shtml",
                    "/dir/dir/abc.shtml"
                  ]
        for i, f in enumerate(files) :
            self.assertEqual(gs.sortname(f), expected[i])
        for i, f in enumerate(files) :
            self.assertEqual(gs.sortname(f, True), expectedDropHtml[i])

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
                    "/dir/dir/c.html",
                    "/dir/xyz.shtml",
                    "/3.shtml",
                    "/dir/dir/abc.shtml"
                  ]
        expected = [ "/index.html",
                     "/1.html",
                     "/2.html",
                     "/3.shtml",
                     "/x.pdf",
                     "/dir/index.html",
                     "/dir/goodbye.html",
                     "/dir/hello.html",
                     "/dir/xyz.shtml",
                     "/dir/y.pdf",
                     "/dir/yoohoo.html",
                     "/dir/dir/index.html",
                     "/dir/dir/a.html",
                     "/dir/dir/abc.shtml",
                     "/dir/dir/b.html",
                     "/dir/dir/c.html",
                     "/dir/dir/d.html",
                     "/dir/dir/z.pdf"
                     ]
        gs.urlsort(files)
        self.assertEqual(files, expected)

    def test_urlsort2(self) :
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
                    "/dir/dir/c.html",
                    "/dir/xyz.shtml",
                    "/3.shtml",
                    "/dir/dir/abc.shtml"
                  ]
        expected = [ "/index.html",
                     "/1.html",
                     "/2.html",
                     "/3.shtml",
                     "/x.pdf",
                     "/dir/index.html",
                     "/dir/goodbye.html",
                     "/dir/hello.html",
                     "/dir/xyz.shtml",
                     "/dir/y.pdf",
                     "/dir/yoohoo.html",
                     "/dir/dir/index.html",
                     "/dir/dir/a.html",
                     "/dir/dir/abc.shtml",
                     "/dir/dir/b.html",
                     "/dir/dir/c.html",
                     "/dir/dir/d.html",
                     "/dir/dir/z.pdf"
                   ]
        gs.urlsort(files, True)
        self.assertEqual(files, expected)
        
    def test_robotsBlocked(self) :
        unblocked = [ "/x.pdf",
                      "/dir/y.pdf",
                      "/dir/dir/z.pdf",
                      "tests/unblocked1.html",
                      "tests/unblocked2.html",
                      "tests/unblocked3.html",
                      "tests/unblocked4.html",
                      "tests/badCharsDoIndex.html"]
        blocked = [ "tests/blocked1.html",
                    "tests/blocked2.html",
                    "tests/blocked3.html",
                    "tests/blocked4.html",
                    "tests/badCharsNoindex1.html",
                    "tests/badCharsNoindex2.html",
                    "tests/blocked5.html",
                    "tests/blocked6.html"]
        for f in unblocked :
            self.assertFalse(gs.robotsBlocked(f))
        for f in blocked :
            self.assertTrue(gs.robotsBlocked(f))

    def test_hasMetaRobotsNoindex(self) :
        unblocked = [ "tests/unblocked1.html",
                      "tests/unblocked2.html",
                      "tests/unblocked3.html",
                      "tests/unblocked4.html",
                      "tests/badCharsDoIndex.html" ]
        blocked = [ "tests/blocked1.html",
                    "tests/blocked2.html",
                    "tests/blocked3.html",
                    "tests/blocked4.html",
                    "tests/badCharsNoindex1.html",
                    "tests/badCharsNoindex2.html",
                    "tests/blocked5.html",
                    "tests/blocked6.html"]
        for f in unblocked :
            self.assertFalse(gs.hasMetaRobotsNoindex(f))
        for f in blocked :
            self.assertTrue(gs.hasMetaRobotsNoindex(f))

    def test_gatherfiles_html(self) :
        os.chdir("tests")
        allfiles = gs.gatherfiles({"html", "htm"})
        os.chdir("..")
        asSet = set(allfiles)
        expected = { "./blocked1.html", "./blocked2.html",
                     "./blocked3.html", "./blocked4.html",
                     "./unblocked1.html", "./unblocked2.html",
                     "./unblocked3.html", "./unblocked4.html",
                     "./subdir/a.html", "./subdir/subdir/b.html",
                     "./badCharsNoindex1.html",
                     "./badCharsNoindex2.html",
                     "./badCharsDoIndex.html",
                     "./blocked5.html",
                     "./blocked6.html",
                     "./exclude/inc1.html", "./exclude/exc1.html",
                     "./exclude/subdir/inc2.html", "./exclude/subdir/exc2.html",
                     "./exclude/excludeSubDir/exc3.html",
                     "./exclude/subdir/exc4.html"}
        if os.name == "nt" :
            expected = { s.replace("/", "\\") for s in expected }
        self.assertEqual(asSet, expected)

    def test_gatherfiles_html_pdf(self) :
        os.chdir("tests")
        allfiles = gs.gatherfiles({"html", "htm", "pdf"})
        os.chdir("..")
        asSet = set(allfiles)
        expected = { "./blocked1.html", "./blocked2.html",
                     "./blocked3.html", "./blocked4.html",
                     "./unblocked1.html", "./unblocked2.html",
                     "./unblocked3.html", "./unblocked4.html",
                     "./subdir/a.html", "./subdir/subdir/b.html",
                     "./x.pdf", "./subdir/y.pdf",
                     "./subdir/subdir/z.pdf",
                     "./badCharsNoindex1.html",
                     "./badCharsNoindex2.html",
                     "./badCharsDoIndex.html",
                     "./blocked5.html",
                     "./blocked6.html",
                     "./exclude/inc1.html", "./exclude/exc1.html",
                     "./exclude/subdir/inc2.html", "./exclude/subdir/exc2.html",
                     "./exclude/excludeSubDir/exc3.html",
                     "./exclude/subdir/exc4.html"}
        if os.name == "nt" :
            expected = { s.replace("/", "\\") for s in expected }
        self.assertEqual(asSet, expected)

    def test_gatherfiles_pdf(self) :
        os.chdir("tests")
        allfiles = gs.gatherfiles({"pdf"})
        os.chdir("..")
        asSet = set(allfiles)
        expected = { "./x.pdf", "./subdir/y.pdf",
                     "./subdir/subdir/z.pdf"}
        if os.name == "nt" :
            expected = { s.replace("/", "\\") for s in expected }
        self.assertEqual(asSet, expected)

    def test_lastmod(self) :
        # assumes that if on windows must be running tests locally
        # rather than in GitHub Actions, and may or may not be in a
        # git repo, so simply skips this test.
        if os.name != "nt" :
            os.chdir("tests")
            dateStr = gs.lastmod("./unblocked1.html")
            self.assertTrue(validateDate(dateStr), msg=dateStr)
            dateStr = gs.lastmod("./subdir/a.html")
            self.assertTrue(validateDate(dateStr), msg=dateStr)
            os.chdir("..")

    def test_urlstring(self) :
        filenames = [ "./a.html",
                      "./index.html",
                      "./subdir/a.html",
                      "./subdir/index.html",
                      "./subdir/subdir/a.html",
                      "./subdir/subdir/index.html",
                      "./aindex.html",
                      "./subdir/aindex.html",
                      "./a.shtml",
                      "./index.shtml",
                      "./subdir/a.shtml",
                      "./subdir/index.shtml",
                      "./subdir/subdir/a.shtml",
                      "./subdir/subdir/index.shtml",
                      "./aindex.shtml",
                      "./subdir/aindex.shtml",
                      "/a.html",
                      "/index.html",
                      "/subdir/a.html",
                      "/subdir/index.html",
                      "/subdir/subdir/a.html",
                      "/subdir/subdir/index.html",
                      "/aindex.html",
                      "/subdir/aindex.html",
                      "/a.shtml",
                      "/index.shtml",
                      "/subdir/a.shtml",
                      "/subdir/index.shtml",
                      "/subdir/subdir/a.shtml",
                      "/subdir/subdir/index.shtml",
                      "/aindex.shtml",
                      "/subdir/aindex.shtml",
                      "a.html",
                      "index.html",
                      "subdir/a.html",
                      "subdir/index.html",
                      "subdir/subdir/a.html",
                      "subdir/subdir/index.html",
                      "aindex.html",
                      "subdir/aindex.html",
                      "a.shtml",
                      "index.shtml",
                      "subdir/a.shtml",
                      "subdir/index.shtml",
                      "subdir/subdir/a.shtml",
                      "subdir/subdir/index.shtml",
                      "aindex.shtml",
                      "subdir/aindex.shtml",
                    ]
        base1 = "https://TESTING.FAKE.WEB.ADDRESS.TESTING/"
        base2 = "https://TESTING.FAKE.WEB.ADDRESS.TESTING"
        expected = [ "https://TESTING.FAKE.WEB.ADDRESS.TESTING/a.html",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/a.html",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/a.html",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/aindex.html",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/aindex.html",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/a.shtml",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/a.shtml",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/a.shtml",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/aindex.shtml",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/aindex.shtml"
                    ]
        for i, f in enumerate(filenames) :
            self.assertEqual(expected[i%len(expected)], gs.urlstring(f, base1))
            self.assertEqual(expected[i%len(expected)], gs.urlstring(f, base2))

    def test_urlstring_drop_html(self) :
        filenames = [ "./a.html",
                      "./index.html",
                      "./subdir/a.html",
                      "./subdir/index.html",
                      "./subdir/subdir/a.html",
                      "./subdir/subdir/index.html",
                      "./aindex.html",
                      "./subdir/aindex.html",
                      "./a.shtml",
                      "./index.shtml",
                      "./subdir/a.shtml",
                      "./subdir/index.shtml",
                      "./subdir/subdir/a.shtml",
                      "./subdir/subdir/index.shtml",
                      "./aindex.shtml",
                      "./subdir/aindex.shtml",
                      "/a.html",
                      "/index.html",
                      "/subdir/a.html",
                      "/subdir/index.html",
                      "/subdir/subdir/a.html",
                      "/subdir/subdir/index.html",
                      "/aindex.html",
                      "/subdir/aindex.html",
                      "/a.shtml",
                      "/index.shtml",
                      "/subdir/a.shtml",
                      "/subdir/index.shtml",
                      "/subdir/subdir/a.shtml",
                      "/subdir/subdir/index.shtml",
                      "/aindex.shtml",
                      "/subdir/aindex.shtml",
                      "a.html",
                      "index.html",
                      "subdir/a.html",
                      "subdir/index.html",
                      "subdir/subdir/a.html",
                      "subdir/subdir/index.html",
                      "aindex.html",
                      "subdir/aindex.html",
                      "a.shtml",
                      "index.shtml",
                      "subdir/a.shtml",
                      "subdir/index.shtml",
                      "subdir/subdir/a.shtml",
                      "subdir/subdir/index.shtml",
                      "aindex.shtml",
                      "subdir/aindex.shtml",
                      ]
        base1 = "https://TESTING.FAKE.WEB.ADDRESS.TESTING/"
        base2 = "https://TESTING.FAKE.WEB.ADDRESS.TESTING"
        expected = [ "https://TESTING.FAKE.WEB.ADDRESS.TESTING/a",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/a",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/a",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/aindex",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/aindex",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/a.shtml",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/a.shtml",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/a.shtml",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/aindex.shtml",
                      "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/aindex.shtml"
                     ]
        for i, f in enumerate(filenames) :
            self.assertEqual(expected[i%len(expected)], gs.urlstring(f, base1, True))
            self.assertEqual(expected[i%len(expected)], gs.urlstring(f, base2, True))

    def test_removeTime(self) :
        date = "2020-09-11T13:35:00-04:00"
        expected = "2020-09-11"
        self.assertEqual(expected, gs.removeTime(date))

    def test_xmlEscapeCharacters(self):
        test_strings = [
            "abs&def",
            "abs<def",
            "abs>def",
            "abs'def",
            'abs"def',
            """&<>"'"'><&"""
        ]
        expected = [
            "abs&amp;def",
            "abs&lt;def",
            "abs&gt;def",
            "abs&apos;def",
            "abs&quot;def",
            "&amp;&lt;&gt;&quot;&apos;&quot;&apos;&gt;&lt;&amp;"
        ]
        for t, e in zip(test_strings, expected):
            self.assertEqual(e, gs.xmlEscapeCharacters(t))
        
    def test_xmlSitemapEntry(self) :
        base = "https://TESTING.FAKE.WEB.ADDRESS.TESTING/"
        f = "./a.html"
        date = "2020-09-11T13:35:00-04:00"
        actual = gs.xmlSitemapEntry(f, base, date)
        expected = "<url>\n<loc>https://TESTING.FAKE.WEB.ADDRESS.TESTING/a.html</loc>\n<lastmod>2020-09-11T13:35:00-04:00</lastmod>\n</url>"
        self.assertEqual(actual, expected)
        actual = gs.xmlSitemapEntry(f, base, date, True)
        expected = "<url>\n<loc>https://TESTING.FAKE.WEB.ADDRESS.TESTING/a</loc>\n<lastmod>2020-09-11T13:35:00-04:00</lastmod>\n</url>"
        self.assertEqual(actual, expected)

    def test_xmlSitemapEntryDateOnly(self) :
        base = "https://TESTING.FAKE.WEB.ADDRESS.TESTING/"
        f = "./a.html"
        date = "2020-09-11T13:35:00-04:00"
        actual = gs.xmlSitemapEntry(f, base, date, False, True)
        expected = "<url>\n<loc>https://TESTING.FAKE.WEB.ADDRESS.TESTING/a.html</loc>\n<lastmod>2020-09-11</lastmod>\n</url>"
        self.assertEqual(actual, expected)
        actual = gs.xmlSitemapEntry(f, base, date, True, True)
        expected = "<url>\n<loc>https://TESTING.FAKE.WEB.ADDRESS.TESTING/a</loc>\n<lastmod>2020-09-11</lastmod>\n</url>"
        self.assertEqual(actual, expected)

    def test_xmlSitemapEntry_withEscapes(self):
        base = "https://TESTING.FAKE.WEB.ADDRESS.TESTING/"
        f_template = "./a{0}.html"
        date = "2020-09-11T13:35:00-04:00"
        test_strings = [
            "abs&def",
            "abs<def",
            "abs>def",
            "abs'def",
            'abs"def',
            """&<>"'"'><&"""
        ]
        expected = [
            "abs&amp;def",
            "abs&lt;def",
            "abs&gt;def",
            "abs&apos;def",
            "abs&quot;def",
            "&amp;&lt;&gt;&quot;&apos;&quot;&apos;&gt;&lt;&amp;"
        ]
        for t, e in zip(test_strings, expected):
            f = f_template.format(t)
            self.assertEqual(e, gs.xmlEscapeCharacters(t))
            actual = gs.xmlSitemapEntry(f, base, date)
            expected = "<url>\n<loc>https://TESTING.FAKE.WEB.ADDRESS.TESTING/a{0}.html</loc>\n<lastmod>2020-09-11T13:35:00-04:00</lastmod>\n</url>".format(e)
            self.assertEqual(actual, expected)
            actual = gs.xmlSitemapEntry(f, base, date, True)
            expected = "<url>\n<loc>https://TESTING.FAKE.WEB.ADDRESS.TESTING/a{0}</loc>\n<lastmod>2020-09-11T13:35:00-04:00</lastmod>\n</url>".format(e)
            self.assertEqual(actual, expected)

    def test_robotsTxtParser(self) :
        expected = [ [],
                     ["/"],
                     ["/"],
                     [],
                     ["/subdir"],
                     ["/subdir/"],
                     ["/subdir/y.pdf"],
                     ["/subdir/subdir/"],
                     ["/subdir/y.pdf", "/subdir/subdir/b.html"],
                     ["/subdir/y.pdf", "/subdir/subdir/b.html"],
                     ["/subdir/y.pdf", "/subdir/subdir/b.html"],
                     ["/subdir/y.pdf", "/subdir/subdir/b.html"]
                     ]
        os.chdir("tests")
        for i, e in enumerate(expected) :
            filename = "robots" + str(i) + ".txt"
            self.assertEqual(set(gs.parseRobotsTxt(filename)), set(e), msg=filename)
        os.chdir("..")

    def test_robotsBlockedWithRobotsParser(self) :
        os.chdir("tests")
        allFiles = [ "./blocked1.html", "./blocked2.html",
                     "./blocked3.html", "./blocked4.html",
                     "./unblocked1.html", "./unblocked2.html",
                     "./unblocked3.html", "./unblocked4.html",
                     "./subdir/a.html", "./subdir/subdir/b.html",
                     "./x.pdf", "./subdir/y.pdf",
                     "./subdir/subdir/z.pdf"]
        for f in allFiles :
            self.assertTrue(gs.robotsBlocked(f, {"/"}))
        blocked = {  "./blocked1.html", "./blocked2.html",
                     "./blocked3.html", "./blocked4.html",
                     "./subdir/a.html", "./subdir/subdir/b.html",
                     "./subdir/y.pdf",
                     "./subdir/subdir/z.pdf"}
        for f in allFiles :
            if f in blocked :
                self.assertTrue(gs.robotsBlocked(f, {"/subdir/"}))
            else :
                self.assertFalse(gs.robotsBlocked(f, {"/subdir/"}))
        blocked = {  "./blocked1.html", "./blocked2.html",
                     "./blocked3.html", "./blocked4.html",
                     "./subdir/subdir/b.html",
                     "./subdir/subdir/z.pdf"}
        for f in allFiles :
            if f in blocked :
                self.assertTrue(gs.robotsBlocked(f, {"/subdir/subdir/"}))
            else :
                self.assertFalse(gs.robotsBlocked(f, {"/subdir/subdir"}))
        blocked = { "./blocked1.html", "./blocked2.html",
                    "./blocked3.html", "./blocked4.html",
                    "./subdir/subdir/b.html", "./subdir/y.pdf",
                    "./unblocked1.html" }
        blockThese = { "/subdir/subdir/b", "/unblocked1.html", "/subdir/y.pdf"}
        for f in allFiles :
            if f in blocked :
                self.assertTrue(gs.robotsBlocked(f, blockThese))
            else :
                self.assertFalse(gs.robotsBlocked(f, blockThese))
        os.chdir("..")

    def test_adjust_path(self):
        self.assertEqual("/", gs.adjust_path("."))
        self.assertEqual("/", gs.adjust_path("\\"))
        self.assertEqual("/", gs.adjust_path(".\\"))
        self.assertEqual("/hello", gs.adjust_path("\\hello"))
        self.assertEqual("/hello", gs.adjust_path(".\\hello"))
        self.assertEqual("/hello/bye", gs.adjust_path("\\hello\\bye"))
        self.assertEqual("/hello/bye", gs.adjust_path(".\\hello\\bye"))
        self.assertEqual("/", gs.adjust_path("/"))
        self.assertEqual("/", gs.adjust_path("./"))
        self.assertEqual("/hello", gs.adjust_path("/hello"))
        self.assertEqual("/hello", gs.adjust_path("./hello"))
        self.assertEqual("/hello/bye", gs.adjust_path("/hello/bye"))
        self.assertEqual("/hello/bye", gs.adjust_path("./hello/bye"))
        self.assertEqual("/hello", gs.adjust_path("hello"))
        self.assertEqual("/hello/bye", gs.adjust_path("hello/bye"))
