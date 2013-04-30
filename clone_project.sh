#!/bin/bash
echo Cloning project $1 as $1_staticmaps
# This checks for TILEMILL_PROJECTS and sets it to a default if it's not set.
: ${TILEMILL_PROJECTS:="$HOME/Documents/MapBox"}
cp -a $TILEMILL_PROJECTS/project/$1/ $TILEMILL_PROJECTS/project/$1_staticmaps
cp -a $TILEMILL_PROJECTS/project/$1/_staticmaps/project.mml $TILEMILL_PROJECTS/project/$1_staticmaps/project.mml.template

