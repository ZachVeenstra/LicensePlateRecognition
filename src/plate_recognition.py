import easyocr
import matplotlib.pyplot as plt
import numpy as np
from urllib.request import urlopen
import csv
import cv2
import re


CSV_PATH = './plates.csv'
STATE_INDEX = 2
DESCRIPTION_INDEX = 2
PLATE_IMAGE_LINK_INDEX = 1

    
def main():
    """
    Go through each license plate in the CSV and read the text from the
    image, calculating the number of which were correctly identified.
    """
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

            state = row[STATE_INDEX].capitalize()

            character_reader = easyocr.Reader(['en'], gpu=True)  # Note: if you have a GPU, set this to True!

            text = character_reader.readtext(license_plate)
            print("Here is the text: ", text)
            # TODO: Read the state in a better way than just getting a certain element from the text.
            # state_read = text[0][1] NOT ALWAYS AT THIS INDEX
            # TODO: Create table with state spelling equivilencies. Ex: California - CA, CAL, CALIFORNIA

            total_plates += 1
            for x in range(len(text)):
                word = text[x][1]
                if state == word.capitalize():
                    print(f"{word} == {state}")
                    num_plates_correctly_identified += 1
                    break
                else:
                    print(f"{word} != {state}")

    if total_plates != 0:
        print(f"Percentage correct = {num_plates_correctly_identified / total_plates}")
    else:
        print("Failed to read")

def getImage(row):
    """
    Extract an image from a row in a csv table.
    A TypeError exception is raised if a gif is given as an argument
    """
    image_url = f"{row[PLATE_IMAGE_LINK_INDEX]}"
    image_type = image_url[(image_url.rindex('.') + 1):]
    print(image_url)
    # We don't support the gif file type for now.
    if image_type.casefold() == 'gif':
        raise TypeError
    image = cv2.imread(image_url)
    """
    # Breaks if we try to display image
    if image is not None:
        # Display the image (optional)
        cv2.imshow('Image', image)
        cv2.waitKey(1)
        cv2.destroyAllWindows()
    
    resp = urlopen(image_link)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)  # The image object
    """
    return image


if __name__ == "__main__":
    main()
