#!/usr/bin/env bash

URL=https://cdn2.riastatic.com/photosnew/auto/photo/bmw_x6-m__413276302f.jpg

echo "Warming up"

ab -s 180 -n 2 http://localhost:3116/read?url=$URL > /dev/null

echo "Benchmarking"

ab -n 30 http://localhost:3116/read?url=$URL
