FROM python:3.6

RUN pip install --no-cache-dir flask waitress Keras imgaug wtforms opencv_python imutils scikit_image asyncio \
    git+https://github.com/matterport/Mask_RCNN

ARG INTEL_TENSORFLOW

RUN if [ $INTEL_TENSORFLOW ]; \
    then pip install --no-cache-dir intel-tensorflow ; \
    else pip install --no-cache-dir tensorflow; \
    fi
