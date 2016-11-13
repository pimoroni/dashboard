#!/bin/bash

gettools="no" # if set to yes downloads the tools required
setup="yes" # if set to yes populates program folder
buildeb="yes" # if set to yes builds the deb files
cleanup="yes" # if set to yes cleans up build files
pkgfiles=( "build" "changes" "deb" "dsc" "tar.xz" )

if [ $gettools == "yes" ]; then
    sudo apt-get update && sudo apt-get install build-essential debhelper devscripts dh-make dput gnupg
fi

if [ $setup == "yes" ]; then
    rm -R ../program/build ../program/debian &> /dev/null
    cp -R ./debian ../program/
fi

cd ../program

if [ $buildeb == "yes" ]; then
    debuild -aarmhf
    for file in ${pkgfiles[@]}; do
        rm ../packaging/*.$file &> /dev/null
        mv ../*.$file ../packaging
    done
fi

if [ $cleanup == "yes" ]; then
    debuild clean
    rm -R ./build ./debian ./doc &> /dev/null
fi

exit 0
