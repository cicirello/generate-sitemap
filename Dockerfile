# Copyright (c) 2020 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM cicirello/alpine-plus-plus:latest
RUN apk add --no-cache --update python3
COPY generatesitemap.py /generatesitemap.py
ENTRYPOINT ["/generatesitemap.py"]
