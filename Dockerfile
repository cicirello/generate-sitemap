# Copyright (c) 2021-2023 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM ghcr.io/cicirello/pyaction:4.21.0
COPY generatesitemap.py /generatesitemap.py
ENTRYPOINT ["/generatesitemap.py"]
