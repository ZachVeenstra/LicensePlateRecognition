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
        ["Guam", "Guam USA"],
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
        ["North Dakota", "N.Dak", "NDak", "NorthDakota", "N.Dakota", "NDakota"],
        ["Ohio"],
        ["Oklahoma", "Okla"],
        ["Oregon", "Ore"],
        ["Pennsylvania", "Penn", "Penna"],
        ["Puerto Rico", "PuertoRico", "Puerto", "Rico"],
        ["Rhode Island", "R.I.", "RhodeIsland", "Rhode"],
        ["South Carolina", "SouthCarolina"],
        ["South Dakota", "SouthDakota", "S.Dak", "S.Dakota", "SDak", "SDakota"],
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
    # Set variables for statistics
    total_plates = 0
    num_plates_correctly_identified = 0
    num_plates_incorrectly_identified = 0
    correctly_identified_state = 0
    incorrectly_identified_state = 0
    prevStateId = 0
    listofplates = []
    plates_with_num_identified = 0

    # Open csv file containing the path to all license plate images
    with open(CSV_PATH) as license_plates_csv:
        csv_reader = csv.reader(license_plates_csv)
        for n, row in enumerate(csv_reader):
            # Skip the first line, which only contains column titles.
            if csv_reader.line_num == 1:
                continue

            try:
                # Attempt to get the next image
                license_plate = getImage(row)
            except Exception:
                continue

            # State ID
            stateId = row[STATE_ID_INDEX]

            # Statisitics of the current state
            if int(stateId) > int(prevStateId):
                print(prevStateName + " Was correctly identified: " + str(correctly_identified_state) + " times")
                print(prevStateName + " Was misidentified: " + str(incorrectly_identified_state) + " times")
                correctly_identified_state = 0
                incorrectly_identified_state = 0

            prevStateName = row[STATE_INDEX]
            prevStateId = row[STATE_ID_INDEX]
            # Read the image and return all text found and sets to the variable 'text'.
            # ([Bounding box coordinates(Top left, Top Right, Bottom Right, Bottom Left)], [Text], [Confidence])
            character_reader = easyocr.Reader(['en'], gpu=True)  # Note: if you have a GPU, set this to True!
            text = character_reader.readtext(license_plate)
            print("Here is the text: ", text)


            total_plates += 1
            isLooping = True
            # the variable abc is to check if a license plate # was found.
            abc = 1
            # This portion iterates through all text boxes found and attempts to validate if it is a license plate
            # number based on the position of the text.
            for x in range(len(text)):
                # Checks the top left and bottom right bounding box coordinates.
                topleft = text[x][0][0]
                bottomright = text[x][0][2]
                if 6 <= topleft[0] and 19 <= topleft[1]:
                    if bottomright[0] <= 224 and bottomright[1] <= 111:
                        # If it is within the general area of a license plate number(based on average of most)
                        # then validate and collect the license plate number.
                        print("License plate # is:", text[x][1], "Confidence %:", text[x][2])
                        listofplates.append(text[x][1])
                        plates_with_num_identified += 1
                        abc = 0
                        break
            if abc == 1:
                print("Failed to find license plate #")
            
            # This iterates through the text to see if it can identify the proper State.
            for x in range(len(text)):
                # The text
                word = text[x][1]
                for i, sublist in enumerate(words):
                    for equivalence in sublist:
                        # Iterates through all state identifiers and attempts to match text
                        if equivalence.lower() in word.lower():
                            # Collects Statistics
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
                    if not isLooping:
                        break
                if not isLooping:
                    break
                """
                # This was the initial state checker w/out equivalencies 
                # Capitalization does not matter.
                if state == word.capitalize():
                    print(f"{word} == {state}")
                    num_plates_correctly_identified += 1
                    break
                else:
                    print(f"{word} != {state}")
                """
    
    # Output of data:
    if total_plates != 0:
        print(f"Percentage correct(States) = {num_plates_correctly_identified / total_plates}")
    else:
        print("Failed to read")
        
    print(f"Percentage misidentified(States) = {num_plates_incorrectly_identified / total_plates}")
    num_plates_not_identified = total_plates - num_plates_incorrectly_identified - num_plates_correctly_identified
    print(f"Percentage not identified(States) = {num_plates_not_identified / total_plates}")
    print("-------------------------------")
    print(f"Percentage licence plate numbers identified(#) = {plates_with_num_identified / total_plates}")

    # Collect all license plate numbers found: 
    file_path = "license_plate_numbers_identified.txt"
    with open(file_path, 'w') as file:
        # Iterate through the list and write each license plate # to a new line in the file
        for plate in listofplates:
            file.write(f"{plate}\n")


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
