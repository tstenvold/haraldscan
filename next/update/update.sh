#!/bin/bash
#Terence Stenvold July 2010
#copy xml files and run this file to add all new Mac's discovered

cp ../../main/MACLIST .
cat *.xml | grep '[0-9ABCDEF]\{2\}:[0-9ABCDEF]\{2\}:[0-9ABCDEF]\{2\}:[0-9ABCDEF]\{2\}:[0-9ABCDEF]\{2\}:[0-9ABCDEF]\{2\}' | cut -d ">" -f 2 | cut -d ":" -f 1,2,3 > macin
python newmac.py
rm macin
cp -f MACLIST ../../main/MACLIST
rm MACLIST
