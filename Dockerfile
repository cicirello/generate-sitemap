# Copyright (c) 2021-2026 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM ghcr.io/cicirello/pyaction:3.14.2-gh-2.86.0
COPY generatesitemap.py /generatesitemap.py
ENTRYPOINT ["/generatesitemap.py"]
