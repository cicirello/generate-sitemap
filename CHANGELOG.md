# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2021-4-15

### Added

### Changed

### Deprecated

### Removed

### Fixed

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
