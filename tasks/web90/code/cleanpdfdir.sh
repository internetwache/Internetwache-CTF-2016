#!/bin/bash

DIR="./pdf/"
SIZE=$(du -sm $DIR | grep -oP "\d+")
if [[ $SIZE -gt 100 ]]; then
	rm -r "$DIR*.pdf"
fi
