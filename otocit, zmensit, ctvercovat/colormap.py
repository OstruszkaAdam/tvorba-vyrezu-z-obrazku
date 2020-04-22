# tvorba 4 otocenych kopii + jedne kopie neotocene (resp. otocene o 0 stupnu), jejichg rozsireni na ctverec, zmenseni na zadanou velikost a ulozeni

import numpy as np
import argparse
import imutils
import cv2
import os
from random import random
import uuid
from PIL import Image
import shutil

TARGET_SIZE = 299

INPUT_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_4_klouby_trenovaci_testovaci\2_Vcetne odvozenin (testovaci bez odvozenin)\01_Train\RA"
# OUTPUT_DIR = r"C:\Users\Adam\Desktop\cil"

input_dir_name = os.path.basename(INPUT_DIR)
output_dir_base = os.path.dirname(INPUT_DIR)
output_dir_name1 = input_dir_name + "_CM_BONE"
output_dir_name2 = input_dir_name + "_CM_OCEAN"
output_dir_name3 = input_dir_name + "_CM_WINTER"
output_dir_name4 = input_dir_name + "_CM_HOT"


count_of_processed_files = 0

# zpracovani vsech souboru ve slozce ###################################################################################
for subdir, dirs, files in os.walk(INPUT_DIR):
    for filename in files:

        # if the file does not end in .jpg or .jpeg (case-insensitive) or other formats, continue with the next iteration of the for loop
        if not (filename.lower().endswith(".jpg") or
                filename.lower().endswith(".jpeg") or
                filename.lower().endswith(".png") or
                filename.lower().endswith(".tif") or
                filename.lower().endswith(".tiff")):
            continue
     # end if

        # show the file name on std out
        print("zpracovava se soubor " + filename)
        count_of_processed_files += 1
        print("Pocet zpracovanych souboru = " + str(count_of_processed_files))
        print()

        new_name = ""




        # ZACATEK OTACENI


        # get the file name and full path of the current image file
        imageFileWithPath = os.path.join(subdir, filename)
        # attempt to open the image with OpenCV
        snimek_puvodni = cv2.imread(imageFileWithPath)

        vyska_puvodniho_obrazku = np.size(snimek_puvodni, 0)
        sirka_puvodniho_obrazku = np.size(snimek_puvodni, 1)

        uhel_A = 4
        # uhel_B = round(5 + random()*15)
        uhel_B = uhel_A + round(2 + random() * 5)

        uhel_C = - uhel_A - round(random() * 5)

        uhel_D = - uhel_B - round(random() * 5)

        uhel_O = 0

        # uhly = [uhel_O, uhel_A, uhel_B, uhel_C, uhel_D]
        uhly = [uhel_O]

        # loop over the rotation angles
        # for angle in np.arange(0, 360, 15):
        for uhel_otoceni in uhly:
            # otoceni snimku o zadany uhel



            # KONEC OTACENI

            # https://www.learnopencv.com/applycolormap-for-pseudocoloring-in-opencv-c-python/
            snimek_obarveny1 = cv2.applyColorMap(snimek_puvodni, cv2.COLORMAP_BONE)
            snimek_obarveny2 = cv2.applyColorMap(snimek_puvodni, cv2.COLORMAP_OCEAN)
            snimek_obarveny3 = cv2.applyColorMap(snimek_puvodni, cv2.COLORMAP_WINTER)
            snimek_obarveny4 = cv2.applyColorMap(snimek_puvodni, cv2.COLORMAP_HOT)




            # oriznuti pripony z nazvu souboru
            nazevSnimkuBezPripony = os.path.splitext(filename)[0]
            # vyjmuti samotne pripony
            # PouzePripona = os.path.splitext(nazev_snimku)[1]
            pouze_pripona = ".jpg"

            rozhazene_poradi = round(random() * 1000)
            rozhazene_poradi = rozhazene_poradi + round(random() * 100)
            rozhazene_poradi = str(rozhazene_poradi)

            new_name1 = "CM-BONE_" + nazevSnimkuBezPripony + pouze_pripona
            new_name2 = "CM-OCEAN_" + nazevSnimkuBezPripony + pouze_pripona
            new_name3 = "CM-WINTER_" + nazevSnimkuBezPripony + pouze_pripona
            new_name4 = "CM-HOT_" + nazevSnimkuBezPripony + pouze_pripona

            output_dirs = [output_dir_name1, output_dir_name2, output_dir_name3, output_dir_name4]

            for nazev_slozky in output_dirs:
                OUTPUT_DIR = os.path.join(output_dir_base, nazev_slozky)
                if not os.path.exists(OUTPUT_DIR):
                    os.makedirs(OUTPUT_DIR)

            # Save the file to the new path
            new_name1 = os.path.join(os.path.join(output_dir_base, output_dir_name1), new_name1)
            new_name2 = os.path.join(os.path.join(output_dir_base, output_dir_name2), new_name2)
            new_name3 = os.path.join(os.path.join(output_dir_base, output_dir_name3), new_name3)
            new_name4 = os.path.join(os.path.join(output_dir_base, output_dir_name4), new_name4)

            # cv2.imwrite(new_name, snimek_prevzorkovany_opencv)
            cv2.imwrite(new_name1, snimek_obarveny1, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            cv2.imwrite(new_name2, snimek_obarveny2, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            cv2.imwrite(new_name3, snimek_obarveny3, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            cv2.imwrite(new_name4, snimek_obarveny4, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

            print("uklada se soubor " + str(new_name))



# end for
