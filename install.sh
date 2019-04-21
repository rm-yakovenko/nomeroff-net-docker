#!/bin/bash

set -e

git clone --depth 1 https://github.com/ria-com/nomeroff-net

wget -N -P nomeroff-net/models https://nomeroff.net.ua/models/mrcnn/mask_rcnn_numberplate_0700.h5 https://nomeroff.net.ua/models/options/numberplate_options_2019_03_05.h5 https://nomeroff.net.ua/models/ocr/eu/anpr_ocr_eu_2-cpu.h5  https://nomeroff.net.ua/models/ocr/ru/anpr_ocr_ru_3-cpu.h5 https://nomeroff.net.ua/models/ocr/ua/anpr_ocr_ua_12-cpu.h5