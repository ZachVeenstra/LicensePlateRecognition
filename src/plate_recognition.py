import easyocr
import csv
import cv2
import LicensePlateEquvalencies

CSV_PATH = './plates.csv'
STATE_INDEX = 2
PLATE_IMAGE_LINK_INDEX = 1
STATE_ID_INDEX = 0


def main():
    """
    Go through each license plate in the CSV and read the text from the
    image, calculating the number of which were correctly identified.
    """

    use_gpu = False

    # EasyOCR can use a GPU to speed up its processing.
    print("Does your machine have GPU? (y/n)")
    if input().casefold() == "y":
        use_gpu = True

    words = LicensePlateEquvalencies.words

    # Set variables for statistics
    total_plates = 0
    num_plates_correctly_identified = 0
    num_plates_incorrectly_identified = 0
    correctly_identified_state = 0
    incorrectly_identified_state = 0
    prev_state_id = 0
    list_of_plates = []
    plates_with_num_identified = 0

    # Open csv file containing the path to all license plate images
    with open(CSV_PATH) as license_plates_csv:
        csv_reader = csv.reader(license_plates_csv)
        for _, row in enumerate(csv_reader):

            # Skip the first line, which only contains column titles.
            if csv_reader.line_num == 1:
                continue

            try:
                # Attempt to get the next image
                license_plate = getImage(row)
            except Exception:
                continue

            state_id = row[STATE_ID_INDEX]

            # Statisitics of the current state
            if int(state_id) > int(prev_state_id):
                print(prev_state_name + " Was correctly identified: " + str(correctly_identified_state) + " times")
                print(prev_state_name + " Was misidentified: " + str(incorrectly_identified_state) + " times")
                correctly_identified_state = 0
                incorrectly_identified_state = 0

            prev_state_name = row[STATE_INDEX]
            prev_state_id = row[STATE_ID_INDEX]

            # Read the image and return all text found and sets to the variable 'text'.
            # ([Bounding box coordinates(Top left, Top Right, Bottom Right, Bottom Left)], [Text], [Confidence])
            character_reader = easyocr.Reader(['en'], gpu=use_gpu)
            text = character_reader.readtext(license_plate)
            print("Here is the text: ", text)

            total_plates += 1
            is_looping = True

            plate_number_found = False

            # This portion iterates through all text boxes found and attempts to validate if it is a license plate
            # number based on the position of the text.
            for x in range(len(text)):
                # Checks the top left and bottom right bounding box coordinates.
                top_left = text[x][0][0]
                bottom_right = text[x][0][2]
                if 6 <= top_left[0] and 19 <= top_left[1]:
                    if bottom_right[0] <= 224 and bottom_right[1] <= 111:
                        # If it is within the general area of a license plate number(based on average of most)
                        # then validate and collect the license plate number.
                        print("License plate # is:", text[x][1], "Confidence %:", text[x][2])
                        list_of_plates.append(text[x][1])
                        plates_with_num_identified += 1
                        plate_number_found = True
                        break

            if plate_number_found == False:
                print("Failed to find license plate #")
            
            # This iterates through the text to see if it can identify the proper State.
            for x in range(len(text)):
                word = text[x][1]
                for i, sublist in enumerate(words):
                    for equivalence in sublist:
                        # Iterates through all state identifiers and attempts to match text
                        if equivalence.lower() in word.lower():
                            # Collects Statistics
                            print(f"{word} contained {equivalence}")
                            print("State ID: " + state_id)
                            print("index: " + str(i))

                            if int(state_id) == i:
                                num_plates_correctly_identified += 1
                                correctly_identified_state += 1
                                print("Correctly Identified: " + str(num_plates_correctly_identified))
                            else:
                                num_plates_incorrectly_identified += 1
                                incorrectly_identified_state += 1
                                print("Misidentified: " + str(num_plates_incorrectly_identified))

                            is_looping = False
                            break

                    if not is_looping:
                        break
                if not is_looping:
                    break
    
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
        for plate in list_of_plates:
            file.write(f"{plate}\n")


def getImage(row):
    """
    Extract an image from a row in a csv table.
    A TypeError exception is raised if a gif is given as an argument
    """
    image_url = f"{row[PLATE_IMAGE_LINK_INDEX]}"
    image_type = image_url[(image_url.rindex('.') + 1):]
    print(image_url)
    # The gif file type isn't supported.
    if image_type.casefold() == 'gif':
        raise TypeError
    image = cv2.imread(image_url)

    return image


if __name__ == "__main__":
    main()
