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
import numpy as np
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter


TARGET_SIZE = 299

INPUT_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_5_ruce_trenovaci_testovaci\01_Rotridene hi-res bez uprav\01_Train\RA"
OUTPUT_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_5_ruce_trenovaci_testovaci\02_low-res augmentovane\RA"

input_dir_name = os.path.basename(INPUT_DIR)
output_dir_base = os.path.dirname(INPUT_DIR)
output_dir_name = input_dir_name + " otocene_fake 299px"
# output_dir_name = "otocene_fake_" + str(TARGET_SIZE)

# OUTPUT_DIR = os.path.join(output_dir_base, output_dir_name)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


count_of_processed_files = 0

kolik_pridat_na_strane_A = 0
kolik_pridat_na_strane_B = 0
rozdil_rozmeru = 0

#######################################################################################################################
def main():
    global count_of_processed_files, kolik_pridat_na_strane_A, kolik_pridat_na_strane_B, rozdil_rozmeru

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
                obrazek_otoceny, sirka_otoceneho_obrazku, vyska_otoceneho_obrazku = rotate_transform(snimek_puvodni, uhel_otoceni)

                # KONEC OTACENI

                # ZACATEK ROZSIROVANI NA CTVEREC

                rozdil_rozmeru = sirka_otoceneho_obrazku - vyska_otoceneho_obrazku
                abs_rozdil = abs(rozdil_rozmeru)
                print("rozdil rozmeru je " + str(abs_rozdil))

                kolik_pridat_na_kazde_strane = abs(rozdil_rozmeru) / 2

                if rozdil_rozmeru % 2 == 1:
                    kolik_pridat_na_strane_A = int(kolik_pridat_na_kazde_strane + 0.5)
                    kolik_pridat_na_strane_B = int(kolik_pridat_na_kazde_strane - 0.5)
                else:
                    kolik_pridat_na_strane_A = int(kolik_pridat_na_kazde_strane)
                    kolik_pridat_na_strane_B = int(kolik_pridat_na_kazde_strane)

                if rozdil_rozmeru == 0:  # rozmery stran jsou stejne, nedelame nic a jdeme na dalsi obrazek
                    continue
                elif rozdil_rozmeru > 0:  # sirka je vetsi, neresime
                   continue

                elif rozdil_rozmeru < 0:  # vyska je vetsi, budeme rozsirovat vlevo a vpravo
                    if (abs_rozdil > 100):
                        obrazek_ctvercovy = cv2.copyMakeBorder(obrazek_otoceny, 0, 0, kolik_pridat_na_strane_A + 50,
                                                               kolik_pridat_na_strane_B - 50, cv2.BORDER_CONSTANT,
                                                               value=[0, 0, 0])
                        print(
                            "rozsiruje se vlevo o " + str(kolik_pridat_na_strane_A) + " a vpravo o " + str(
                                kolik_pridat_na_strane_B))
                        nova_sirka = sirka_otoceneho_obrazku + kolik_pridat_na_strane_A + kolik_pridat_na_strane_B
                        print("nove rozmery jsou " + str(nova_sirka) + " x " + str(vyska_otoceneho_obrazku))
                    elif (50 <= abs_rozdil <= 100):
                        obrazek_ctvercovy = cv2.copyMakeBorder(obrazek_otoceny, 0, 0, kolik_pridat_na_strane_A + 25,
                                                               kolik_pridat_na_strane_B - 25, cv2.BORDER_CONSTANT,
                                                               value=[0, 0, 0])
                        print(
                            "rozsiruje se vlevo o " + str(kolik_pridat_na_strane_A) + " a vpravo o " + str(
                                kolik_pridat_na_strane_B))
                        nova_sirka = sirka_otoceneho_obrazku + kolik_pridat_na_strane_A + kolik_pridat_na_strane_B
                        print("nove rozmery jsou " + str(nova_sirka) + " x " + str(vyska_otoceneho_obrazku))
                    elif (abs_rozdil < 50):
                        obrazek_ctvercovy = cv2.copyMakeBorder(obrazek_otoceny, 0, 0, kolik_pridat_na_strane_A + 15,
                                                               kolik_pridat_na_strane_B - 15, cv2.BORDER_CONSTANT,
                                                               value=[0, 0, 0])
                        print(
                            "rozsiruje se vlevo o " + str(kolik_pridat_na_strane_A) + " a vpravo o " + str(
                                kolik_pridat_na_strane_B))
                        nova_sirka = sirka_otoceneho_obrazku + kolik_pridat_na_strane_A + kolik_pridat_na_strane_B
                        print("nove rozmery jsou " + str(nova_sirka) + " x " + str(vyska_otoceneho_obrazku))

                    # end if

                    # KONEC ROZSIROVANI NA CTVEREC

                    # ZACATEK ZMENSOVANI

                    vstup_do_pillow = cv2.cvtColor(obrazek_ctvercovy, cv2.COLOR_BGR2RGB)
                    obazek_zmenseny = Image.fromarray(vstup_do_pillow)

                    sirka_obrazku, vyska_obrazku = obazek_zmenseny.size
                    print("rozmery jsou " + str(sirka_obrazku) + " x " + str(vyska_obrazku))

                    action_name = ""
                    base, extension = os.path.splitext(filename)  # Separate base from extension

                    newsize = (900, 900)

                    snimek_prevzorkovany = obazek_zmenseny.resize(newsize, Image.ANTIALIAS)

                    snimek_prevzorkovany_opencv = np.array(snimek_prevzorkovany)  # Convert to OpenCV
                    snimek_prevzorkovany_opencv = snimek_prevzorkovany_opencv[:, :, ::-1].copy()  # Convert RGB to BGR

                    # KONEC ZMENSOVANI

                    snimek_elastic = elastic_transform(snimek_prevzorkovany_opencv,300,7)


                    # ZACATEK ZMENSOVANI

                    vstup_do_pillow = cv2.cvtColor(snimek_elastic, cv2.COLOR_BGR2RGB)
                    snimek_elastic_zmenseny = Image.fromarray(vstup_do_pillow)

                    sirka_obrazku, vyska_obrazku = snimek_elastic_zmenseny.size
                    print("rozmery jsou " + str(sirka_obrazku) + " x " + str(vyska_obrazku))

                    action_name = ""

                    newsize = (TARGET_SIZE, TARGET_SIZE)

                    snimek_prevzorkovany_dalsi = snimek_elastic_zmenseny.resize(newsize, Image.ANTIALIAS)

                    snimek_prevzorkovany_opencv_dalsi = np.array(snimek_prevzorkovany_dalsi)  # Convert to OpenCV
                    snimek_prevzorkovany_opencv_dalsi = snimek_prevzorkovany_opencv_dalsi[:, :, ::-1].copy()  # Convert RGB to BGR

                    # KONEC ZMENSOVANI





                    # oriznuti pripony z nazvu souboru
                    nazevSnimkuBezPripony = os.path.splitext(filename)[0]
                    # vyjmuti samotne pripony
                    # PouzePripona = os.path.splitext(nazev_snimku)[1]
                    pouze_pripona = ".jpg"

                    rozhazene_poradi = round(random() * 1000)
                    rozhazene_poradi = rozhazene_poradi + round(random() * 100)
                    rozhazene_poradi = str(rozhazene_poradi)

                    new_name = rozhazene_poradi + "_" + nazevSnimkuBezPripony + "_elastic" + pouze_pripona

                    # new_name = "OTOCENY_" + str(uhel_otoceni) + "_STUPNU_" + nazevSnimkuBezPripony + PouzePripona
                    # Save the file to the new path
                    new_name = os.path.join(OUTPUT_DIR, new_name)

                    # cv2.imwrite(new_name, snimek_prevzorkovany_opencv)
                    cv2.imwrite(new_name, snimek_prevzorkovany_opencv_dalsi, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

                    print("uklada se soubor " + str(new_name))

    # end for


def rotate_transform(snimek_puvodni, uhel_otoceni):
    snimek_otoceny = imutils.rotate_bound(snimek_puvodni, uhel_otoceni)
    snimek_otoceny_a_orezany = snimek_otoceny
    # velmi nepatrne doostreni noveho obrazku
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    snimek_otoceny_a_orezany_a_doostreny = cv2.filter2D(snimek_otoceny_a_orezany, -1, kernel)
    mira_pruhlednosti = 0.93
    obrazek_otoceny = cv2.addWeighted(snimek_otoceny_a_orezany_a_doostreny, 1 - mira_pruhlednosti,
                                      snimek_otoceny_a_orezany,
                                      mira_pruhlednosti, 0)
    # random oriznuti
    uhel_absolutni_velikost = abs(uhel_otoceni)
    vyska_otoceneho_obrazku = np.size(obrazek_otoceny, 0)
    sirka_otoceneho_obrazku = np.size(obrazek_otoceny, 1)
    nahodna_velikost_orezu = round(random() * 15)  # nahodny rozmer oriznuteho pruhu
    velikost_orezu_horni = uhel_absolutni_velikost * 6 + nahodna_velikost_orezu
    velikost_orezu_leva_prava = uhel_absolutni_velikost * 5
    velikost_orezu_dolni = velikost_orezu_horni + round(uhel_absolutni_velikost * 10)
    x_start, y_start = velikost_orezu_leva_prava, velikost_orezu_horni
    x_end, y_end = sirka_otoceneho_obrazku - velikost_orezu_leva_prava, vyska_otoceneho_obrazku - velikost_orezu_dolni
    ref_point = [(x_start, y_start), (x_end, y_end)]
    # ref_point = [(0, y_start), (sirka_otoceneho_obrazku, y_end)]
    obrazek_otoceny = obrazek_otoceny[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
    return obrazek_otoceny, sirka_otoceneho_obrazku, vyska_otoceneho_obrazku

#######################################################################################################################
def elastic_transform(image, alpha, sigma):
    """Elastic deformation of images as described in [Simard2003]_.
    .. [Simard2003] Simard, Steinkraus and Platt, "Best Practices for
       Convolutional Neural Networks applied to Visual Document Analysis", in
       Proc. of the International Conference on Document Analysis and
       Recognition, 2003.
       SIGMA... cim nizsi cislo, tim vyraznejsi mira zkrouceni. Pouzitelne jsou hodnoty 8 a vyse. Nad 10 uz nedela temer nic.
       ALPHA... stejne jak sigma, ale opacny ucinek. Tady urcuje miru zkrouceni, ale cim vyssi hodnota, tim vetsi ucinek. Hodnoty zhruba okolo 500
    """

    alpha = 300
    sigma = 8
    random_state = np.random.RandomState(None)

    shape = image.shape
    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dz = np.zeros_like(dx)

    x, y, z = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), np.arange(shape[2]))
    print(x.shape)
    indices = np.reshape(y+dy, (-1, 1)), np.reshape(x+dx, (-1, 1)), np.reshape(z, (-1, 1))

    distored_image = map_coordinates(image, indices, order=1, mode='reflect')
    return distored_image.reshape(image.shape)

#######################################################################################################################
if __name__ == "__main__":
    main()
