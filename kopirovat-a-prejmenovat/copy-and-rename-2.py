import os
import shutil
import uuid

INPUT_DIR = r"H:\MIMIC"
OUTPUT_DIR = r"H:\SLOUCENY-DATASET"

INPUT_DATASET_NAME = "NIHH"

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
        new_name = INPUT_DATASET_NAME + "_" + base + "_" + str(uuid.uuid1()) + extension

        # Choose the right target subfolder according to filename
        new_subfolder = ""
        if "frontal" in filename:
            new_subfolder = "frontal"
        elif "lateral" in filename:
            new_subfolder = "lateral"

        # Add the subfolder to output path
        new_output_dir = os.path.join(OUTPUT_DIR, new_subfolder)

        if not os.path.exists(new_output_dir):
            os.makedirs(new_output_dir)

        # Save the file to the new path
        new_name = os.path.join(new_output_dir, new_name)
        print(new_name)

        shutil.copyfile(old_name, new_name)

        # Increment and show count of all copied files
        COUNT_OF_COPIED_FILES += 1
        print("Count of copied files = " + str(COUNT_OF_COPIED_FILES))
        print()

    # end for
# end for
