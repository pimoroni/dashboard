#!/bin/bash

mainlog="CHANGELOG"
debianlog="debian/changelog"

# function define

success() {
    echo "$(tput setaf 2)$1$(tput sgr0)"
}

inform() {
    echo "$(tput setaf 6)$1$(tput sgr0)"
}

warning() {
    echo "$(tput setaf 1)$1$(tput sgr0)"
}

newline() {
    echo ""
}

# generate debian changelog

cat $mainlog > $debianlog
inform "seeded debian changelog"

exit 0
