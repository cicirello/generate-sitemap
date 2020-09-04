#!/bin/bash -l
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

websiteRoot=$1
baseUrl=$2
includeHTML=$3
includePDF=$4
sitemapFormat=$5

numUrls=0
skipCount=0

function formatSitemapEntry {
	if [ "$sitemapFormat" == "xml" ]; then
		echo "<url>" >> sitemap.xml
		echo "<loc>$2${1%index.html}</loc>" >> sitemap.xml
		echo "<lastmod>$3</lastmod>" >> sitemap.xml
		echo "</url>" >> sitemap.xml
	else
		echo "$2${1/%\/index.html/\/}" >> sitemap.txt
	fi
	numUrls=$((numUrls+1))
}

cd "$websiteRoot"

if [ "$sitemapFormat" == "xml" ]; then
	echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" > sitemap.xml
	echo "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" >> sitemap.xml
else
	rm -f sitemap.txt
	touch sitemap.txt
fi

if [ "$includeHTML" == "true" ]; then
	while read file; do 
		if [ "0" == $(grep -i -c -E "<meta*.*name*.*robots*.*content*.*noindex" $file || true) ]; then
			lastMod=$(git log -1 --format=%cI $file)
			formatSitemapEntry ${file#./} "$baseUrl" "$lastMod"
		else
			skipCount=$((skipCount+1))
		fi
	done < <(find . \( -name '*.html' -o -name '*.htm' \) -type f -printf '%d\0%h\0%p\n' | sort -t '\0' -n | awk -F '\0' '{print $3}')
fi
if [ "$includePDF" == "true" ]; then
	while read file; do
		lastMod=$(git log -1 --format=%cI $file)
		formatSitemapEntry ${file#./} "$baseUrl" "$lastMod"
	done < <(find . -name '*.pdf' -type f -printf '%d\0%h\0%p\n' | sort -t '\0' -n | awk -F '\0' '{print $3}')
fi

if [ "$sitemapFormat" == "xml" ]; then
	echo "</urlset>"  >> sitemap.xml
	pathToSitemap="$websiteRoot/sitemap.xml"
else 
	pathToSitemap="$websiteRoot/sitemap.txt"
fi

echo ::set-output name=sitemap-path::$pathToSitemap
echo ::set-output name=url-count::$numUrls
echo ::set-output name=excluded-count::$skipCount
