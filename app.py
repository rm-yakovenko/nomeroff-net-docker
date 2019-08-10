import os
import sys
import warnings
from urllib.request import urlopen
import matplotlib.image as mpimg

warnings.filterwarnings('ignore')

# change this property
NOMEROFF_NET_DIR = os.path.abspath('./nomeroff-net')

# specify the path to Mask_RCNN if you placed it outside Nomeroff-net project
MASK_RCNN_DIR = os.path.join(NOMEROFF_NET_DIR, 'Mask_RCNN')
MASK_RCNN_LOG_DIR = os.path.join(NOMEROFF_NET_DIR, 'logs')

sys.path.append(NOMEROFF_NET_DIR)

# Import license plate recognition tools.
from NomeroffNet import filters, RectDetector, TextDetector, OptionsDetector, Detector, textPostprocessing

nnet = rectDetector = optionsDetector = textDetector = None


def read_number_plates(url):
    with urlopen(url) as file:
        img = mpimg.imread(file, 0)

    global nnet, rectDetector, optionsDetector, textDetector
    if not nnet:
        nnet = Detector(MASK_RCNN_DIR, MASK_RCNN_LOG_DIR)
        nnet.loadModel('latest')

    NP = nnet.detect([img])

    # Generate image mask.
    cv_img_masks = filters.cv_img_mask(NP)

    if not rectDetector:
        rectDetector = RectDetector()

    if not optionsDetector:
        optionsDetector = OptionsDetector()
        optionsDetector.load('latest')

    if not textDetector:
        textDetector = TextDetector.get_static_module("eu")()
        textDetector.load("latest")

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
