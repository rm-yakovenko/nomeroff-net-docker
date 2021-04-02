import os
import sys
import cv2
import warnings
from urllib.request import urlopen
import matplotlib.image as mpimg
from threading import Lock

warnings.filterwarnings('ignore')

lock = Lock()

# NomeroffNet path
NOMEROFF_NET_DIR = os.path.abspath('../nomeroff-net')
sys.path.append(NOMEROFF_NET_DIR)
# Import license plate recognition tools.
from NomeroffNet.YoloV5Detector import Detector
detector = Detector()
detector.load()

from NomeroffNet.BBoxNpPoints import NpPointsCraft, getCvZoneRGB, convertCvZonesRGBtoBGR, reshapePoints
npPointsCraft = NpPointsCraft()
npPointsCraft.load()

from NomeroffNet.OptionsDetector import OptionsDetector
from NomeroffNet.TextDetector import TextDetector

from NomeroffNet import TextDetector
from NomeroffNet import textPostprocessing

# load models
optionsDetector = OptionsDetector()
optionsDetector.load("latest")

textDetector = TextDetector.get_static_module("eu")()
textDetector.load("latest")

def read_number_plates(url):
    with urlopen(url) as file:
        img = mpimg.imread(file, 0)

    # Ensure that only one model is loaded among all threads.
    with lock:
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

      targetBoxes = detector.detect_bbox(img)
      all_points = npPointsCraft.detect(img, targetBoxes,[5,2,0])

      # cut zones
      zones = convertCvZonesRGBtoBGR([getCvZoneRGB(img, reshapePoints(rect, 1)) for rect in all_points])

      # predict zones attributes
      regionIds, stateIds = optionsDetector.predict(zones)
      regionNames = optionsDetector.getRegionLabels(regionIds)

      # find text with postprocessing by standart
      textArr = textDetector.predict(zones)
      textArr = textPostprocessing(textArr, regionNames)

    return textArr, regionNames
