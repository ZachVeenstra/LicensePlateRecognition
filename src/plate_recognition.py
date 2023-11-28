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
    total_plates = 0
    num_plates_correctly_identified = 0
    with open(CSV_PATH) as license_plates_csv:
        csv_reader = csv.reader(license_plates_csv)
        for row in csv_reader:
            # Skip the first line, which only contains column titles.
            if csv_reader.line_num == 1:
                continue

            try:
                license_plate = getImage(row)
            except Exception:
                continue

            state = row[STATE_INDEX]

            character_reader = easyocr.Reader(['en'], gpu=False) # Note: if you have a GPU, set this to True!

            text = character_reader.readtext(license_plate)
            
            # TODO: Read the state in a better way than just getting a certain element from the text.
            state_read = text[0][1]
            
            # TODO: Create table with state spelling equivilencies. Ex: California - CA, CAL, CALIFORNIA

            total_plates += 1
            if state == state_read:
                print(f"{state_read} == {state}")
                num_plates_correctly_identified += 1
            else:
                print(f"{state_read} != {state}")
    
    print(f"Percentage correct = {num_plates_correctly_identified / total_plates}")


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