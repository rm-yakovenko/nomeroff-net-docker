import os
import sys
import warnings
from urllib.request import urlopen
import matplotlib.image as mpimg
import tensorflow as tf

# https://github.com/tensorflow/tensorflow/issues/28287#issuecomment-495005162
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
sess = tf.Session()
graph = tf.get_default_graph()

from tensorflow.python.keras.backend import set_session
set_session(sess)

warnings.filterwarnings('ignore')

# change this property
NOMEROFF_NET_DIR = os.path.abspath('./nomeroff-net')

# specify the path to Mask_RCNN if you placed it outside Nomeroff-net project
MASK_RCNN_DIR = os.path.join(NOMEROFF_NET_DIR, 'Mask_RCNN')
MASK_RCNN_LOG_DIR = os.path.join(NOMEROFF_NET_DIR, 'logs')

sys.path.append(NOMEROFF_NET_DIR)

# Import license plate recognition tools.
from NomeroffNet import filters, RectDetector, TextDetector, OptionsDetector, Detector, textPostprocessing

nnet = Detector(MASK_RCNN_DIR, MASK_RCNN_LOG_DIR)
nnet.loadModel('latest')

rectDetector = RectDetector()

optionsDetector = OptionsDetector()
optionsDetector.load('latest')

textDetector = TextDetector.get_static_module("eu")()
textDetector.load("latest")


def read_number_plates(url):
    global graph, sess
    with urlopen(url) as file:
        img = mpimg.imread(file, 0)

    with graph.as_default():
        set_session(sess)
        NP = nnet.detect([img])

        # Generate image mask.
        cv_img_masks = filters.cv_img_mask(NP)

        # Detect points.
        points = rectDetector.detect(cv_img_masks)
        zones = rectDetector.get_cv_zonesBGR(img, points)

        # find standart
        region_ids, state_ids, _ = optionsDetector.predict(zones)
        region_names = optionsDetector.getRegionLabels(region_ids)

        # find text with postprocessing by standart
        number_plates = textDetector.predict(zones, region_names)
        number_plates = textPostprocessing(number_plates, region_names)

    return number_plates, region_names
