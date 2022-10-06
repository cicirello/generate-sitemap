# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2022-10-06

### Added

### Changed

### Deprecated

### Removed

### Fixed
* Now handles alternate casing of boolean inputs specified in GitHub workflow YAML files,
  where it previously expected lowercase only.
* Refactored entrypoint for improved maintainability, and ease of planned new functionality.

### CI/CD

### Dependencies
* Bumped pyaction from 4.7.0 to 4.10.0, which includes upgrading Python in the Docker container to 3.10.7.


## [1.8.4] - 2022-08-03

### Changed
* Refactored index.html dropping logic to ease support for additional dropped index filenames.

### Fixed
* Checks .shtml files for noindex directives, excluding those that have it from the sitemap.
* Added index.shtml to set of index filenames that are dropped from URLs in sitemap.

### Dependencies
* Bumped base docker image cicirello/pyaction from 4.3.1 to 4.7.0.


## [1.8.3] - 2022-04-22

### Fixed
* Corrected check for robots noindex directive in case when non-utf8 characters
  present in an html file.
* Disabled pycache to protect against potential future bug. Currently
  no imports so no pycache created, but if future versions import
  local py modules, a pycache would be created during run in repo. Disabled
  creation of pycache now to avoid.

### Dependencies
* Bumped base Docker image cicirello/pyaction from 4.2.0 to 4.3.1.


## [1.8.2] - 2022-03-04

### Changed
* Bumped Python to 3.10.
* Bumped base Docker image to pyaction 4.2.0.
* Now pulls base Docker image from the GitHub Container Registry rather
  than Docker Hub under the assumption that pulling from GitHub from
  GitHub Actions is likely faster than from Docker Hub.


## [1.8.1] - 2021-07-29

### Changed
* Upgraded base docker image to cicirello/pyaction:4.


## [1.8.0] - 2021-06-28

### Added
* Added option to exclude `.html` from URLs listed in the sitemap 
  for html files. GitHub Pages automatically serves a corresponding
  html file if a user browses to a page with a URL with no file extension.
  This new option to the `generate-sitemap` action enables your sitemap to
  match this behavior if you prefer the extension-less look of URLs. There
  is a new action input, `drop-html-extension`, to control this behavior.

### Changed
* Use major release tag when pulling base docker image (e.g., 
  automatically get non-breaking changes to base image, such as 
  bug fixes, etc without need to update Dockerfile).


## [1.7.2] - 2021-05-13

### Changed
* Switched tag used to pull base Docker image from latest to the
  specific release that is the current latest, to enable testing
  against base image updates prior to releases. This is a purely
  non-functional change.

### Fixed
* Bug involving missing lastmod dates for website files created by
  the workflow, but not yet committed. These are now set using the 
  current date and time.


## [1.7.1] - 2021-05-06

### Changed
* Refactored to improve code maintainability.

### CI/CD
* Introduced major version tag.


## [1.7.0] - 2021-4-26

### Added
* New action input, `additional-extensions`, that enables adding 
  other indexable file types to the sitemap.

### CI/CD
* Enabled CodeQL code scanning on all push/pull-request events.


## [1.6.2] - 2021-3-10

### Changed
* Improved the documentation (otherwise, this release is
  functionally equivalent to the previous release).


## [1.6.1] - 2020-9-24

### Fixed
* Bug in generating URL for files with names ending 
  in "index.html" but not exactly equal to "index.html", 
  such as "aindex.html". Previous version would incorrectly 
  truncate this to just "a", dropping the "index.html". This 
  version now correctly identifies "index.html" files.


## [1.6.0] - 2020-9-21

### Added
* Support for robots.txt: In addition to the previous 
  functionality of excluding html URL's that 
  contain `<meta name="robots" content="noindex">` directives, 
  the `generate-sitemap` GitHub action now parses a `robots.txt` 
  file, if present at the root of the website, excluding any 
  URLs from the sitemap that match `Disallow:` rules for `User-agent: *`.


## [1.5.0] - 2020-9-14

### Changed
* Minor refactoring of python, and optimized action load time 
  by using a prebuilt base docker image that includes exactly 
  what is needed (git and python).

## [1.4.0] - 2020-9-11

### Changed
* Completely re-implemented in Python to enable more easily 
  adding planned future functionality.


## [1.3.0] - 2020-9-9

### Changed
* URL sort order updated (primary sort is by depth of page in 
  site, and URLs at same depth are then sorted alphabetically)
* URL sorting and URL filtering (skipping html files with meta 
  robots noindex directives) is now implemented in Python


## [1.2.0] - 2020-9-4

### Changed
* Documentation updates
* Uses a new base Docker 
  image, [cicirello/alpine-plus-plus](https://github.com/cicirello/alpine-plus-plus)


## [1.1.0] - 2020-8-10

### Added
* Sorting of sitemap entries.


## [1.0.0] - 2020-7-31

### Initial release
This action generates a sitemap for a website hosted on 
GitHub Pages. It supports both xml and txt sitemaps. When 
generating an xml sitemap, it uses the last commit date 
of each file to generate the `<lastmod>` tag in the sitemap 
entry. It can include html as well as pdf files in the 
sitemap, and has inputs to control the included file types 
(defaults include both html and pdf files in the sitemap). It 
skips over html files that 
contain `<meta name="robots" content="noindex">`. It otherwise 
does not currently attempt to respect a `robots.txt` file.
