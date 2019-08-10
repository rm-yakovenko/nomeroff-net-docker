FROM python:3.7

RUN pip install --no-cache-dir flask waitress Cython numpy wtforms tqdm \
    git+https://github.com/matterport/Mask_RCNN

RUN pip install --no-cache-dir nomeroff-net

ARG INTEL_TENSORFLOW

RUN if [ $INTEL_TENSORFLOW ]; \
    then pip install --no-cache-dir intel-tensorflow ; \
    else pip install --no-cache-dir tensorflow; \
    fi
