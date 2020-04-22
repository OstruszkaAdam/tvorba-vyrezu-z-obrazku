import os
import csv
import random


INPUT_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_5_ruce_trenovaci_testovaci\03_low-res na cloud bez rozdeleni na subsety\RA"

LABEL = "RA"
# konkretni diagnoza

SUBDATASET_TRAIN = "TRAIN"
SUBDATASET_TEST = "TEST"

csv_file = open(LABEL + ".csv", "a")
csw_writer = csv.writer(csv_file)
# csw_writer.writerow(('set', 'image_path', 'label'))
COUNT_OF_WRITTEN_FILES = 0
VELIKOST_TRENOVACIHO_SUBSETU = 0.1 # v procentech



# zjisteni poctu snimku ve slozce a vypocteni, kolik snimku z tohoto poctu ma byt zarazeno mezi testovaci
path, dirs, files = next(os.walk(INPUT_DIR))
pocet_snimku_ve_slozce = len(files)
pocet_snimku_do_testovaciho_subsetu = round(pocet_snimku_ve_slozce * VELIKOST_TRENOVACIHO_SUBSETU)


# vygeneruje zadany pocet hodnot v zadaem rozmezi - snimky s temito indexy budou zarazene mezi testovaci
randomlist = random.sample(range(1, pocet_snimku_ve_slozce), pocet_snimku_do_testovaciho_subsetu)
randomlist.sort() #jinak jsou hodnoty v random poradi
print (randomlist)

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

        # pokud je snimek na seznamu testovacich
        if(COUNT_OF_WRITTEN_FILES in randomlist):
            print(SUBDATASET_TEST)
            csw_writer.writerow((SUBDATASET_TEST, "gs://bucket-ruce/" + LABEL + "/" + filename, LABEL))
        else: #pokud neni
            csw_writer.writerow((SUBDATASET_TRAIN, "gs://bucket-ruce/" + LABEL + "/" + filename, LABEL))
            print(SUBDATASET_TRAIN)

        # Increment and show count of all copied files
        COUNT_OF_WRITTEN_FILES += 1
        print("Count of written files = " + str(COUNT_OF_WRITTEN_FILES))
        print()

    # end for
# end for
csv_file.close()