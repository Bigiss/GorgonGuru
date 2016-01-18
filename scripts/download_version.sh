#!/bin/sh

VERSION=$1

if [ -z ${VERSION} ]; then
	exit
fi


mkdir v${VERSION}
for f in `echo "abilities.json
advancementtables.json
ai.json
attributes.json
directedgoals.json
effects.json
items.json
quests.json
recipes.json
skills.json
tsysclientinfo.json
xptables.json"`; do
	wget "http://cdn.projectgorgon.com/v${VERSION}/data/${f}" -O v${VERSION}/${f}
done

