FROM alpine:3.10

# We need git to check commit dates 
# when generating lastmod dates for
# the sitemap.xml.
RUN apk update
RUN apk add git

# The base alpine find command is quite 
# limited. We need full featured find.
RUN apk add findutils

# We also need coreutils to get fuller
# featured versions of shell commands, 
# such as sort.
RUN apk add coreutils

# We also need gawk
RUN apk add gawk

COPY LICENSE README.md /
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
