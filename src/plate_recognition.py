
import easyocr
import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen
import csv
import cv2

CSV_PATH = './data/license_plates.csv'
STATE_INDEX = 0
DESCRIPTION_INDEX = 1
PLATE_IMAGE_LINK_INDEX = 2


def main():
    with open(CSV_PATH) as license_plates_csv:
        csv_reader = csv.reader(license_plates_csv)
        for row in csv_reader:
            # Skip the first line, which only contains column titles.
            if csv_reader.line_num == 1:
                continue

            try:
                image = getImage(row)
            except Exception:
                continue


            plt.imshow(image)
            plt.show()

            break


def getImage(row):
    """
    Extract an image from a row in a csv table.
    A TypeError exception is raised if a gif is given as an argument
    """
    image_url = f"{row[PLATE_IMAGE_LINK_INDEX][9:-1]}"
    image_type = image_url[image_url.rindex('.')+1: ]

    # We don't support the gif file type for now.
    if image_type.casefold() == 'gif':
        raise TypeError

    resp = urlopen(image_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR) # The image object

    return image

if __name__ == "__main__":
    main()