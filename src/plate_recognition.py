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
STATE_ID_INDEX = 0

    
def main():
    words = [
        ["Alabama", "Bama"],
        ["Alaska", "Alas"],
        ["American Samoa", "Samoa"],
        ["Arizona", "Ariz"],
        ["Arkansas", "Ark"],
        ["California", "Calif", "Cali", "Cal"],
        ["CNMI", "Saipan", "Mariana", "Northern Mariana", "Pacific", "NorthernMariana"],
        ["Colorado", "Colo", "Color"],
        ["Connecticut", "Conn"],
        ["Delaware", "Del"],
        ["Florida", "Rida" "Fla"],
        ["Georgia", "Peach"],
        ["Guam"],
        ["Hawaii", "Aloha"],
        ["Idaho", "Potato"],
        ["Illinois", "Ill"],
        ["Indiana", "Ind"],
        ["Iowa"],
        ["Kansas", "Kan"],
        ["Kentucky", "Tucky"],
        ["Louisiana"],
        ["Maine", "Vacationland", "Vacation"],
        ["Maryland", "Mary"],
        ["Massachusetts", "Mass"],
        ["Michigan", "Mich", "Pure"],
        ["Minnesota", "Minn", "Sota"],
        ["Mississippi", "Sippi", "Missi"],
        ["Missouri", "Souri"],
        ["Montana"],
        ["Nebraska", "Neb"],
        ["Nevada", "Nev"],
        ["New Hampshire", "NH", "Hampshire", "NewHampshire"],
        ["New Jersey", "NJ", "N.J.", "Jersey", "Garden", "NewJersey"],
        ["New Mexico", "Mexico", "Enchantment", "NewMexico"],
        ["New York", "York", "NewYork"],
        ["North Carolina", "NorthCarolina"],
        ["North Dakota","N.Dak", "NDak", "NorthDakota", "N.Dakota", "NDakota"],
        ["Ohio"],
        ["Oklahoma","Okla"],
        ["Oregon", "Ore"],
        ["Pennsylvania", "Penn", "Penna"],
        ["Puerto Rico", "PuertoRico", "Puerto", "Rico"],
        ["Rhode Island", "R.I.", "RhodeIsland", "Rhode"],
        ["South Carolina", "SouthCarolina"],
        ["South Dakota","SouthDakota", "S.Dak", "S.Dakota", "SDak", "SDakota"],
        ["Tennessee", "Tenn"],
        ["Texas", "Tex"],
        ["Islands", "VirginIslands"],
        ["Utah"],
        ["Vermont"],
        ["Virginia"],
        ["Washington", "Wash"],
        ["Columbia", "Washington DC", "Washington D.C.", "WashingtonDC", "DC", "D.C"],
        ["West Virginia", "WV", "W.Va.", "WestVirginia", "West", "WVA", "W.Va"],
        ["Wisconsin", "Wisc"],
        ["Wyoming", "WY", "Wyo"]
    ]

    """
    Go through each license plate in the CSV and read the text from the
    image, calculating the number of which were correctly identified.
    """
    total_plates = 0
    num_plates_correctly_identified = 0
    num_plates_incorrectly_identified = 0
    correctly_identified_state = 0
    incorrectly_identified_state = 0
    num_plates_not_identified = 0
    prevStateId = 0
    with open(CSV_PATH) as license_plates_csv:
        csv_reader = csv.reader(license_plates_csv)
        for n, row in enumerate(csv_reader):
            # Skip the first line, which only contains column titles.
            if csv_reader.line_num == 1:
                continue

            try:
                license_plate = getImage(row)
            except Exception:
                continue


            stateId = row[STATE_ID_INDEX]

            if int(stateId) > int(prevStateId):
                print(prevStateName + " Was correctly identified: " + str(correctly_identified_state) + " times")
                print(prevStateName + " Was misidentified: " + str(incorrectly_identified_state) + " times")
                correctly_identified_state = 0
                incorrectly_identified_state = 0

            prevStateName = row[STATE_INDEX]
            prevStateId = row[STATE_ID_INDEX]

            character_reader = easyocr.Reader(['en'], gpu=True)  # Note: if you have a GPU, set this to True!

            text = character_reader.readtext(license_plate)
            print("Here is the text: ", text)
            # TODO: Read the state in a better way than just getting a certain element from the text.
            # state_read = text[0][1] NOT ALWAYS AT THIS INDEX
            # TODO: Create table with state spelling equivalencies. Ex: California - CA, CAL, CALIFORNIA

            total_plates += 1
            isLooping = True
            for x in range(len(text)):
                word = text[x][1]
                for i, sublist in enumerate(words):
                    for equivalence in sublist:
                        if equivalence.lower() in word.lower():
                            print(f"{word} contained {equivalence}")
                            print("State ID: " + stateId)
                            print("index: " + str(i))
                            if int(stateId) == i:
                                num_plates_correctly_identified += 1
                                correctly_identified_state += 1
                                print("Correctly Identified: " + str(num_plates_correctly_identified))
                            else:
                                num_plates_incorrectly_identified += 1
                                incorrectly_identified_state += 1
                                print("Misidentified: " + str(num_plates_incorrectly_identified))
                            isLooping = False
                            break
                        """else:
                            print(f"{word} didn't contain {equivalence}")"""
                    if not isLooping:
                        break
                if not isLooping:
                    break
                """if state == word.capitalize():
                    print(f"{word} == {state}")
                    num_plates_correctly_identified += 1
                    break
                else:
                    print(f"{word} != {state}")"""

    if total_plates != 0:
        print(f"Percentage correct = {num_plates_correctly_identified / total_plates}")
    else:
        print("Failed to read")
    print(f"Percentage misidentified = {num_plates_incorrectly_identified / total_plates}")

    num_plates_not_identified = total_plates - num_plates_incorrectly_identified - num_plates_correctly_identified
    print(f"Percentage not identified = {num_plates_not_identified / total_plates}")

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


