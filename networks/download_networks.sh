#!/usr/bin/env bash

wget -q https://cloud.uni-hamburg.de/public.php/dav/files/Rw3McfsN7eSLHfG/?accept=zip -O graphs.zip
unzip -q graphs.zip
mv graphs/* .
rm -rf graphs
rm graphs.zip
