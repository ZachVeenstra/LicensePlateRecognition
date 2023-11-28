import subprocess
import shlex
import csv

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
        
        image_link = f"{row[PLATE_IMAGE_LINK_INDEX][9:-1]}"
        file_path = f"./data/images/{image_link[69:]}"
        command = f'curl {image_link} --create-dirs -o {file_path}'

        print(command)
        
        args = shlex.split(command)
        process = subprocess.Popen(args,shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()