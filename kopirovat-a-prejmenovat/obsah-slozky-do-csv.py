import os
import csv


INPUT_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_5_ruce_trenovaci_testovaci\01_Rotridene hi-res bez uprav\01_Train\RA_Resampled"

LABEL = "RA"
# konkretni diagnoza

SUBDATASET_NAME = "TRAIN"
# muze nabyvat hodnot TEST nebo TRAIN

csv_file = open(LABEL + ".csv", "a")
csw_writer = csv.writer(csv_file)
# csw_writer.writerow(('set', 'image_path', 'label'))
COUNT_OF_WRITTEN_FILES = 0


# Walk through all files in the directory that contains the files to copy
for root, dirs, files in os.walk(INPUT_DIR):
    for filename in files:

        # if the file does not end in .jpg or .jpeg (case-insensitive) or other formats, continue with the next iteration of the for loop
        if not (filename.lower().endswith(".jpg") or
                filename.lower().endswith(".jpeg") or
                filename.lower().endswith(".png") or
                filename.lower().endswith(".tif") or
                filename.lower().endswith(".tiff")):
            continue
        # end if

        print(filename)

        csw_writer.writerow((SUBDATASET_NAME, "gs://bucket-ruce/" + LABEL + "/" + filename, LABEL))

        # Increment and show count of all copied files
        COUNT_OF_WRITTEN_FILES += 1
        print("Count of written files = " + str(COUNT_OF_WRITTEN_FILES))
        print()

    # end for
# end for
csv_file.close()