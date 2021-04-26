# generate-sitemap: Github action for automating sitemap generation
# 
# Copyright (c) 2020-2021 Vincent A Cicirello
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

class IntegrationTest(unittest.TestCase) :

    def testIntegration(self) :
        urlset = set()
        with open("tests/sitemap.xml","r") as f :
            for line in f :
                i = line.find("<loc>")
                if i >= 0 :
                    i += 5
                    j = line.find("</loc>", 5)
                    if j >= 0 :
                        urlset.add(line[i:j].strip())
        expected = { "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked1.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked2.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked3.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/unblocked4.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/a.html",
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/x.pdf", 
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/subdir/subdir/z.pdf" }
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
                     "https://TESTING.FAKE.WEB.ADDRESS.TESTING/include.pptx"}
        self.assertEqual(expected, urlset)

