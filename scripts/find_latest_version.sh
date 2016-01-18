#!/bin/sh

VERSION=$1
NUMVERS=$2

if [ -z ${VERSION} ]; then
	exit
fi

if [ -z ${NUMBERS} ]; then
        NUMVERS=20
fi

for i in `seq ${VERSION} $((${VERSION}+${NUMVERS}))`; do
	RES=$(curl -f -s -I "http://cdn.projectgorgon.com/v${i}/data/abilities.json" | grep "Last-Modified:")
	if [ $? -eq 0 ]; then
		echo -n "Version ${i} found .. "
                echo $RES
	fi
done

