FROM tensorflow/tensorflow:latest-py3

RUN apt install -y git libsm6 libxrender1

RUN pip install --no-cache-dir flask waitress Cython numpy wtforms tqdm \
    git+https://github.com/matterport/Mask_RCNN

RUN pip install --no-cache-dir nomeroff-net