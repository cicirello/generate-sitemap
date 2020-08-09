#!/bin/sh -l

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
	find . \( -name '*.html' -o -name '*.htm' \) -type f | sort -r | while read i; do 
		if [ "0" == $(grep -i -c -E "<meta*.*name*.*robots*.*content*.*noindex" $i || true) ]; then
			lastMod=$(git log -1 --format=%cI $i)
			formatSitemapEntry ${i#./} "$baseUrl" "$lastMod"
		else
			skipCount=$((skipCount+1))
		fi
	done
fi
if [ "$includePDF" == "true" ]; then
	for i in $(find . -name '*.pdf' -type f); do 
		lastMod=$(git log -1 --format=%ci $i)
		formatSitemapEntry ${i#./} "$baseUrl" "$lastMod"
	done
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
