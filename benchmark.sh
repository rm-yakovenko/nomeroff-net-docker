#!/usr/bin/env bash

echo "Warming up"

ab -s 180 -n 2 http://localhost:3116/read?url=https://raw.githubusercontent.com/ria-com/nomeroff-net/master/examples/images/example1.jpeg > /dev/null

echo "Benchmarking"

ab -n 10 http://localhost:3116/read?url=https://raw.githubusercontent.com/ria-com/nomeroff-net/master/examples/images/example1.jpeg
