import numpy as np
import argparse
import imutils
import cv2
import os
from random import seed
from random import random


INPUT_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_3_rozrezane_na_klouby\_OA\Rozrezane (absolutni rozmery)"
# OUTPUT_DIR = r"C:\Users\Adam\Desktop\cil"

output_dir_base = os.path.dirname(INPUT_DIR)
output_dir_name = "FAKE-otocene"

OUTPUT_DIR = os.path.join(output_dir_base, output_dir_name)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

COUNT_OF_COPIED_FILES = 0

# zpracovani vsech souboru ve slozce ###################################################################################
for nazevSnimku in os.listdir(INPUT_DIR):

    # if the file does not end in .jpg or .jpeg (case-insensitive) or other formats, continue with the next iteration of the for loop
    if not (nazevSnimku.lower().endswith(".jpg") or
            nazevSnimku.lower().endswith(".jpeg") or
            nazevSnimku.lower().endswith(".png") or
            nazevSnimku.lower().endswith(".tif") or
            nazevSnimku .lower().endswith(".tiff")):
        continue
    # end if

    # show the file name on std out
    print("zpracovava se soubor " + nazevSnimku)

    # get the file name and full path of the current image file
    imageFileWithPath = os.path.join(INPUT_DIR, nazevSnimku)
    # attempt to open the image with OpenCV
    snimek_puvodni = cv2.imread(imageFileWithPath)

    uhel_A = round(5 + random()*10)
    uhel_B = round(5 + random()*15)

    if (uhel_A == uhel_B):
        if(uhel_B<15):
            uhel_B += 3
        else:
            uhel_B -= 3

    uhel_C = 360 - uhel_A

    uhly = [uhel_A, uhel_B, uhel_C]

    # loop over the rotation angles
    # for angle in np.arange(0, 360, 15):
    for uhel_otoceni_vlevo in uhly:
        # otoceni snimku o zadany uhel
        snimek_otoceny = imutils.rotate(snimek_puvodni, uhel_otoceni_vlevo)

        # oriznuti okolni tkane a cernych okraju vzniklych otocenim
        cislo_pripocitane_k_velikosti_vyrezu = round(random() * 20)
        hranice_vyrezu_horni_a_leva = 35 + cislo_pripocitane_k_velikosti_vyrezu
        hranice_vyrezu_dolni_a_prava = 299 - 35 - cislo_pripocitane_k_velikosti_vyrezu
        snimek_otoceny_a_orezany = snimek_otoceny[hranice_vyrezu_horni_a_leva:hranice_vyrezu_dolni_a_prava, hranice_vyrezu_horni_a_leva:hranice_vyrezu_dolni_a_prava]
        print(hranice_vyrezu_dolni_a_prava)
        print(hranice_vyrezu_horni_a_leva)

        # velmi nepatrne doostreni noveho obrazku
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        snimek_otoceny_a_orezany_a_doostreny = cv2.filter2D(snimek_otoceny_a_orezany, -1, kernel)
        mira_pruhlednosti = 0.95
        obrazek_hotovy = cv2.addWeighted(snimek_otoceny_a_orezany_a_doostreny, 1 - mira_pruhlednosti, snimek_otoceny_a_orezany, mira_pruhlednosti, 0)

        # sestaveni noveho nazvu a ulozeni souboru
        cv2.imshow("Otoceny, oriznuty a doostreny snimek", obrazek_hotovy)
        cv2.waitKey(0)

        new_name = "OTOCENY_" + str(uhel_otoceni_vlevo) + "_STUPNU_" + nazevSnimku
        # Save the file to the new path
        new_name = os.path.join(OUTPUT_DIR, new_name)
        print(new_name)

        cv2.imwrite(new_name, snimek_otoceny_a_orezany)


# end for


