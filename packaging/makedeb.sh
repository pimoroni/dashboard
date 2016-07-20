#!/bin/bash

gettools="yes"
setup="yes"
cleanup="yes"
pkgfiles=( "build" "changes" "deb" "dsc" "tar.xz" )


if [ $gettools == "yes" ]; then
    sudo apt-get update && sudo apt-get install build-essential debhelper devscripts dh-make dput gnupg
fi

if [ $setup == "yes" ]; then
    rm -R ../dashboard/debian &> /dev/null
    cp -R ./debian/ ../dashboard/
fi

cd ../dashboard && debuild

for file in ${pkgfiles[@]}; do
    mv ../*.$file ../packaging
done

if [ $cleanup == "yes" ]; then
    debuild clean
    rm -R ./debian &> /dev/null
fi

exit 0
