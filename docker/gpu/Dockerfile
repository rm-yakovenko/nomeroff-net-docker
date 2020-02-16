FROM tensorflow/tensorflow:1.15.2-gpu-py3

RUN apt update && apt install -y git libsm6 libxrender1

RUN pip install --no-cache-dir flask waitress Cython numpy wtforms tqdm \
    git+https://github.com/matterport/Mask_RCNN

RUN pip install --no-cache-dir nomeroff-net-gpu