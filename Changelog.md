# 0.42 #

## Distribution ##
  * 32 bit and 64 bit binary for Linux
  * OS X version still source code

## Output ##
  * In XML format for easier parsing

## MACLIST ##
  * Updated to 345 Entries.

# 0.41 #

## Distribution ##
  * 32 bit binary will be used for distribution
  * Source code will be labeled as such

## Interface ##
  * Added a coloured title
  * Fixed some displaying issues

## MACLIST ##
  * Updated to 310 Entries.

# 0.401 #
  * There is no diffence in functionality between 0.4 and 0.401

## Distribution ##
  * Revered back to just a src dist. The binary seems to not be working.

## Changed Features ##
  * In the archive the files are now in a folder again.


# 0.4 #

## Distribution ##
  * ~~Harald Scan is now distributed in either source code or dist~~
  * Harald Scan is still distributed by means of source code
## Added Features ##
  * CLI has added a Number of devices discovered by duration (default is 15 mins)
  * The duration for above is configurable through `-t TIME`
  * You can choose either a in memory database or a file database
  * Option to disable services scans entirely even if MAC is 'Unknown'
  * Option to disable writing devices to a text file
  * ability to check Harald Scan version with `--version`
  * Added `-f` for flushing a large database to another db file. Typical usage would be with a large in memory database.

## Changed Features ##
  * Harald Scan will write to a file every time unless `--no-write` is specified
  * Changed argument handling to optparse much better now
  * Uses sqlite3 module instead of pysqlite2 (I didn't realize it was there :S)

## Bug Fixes ##
  * A bunch don't remember though
