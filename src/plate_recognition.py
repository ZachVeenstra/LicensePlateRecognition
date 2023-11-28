
# import easyocr
import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen
import subprocess
import shlex
import csv
import cv2

CSV_PATH = './data/license_plates.csv'
STATE_INDEX = 0
DESCRIPTION_INDEX = 1
PLATE_IMAGE_LINK_INDEX = 2


with open(CSV_PATH) as license_plates_csv:
    csv_reader = csv.reader(license_plates_csv)
    for row in csv_reader:
        # Skip the first line, which only contains column titles.
        if csv_reader.line_num == 1:
            continue

        image_url = f"{row[PLATE_IMAGE_LINK_INDEX][9:-1]}"
        image_type = image_url[image_url.rindex('.')+1: ]

        if image_type.casefold() == 'gif':
            continue

        resp = urlopen(image_url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR) # The image object


        plt.imshow(image)
        plt.show()

        break
