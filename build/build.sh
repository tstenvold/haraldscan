#!/bin/bash

cxfreeze --target-dir=haraldscan-dist-$1 haraldscan.py
cp MACLIST haraldscan-dist-$1/MACLIST
cp doc/README haraldscan-dist-$1/README
cp doc/gpl-3.0.txt haraldscan-dist-$1/gpl-3.0.txt
tar -cvzf haraldscan-dist-$1.tar.gz haraldscan-dist-$1
rm -R haraldscan-dist-$1
