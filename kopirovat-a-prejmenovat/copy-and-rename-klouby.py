import os
import shutil
import uuid

INPUT_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_2_rozrezane_na_prave_a_leve_a_prevracene\_RA\originaly_a_souradnice\1-2znaky"
OUTPUT_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_5_ruce_trenovaci_testovaci\01_Train\RA"

COUNT_OF_COPIED_FILES = 0

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

        old_name = os.path.join(os.path.abspath(root), filename)
        print(old_name)

        # Separate base from extension
        base, extension = os.path.splitext(filename)

        # Create new name with unique ID
        # new_name = "NEART_" + base + extension
        new_name = "RA12_" + base + str(uuid.uuid1()) + extension

        # Save the file to the new path
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)


        new_name = os.path.join(OUTPUT_DIR, new_name)
        print(new_name)

        shutil.copyfile(old_name, new_name)

        # Increment and show count of all copied files
        COUNT_OF_COPIED_FILES += 1
        print("Count of copied files = " + str(COUNT_OF_COPIED_FILES))
        print()

    # end for
# end for
