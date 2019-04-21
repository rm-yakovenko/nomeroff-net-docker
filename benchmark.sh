#!/usr/bin/env bash

echo "Warming up"

ab -s 120 -n 2 http://localhost:3116/read?url=https://automoto.r.worldssl.net/auto/Chevrolet-Lacetti-ne_ukazan-none-2007-16-23414105.jpeg > /dev/null

echo "Benchmarking"

ab -n 10 http://localhost:3116/read?url=https://automoto.r.worldssl.net/auto/Chevrolet-Lacetti-ne_ukazan-none-2007-16-23414105.jpeg
