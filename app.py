import os
import sys
import warnings
from urllib.request import urlopen
import matplotlib.image as mpimg
import tensorflow as tf

warnings.filterwarnings('ignore')

# change this property
NOMEROFF_NET_DIR = os.path.abspath('../nomeroff-net')
sys.path.append(NOMEROFF_NET_DIR)

# Import license plate recognition tools.
from NomeroffNet import  Detector
from NomeroffNet import  filters
from NomeroffNet import  RectDetector
from NomeroffNet import  OptionsDetector
from NomeroffNet import  TextDetector
from NomeroffNet import  textPostprocessing

# load models
rectDetector = RectDetector()

optionsDetector = OptionsDetector()
optionsDetector.load("latest")

textDetector = TextDetector.get_static_module("eu")()
textDetector.load("latest")

nnet = Detector()
nnet.loadModel(NOMEROFF_NET_DIR)

def read_number_plates(url):
    with urlopen(url) as file:
        img = mpimg.imread(file, 0)

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
