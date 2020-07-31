FROM alpine:3.10

# We need git to check commit dates 
# when generating lastmod dates for
# the sitemap.xml.
RUN apk update
RUN apk add git

COPY LICENSE README.md /
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
