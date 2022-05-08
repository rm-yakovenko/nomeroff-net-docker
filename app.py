import os
import sys
import tempfile
from urllib.request import urlopen

# NomeroffNet path
nomeroff_net_dir = os.path.abspath('../nomeroff-net')
sys.path.append(nomeroff_net_dir)
from nomeroff_net import pipeline
from nomeroff_net.tools import unzip

number_plate_detection_and_reading = pipeline("number_plate_detection_and_reading", image_loader="opencv")

def read_number_plates(url):
    global number_plate_detection_and_reading

    with tempfile.NamedTemporaryFile() as fp:
        with urlopen(url) as response:
            fp.write(response.read())

        result = number_plate_detection_and_reading([fp.name])

    (images, images_bboxs,
       images_points, images_zones, region_ids,
       region_names, count_lines,
       confidences, texts) = unzip(result)

    return texts[0], region_names[0]
