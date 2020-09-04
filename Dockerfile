# Copyright (c) 2020 Vincent A. Cicirello
# https://www.cicirello.org/
# Licensed under the MIT License
FROM cicirello/alpine-plus-plus:latest
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
