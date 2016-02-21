#!/bin/bash

CURDIR=$(pwd)

if [[ ! "$CURDIR" =~ tasks$ ]]; then
	echo "Please run this script from the 'tasks/' directory."
	exit 1;
fi

DESTDIR="$(pwd)/../static/files/"
for file in $(/bin/ls .)
do
	if [[ ! -d "$file" ]]; then
		continue;
	fi
	cd "$file"

	zip -r "$file.zip" "task/"
	mv "$file.zip" "$DESTDIR/"
	cd ..
done;
