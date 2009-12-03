#!/bin/bash

cxfreeze --target-dir=haraldscan-dist-$1 haraldscan.py
cp MACLIST haraldscan-dist-$1/MACLIST
cp gpl-3.0.txt haraldscan-dist-$1/gpl-3.0.txt
tar -cvzf haraldscan-dist-$1.tar.gz haraldscan-dist-$1
