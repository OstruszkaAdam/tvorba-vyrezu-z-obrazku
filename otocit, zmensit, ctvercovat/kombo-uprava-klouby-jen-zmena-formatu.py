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

INPUT_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_4_klouby_trenovaci_testovaci\1_Zakladni verze\01_Train\NEART"
# OUTPUT_DIR = r"C:\Users\Adam\Desktop\cil"

input_dir_name = os.path.basename(INPUT_DIR)
output_dir_base = os.path.dirname(INPUT_DIR)
output_dir_name = input_dir_name + " flipnute"
# output_dir_name = "otocene_fake_" + str(TARGET_SIZE)

OUTPUT_DIR = os.path.join(output_dir_base, output_dir_name)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


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
            snimek_otoceny = imutils.rotate_bound(snimek_puvodni, uhel_otoceni)

            snimek_otoceny_a_orezany = snimek_otoceny

            # velmi nepatrne doostreni noveho obrazku
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
            snimek_otoceny_a_orezany_a_doostreny = cv2.filter2D(snimek_otoceny_a_orezany, -1, kernel)
            mira_pruhlednosti = 0.93
            obrazek_otoceny = cv2.addWeighted(snimek_otoceny_a_orezany_a_doostreny, 1 - mira_pruhlednosti,
                                              snimek_otoceny_a_orezany,
                                              mira_pruhlednosti, 0)




            # KONEC OTACENI





            # oriznuti pripony z nazvu souboru
            nazevSnimkuBezPripony = os.path.splitext(filename)[0]
            # vyjmuti samotne pripony
            # PouzePripona = os.path.splitext(nazev_snimku)[1]
            pouze_pripona = ".jpg"

            rozhazene_poradi = round(random() * 1000)
            rozhazene_poradi = rozhazene_poradi + round(random() * 100)
            rozhazene_poradi = str(rozhazene_poradi)

            new_name =  nazevSnimkuBezPripony + pouze_pripona

            # new_name = "OTOCENY_" + str(uhel_otoceni) + "_STUPNU_" + nazevSnimkuBezPripony + PouzePripona
            # Save the file to the new path
            new_name = os.path.join(OUTPUT_DIR, new_name)

            # cv2.imwrite(new_name, snimek_prevzorkovany_opencv)
            cv2.imwrite(new_name, snimek_puvodni, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

            print("uklada se soubor " + str(new_name))



# end for
