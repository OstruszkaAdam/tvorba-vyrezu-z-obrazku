import numpy as np
import argparse
import imutils
import cv2
import os
from random import random
import uuid

INPUT_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_2_rozrezane_na_prave_a_leve_a_prevracene\_RA\originaly_a_souradnice"
# OUTPUT_DIR = r"C:\Users\Adam\Desktop\cil"

input_dir_name = os.path.basename(INPUT_DIR)
output_dir_base = os.path.dirname(INPUT_DIR)
output_dir_name = input_dir_name + " otocene_fake"

OUTPUT_DIR = os.path.join(output_dir_base, output_dir_name)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

COUNT_OF_COPIED_FILES = 0

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

        # get the file name and full path of the current image file
        imageFileWithPath = os.path.join(subdir, filename)
        # attempt to open the image with OpenCV
        snimek_puvodni = cv2.imread(imageFileWithPath)

        vyska_obrazku = np.size(snimek_puvodni, 0)
        sirka_obrazku = np.size(snimek_puvodni, 1)

        uhel_A = 4
        # uhel_B = round(5 + random()*15)
        uhel_B = uhel_A + round(2 + random() * 5)

        uhel_C = - uhel_A - round(random() * 5)

        uhel_D = - uhel_B - round(random() * 5)

        uhly = [uhel_A, uhel_B, uhel_C, uhel_D]

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
            obrazek_hotovy = cv2.addWeighted(snimek_otoceny_a_orezany_a_doostreny, 1 - mira_pruhlednosti,
                                             snimek_otoceny_a_orezany,
                                             mira_pruhlednosti, 0)

            # random oriznuti
            uhel_absolutni_velikost = abs(uhel_otoceni)
            vyska_upraveneho_obrazku = np.size(obrazek_hotovy, 0)
            sirka_upraveneho_obrazku = np.size(obrazek_hotovy, 1)
            nahodna_velikost_orezu = round(random() * 50)  # nahodny rozmer oriznuteho pruhu
            velikost_orezu_horni_dolni = uhel_absolutni_velikost * 8 + nahodna_velikost_orezu
            velikost_orezu_leva_prava = uhel_absolutni_velikost * 8 + nahodna_velikost_orezu

            x_start, y_start = velikost_orezu_leva_prava, velikost_orezu_horni_dolni
            x_end, y_end = sirka_upraveneho_obrazku - velikost_orezu_leva_prava, vyska_upraveneho_obrazku - velikost_orezu_horni_dolni
            ref_point = [(x_start, y_start), (x_end, y_end)]
            obrazek_hotovy = obrazek_hotovy[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]

            # sestaveni noveho nazvu a ulozeni souboru
            # cv2.imshow("Otoceny, oriznuty a doostreny snimek", obrazek_hotovy)
            # cv2.waitKey(0)

            # oriznuti pripony z nazvu souboru
            nazevSnimkuBezPripony = os.path.splitext(filename)[0]
            # vyjmuti samotne pripony
            # PouzePripona = os.path.splitext(nazev_snimku)[1]
            PouzePripona = ".png"

            new_name = "OTOCENY_" + str(uhel_otoceni) + "_STUPNU_" + nazevSnimkuBezPripony + str(uuid.uuid1()) + PouzePripona
            # new_name = "OTOCENY_" + str(uhel_otoceni) + "_STUPNU_" + nazevSnimkuBezPripony + PouzePripona
            # Save the file to the new path
            new_name = os.path.join(OUTPUT_DIR, new_name)
            print(new_name)

            cv2.imwrite(new_name, obrazek_hotovy)


# end for
