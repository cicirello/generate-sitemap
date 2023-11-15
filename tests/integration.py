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

import unittest

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
        
class IntegrationTest(unittest.TestCase) :

    def testIntegrationExcludePaths(self):
        urlset = set()
        with open("tests/exclude/sitemap.xml","r") as f :
            for line in f :
                i = line.find("<loc>")
                if i >= 0 :
                    i += 5
                    j = line.find("</loc>", i)
                    if j >= 0 :
                        urlset.add(line[i:j].strip())
                    else :
                        self.fail("No closing </loc>")
                i = line.find("<lastmod>")
                if i >= 0 :
                    i += 9
                    j = line.find("</lastmod>", i)
                    if j >= 0 :
                        self.assertTrue(validateDate(line[i:j].strip()))
                    else :
                        self.fail("No closing </lastmod>")
        
        expected = { "https://TESTING.FAKE.WEB.ADDRESS.TESTING/inc1.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/inc2.html"
                     }
        self.assertEqual(expected, urlset)
                    

    def testIntegration(self) :
        urlset = set()
        with open("tests/sitemap.xml","r") as f :
            for line in f :
                i = line.find("<loc>")
                if i >= 0 :
                    i += 5
                    j = line.find("</loc>", i)
                    if j >= 0 :
                        urlset.add(line[i:j].strip())
                    else :
                        self.fail("No closing </loc>")
                i = line.find("<lastmod>")
                if i >= 0 :
                    i += 9
                    j = line.find("</lastmod>", i)
                    if j >= 0 :
                        self.assertTrue(validateDate(line[i:j].strip()))
                    else :
                        self.fail("No closing </lastmod>")
                    
        expected = { "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked1.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked2.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked3.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked4.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/a.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/x.pdf", 
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/z.pdf",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/uncommitted.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/badCharsDoIndex.html"
                     }
        self.assertEqual(expected, urlset)

    def testIntegrationWithAdditionalTypes(self) :
        urlset = set()
        with open("tests/sitemap.txt","r") as f :
            for line in f :
                line = line.strip()
                if len(line) > 0 :
                    urlset.add(line)
        expected = { "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked1.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked2.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked3.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked4.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/a.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/x.pdf", 
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/z.pdf",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/include.docx",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/include.pptx",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/uncommitted.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/badCharsDoIndex.html"
                     }
        self.assertEqual(expected, urlset)

    def testIntegrationDropHtmlExtension(self) :
        urlset = set()
        with open("tests/subdir/sitemap.xml","r") as f :
            for line in f :
                i = line.find("<loc>")
                if i >= 0 :
                    i += 5
                    j = line.find("</loc>", i)
                    if j >= 0 :
                        urlset.add(line[i:j].strip())
                    else :
                        self.fail("No closing </loc>")
                i = line.find("<lastmod>")
                if i >= 0 :
                    i += 9
                    j = line.find("</lastmod>", i)
                    if j >= 0 :
                        self.assertTrue(validateDate(line[i:j].strip()))
                    else :
                        self.fail("No closing </lastmod>")

        expected = { "https://TESTING.FAKE.WEB.ADDRESS.TESTING/a",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/y.pdf",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/b",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/z.pdf"
                     }
        self.assertEqual(expected, urlset)

    def testIntegrationWithAdditionalTypesDropHtmlExtension(self) :
        urlset = set()
        with open("tests/subdir/sitemap.txt","r") as f :
            for line in f :
                line = line.strip()
                if len(line) > 0 :
                    urlset.add(line)
        expected = { "https://TESTING.FAKE.WEB.ADDRESS.TESTING/a",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/y.pdf",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/b",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/z.pdf"
                     }
        self.assertEqual(expected, urlset)

