#!/bin/bash

for i in amelia cerulean cosmo cyborg flatly journal lumen readable simplex slate spacelab superhero united yeti; do
    mkdir $i
    cd $i
    wget "http://bootswatch.com/$i/variables.less"
    wget "http://bootswatch.com/$i/bootswatch.less"
    cd ..
done