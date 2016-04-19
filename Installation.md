# Installation for Binary #

  1. Unpack to a directory
  1. Run `./haraldscan.py -b` to build database
  1. `./haradscan [Options]` to run Harald Scan

  * For GNU/Linux only
  * Should be completely independent and require no dependencies


# Installation for Source Code #

  1. Unpack to a directory
  1. Run `python haraldscan.py -b` to build database
  1. `python haradscan.py [Options]` to run Harald Scan

## Requirements OS X ##

  * [Python 2.5](http://www.python.org) **Must be able to `import objc` with python**
  * [Lightblue](http://lightblue.sourceforge.net/)
  * [PySQLite](http://oss.itsystementwicklung.de/trac/pysqlite/)
  * X CODE from Apple

As neither of these are available from Macports. You need to install from source. Please let me know of any successes or failures.

## Requirements GNU/Linux ##

  * [Python 2.6](http://www.python.org)
  * [Pybluez](http://code.google.com/p/pybluez/)
  * [PySQLite](http://oss.itsystementwicklung.de/trac/pysqlite/)