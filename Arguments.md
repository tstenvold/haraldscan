# Intro #
This page will provide a detailed overview of the command line arguments

Harald Scan should be run from the directory it was unpacked to. Doing otherwise may cause issues with Harald Scan not being able to locate files or writing files to odd locations.

# Arguments #
Usage: haraldscan OPTIONS

Options:
> `--version`             show program's version number and exit

> `-h, --help`           show this help message and exit

> `-b, --build`           Builds MAC Addr database. Ignores all other options

> `-f FLUSHNUM, --flush=FLUSHNUM`  When db = size entered. Flush entries to a different database (useful if combined with -m)

> `-m, --memorydb`        Puts the database in Memory instead of a file on disk

> `--no-service`          Disables service scans on 'Unknown' devices

> `--no-write`            Disables writing discovered device info to a file

> `-s, --service`         Does a service scan of all devices found and saves a file like a 'Unknown' device would

> `-t NMINUTES, --time=NMINUTES` Shows number of devices found per time specified in mins (default is 15 mins)

> `-u, --update`          Updates the MACLIST if there are updates and rebuilds the database (requires and Internet connection)

> -w FILENAME, --write=FILENAME Outputs discovered device info to a file you specify (unspecified: filename is a timestamp)