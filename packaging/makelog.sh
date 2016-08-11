#!/bin/bash

mainlog="CHANGELOG"
debianlog="debian/changelog"

# generate debian changelog

cat $mainlog > $debianlog

exit 0
