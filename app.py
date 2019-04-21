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
MASK_RCNN_MODEL_PATH = os.path.join(NOMEROFF_NET_DIR, "models/mask_rcnn_numberplate_0700.h5")
OPTIONS_MODEL_PATH = os.path.join(NOMEROFF_NET_DIR, "models/numberplate_options_2019_03_05.h5")

# If you use gpu version tensorflow please change model to gpu version named like *-gpu.pb
mode = "cpu"
OCR_NP_UKR_TEXT = os.path.join(NOMEROFF_NET_DIR, "models/anpr_ocr_ua_12-{}.h5".format(mode))
OCR_NP_EU_TEXT = os.path.join(NOMEROFF_NET_DIR, "models/anpr_ocr_eu_2-{}.h5".format(mode))
OCR_NP_RU_TEXT = os.path.join(NOMEROFF_NET_DIR, "models/anpr_ocr_ru_3-{}.h5".format(mode))

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
        nnet.loadModel(MASK_RCNN_MODEL_PATH)

    NP = nnet.detect([img])

    # Generate image mask.
    cv_img_masks = filters.cv_img_mask(NP)

    if not rectDetector:
        rectDetector = RectDetector()

    if not optionsDetector:
        optionsDetector = OptionsDetector()
        optionsDetector.load(OPTIONS_MODEL_PATH)

    if not textDetector:
        textDetector = TextDetector({
            "eu_ua_2004_2015": {
                "for_regions": ["eu_ua_2015", "eu_ua_2004"],
                "model_path": OCR_NP_UKR_TEXT
            },
            "eu": {
                "for_regions": ["eu", "eu_ua_1995"],
                "model_path": OCR_NP_EU_TEXT
            },
            "ru": {
                "for_regions": ["ru"],
                "model_path": OCR_NP_RU_TEXT
            }
        })

    # Detect points.
    points = rectDetector.detect(cv_img_masks)
    zones = rectDetector.get_cv_zonesBGR(img, points)

    # find standart
    region_ids, state_ids = optionsDetector.predict(zones)
    region_names = optionsDetector.getRegionLabels(region_ids)

    # find text with postprocessing by standart
    number_plates = textDetector.predict(zones, region_names)
    number_plates = textPostprocessing(number_plates, region_names)
    return number_plates, region_names
