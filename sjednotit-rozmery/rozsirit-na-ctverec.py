import os
import shutil
import cv2
from PIL import Image
import numpy as np

INPUT_DIR = r"H:\MachineLearning\SLOUCENY-DATSET\hands\both"

output_dir_name = "rozsirene na ctverec"
OUTPUT_DIR = os.path.join(INPUT_DIR, output_dir_name)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


#######################################################################################################################
def main():
    count_of_processed_files = 0

    # Walk through all files in the directory that contains the files to copy
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

            old_name_and_path = os.path.join(os.path.abspath(subdir), filename)
            print(old_name_and_path)
            base, extension = os.path.splitext(filename)  # Separate base from extension
            new_filename = "ctverec_" + base + extension

            new_name_and_path = os.path.join(OUTPUT_DIR, new_filename)
            # print(new_name_and_path)

            snimek_puvodni = cv2.imread(old_name_and_path)
            vyska_obrazku = np.size(snimek_puvodni, 0)
            sirka_obrazku = np.size(snimek_puvodni, 1)
            print("rozmery jsou " + str(sirka_obrazku) + " x " + str(vyska_obrazku))

            rozdil_rozmeru = sirka_obrazku - vyska_obrazku
            print("rozdil rozmeru je " + str(abs(rozdil_rozmeru)))

            kolik_pridat_na_kazde_strane = abs(rozdil_rozmeru) / 2

            # kolik_pridat_na_strane_A = 0
            # kolik_pridat_na_strane_B = 0

            if rozdil_rozmeru % 2 == 1:
                kolik_pridat_na_strane_A = int(kolik_pridat_na_kazde_strane + 0.5)
                kolik_pridat_na_strane_B = int(kolik_pridat_na_kazde_strane - 0.5)
            else:
                kolik_pridat_na_strane_A = int(kolik_pridat_na_kazde_strane)
                kolik_pridat_na_strane_B = int(kolik_pridat_na_kazde_strane)


            if rozdil_rozmeru == 0: # rozmery stran jsou stejne, nedelame nic a jdeme na dalsi obrazek
                continue
            elif rozdil_rozmeru > 0: # sirka je vetsi, budeme rozsirovat nahore a dole
                # cv2.copyMakeBorder(obrazek, horni, dolni, leva, prava ,typ_okraje, barva)
                snimek_upraveny = cv2.copyMakeBorder(snimek_puvodni, kolik_pridat_na_strane_A, kolik_pridat_na_strane_B, 0, 0,cv2.BORDER_CONSTANT, value=[0, 0, 0])
                print("rozsiruje se nahore o " + str(kolik_pridat_na_strane_A) + " a dole o " + str(kolik_pridat_na_strane_B))
                nova_vyska = vyska_obrazku + kolik_pridat_na_strane_A + kolik_pridat_na_strane_B
                print("nove rozmery jsou " + str(sirka_obrazku) + " x " + str(nova_vyska))

                if (nova_vyska != sirka_obrazku):
                    print()
                    print("!!!!!!!!!!!!!!!!!")
                    print("CHYBAAAAAAAAAAAAA")
                    print("!!!!!!!!!!!!!!!!!")
                    print()

            elif rozdil_rozmeru < 0: # vyska je vetsi, budeme rozsirovat vlevo a vpravo
                snimek_upraveny = cv2.copyMakeBorder(snimek_puvodni, 0, 0, kolik_pridat_na_strane_A, kolik_pridat_na_strane_B, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                print("rozsiruje se vlevo o " + str(kolik_pridat_na_strane_A) + " a vpravo o " + str(kolik_pridat_na_strane_B))
                nova_sirka = sirka_obrazku + kolik_pridat_na_strane_A + kolik_pridat_na_strane_B
                print("nove rozmery jsou " + str(nova_sirka) + " x " + str(vyska_obrazku))


                if (nova_sirka != vyska_obrazku):
                    print()
                    print("!!!!!!!!!!!!!!!!!")
                    print("CHYBAAAAAAAAAAAAA")
                    print("!!!!!!!!!!!!!!!!!")
                    print()
            # end if


            zapsatVystupniSnimekNaDisk(new_name_and_path, snimek_upraveny)

            # Increment and show count of all copied files
            count_of_processed_files += 1
            print("Pocet zpracovanych souboru = " + str(count_of_processed_files))
            print()

        # end for
    # end for


# end main


#######################################################################################################################
def ulozitVystupniSnimek(nazev_snimku, nazev_snimku_vcetne_cesty_k_nemu, oznaceni_kloubu, snimek_k_ulozeni):
    # oriznuti pripony z nazvu souboru
    nazevSnimkuBezPripony = os.path.splitext(nazev_snimku)[0]
    # vyjmuti samotne pripony
    PouzePripona = os.path.splitext(nazev_snimku)[1]

    cestaDoSlozkySeSnimkem = os.path.dirname(nazev_snimku_vcetne_cesty_k_nemu) + "/"  # ziskani cesty do slozky se snimkem

    # pokud se cesta ke snimku rovna ceste ke vstupni slozce (tzn. snimek uz neni dale zanoreny do podslozek)
    if cestaDoSlozkySeSnimkem == INPUT_DIR:
        # jenom zpracovat snimek BEZ zpracovani jmena podslozky

        nazevVystupnihoSnimku = OUTPUT_DIR + nazevSnimkuBezPripony + "_" + oznaceni_kloubu + "_" + PouzePripona
        zapsatVystupniSnimekNaDisk(nazevVystupnihoSnimku, snimek_k_ulozeni)

    # pokud snimek je dale zanoreny do podslozek
    else:
        # zpracovat snimek a zpracovat i jmeno podslozky (tzn. vytvorit ji v cilovem umisteni)

        # ziskani nazvu podslozky, ve ktere je snimek umisteny
        cestaDoSlozkySeSnimkem = os.path.dirname(nazev_snimku_vcetne_cesty_k_nemu)  # ziskani cesty do slozky se snimkem
        nazevPodslozkySeSnimky = os.path.split(cestaDoSlozkySeSnimkem)[1]  # ziskani nazvu pouze posledni slozky

        # vytvoreni podlozky v cilove slozky (pokud jeste neexistuje)
        cilovaSlozkaVcetnePodslozky = OUTPUT_DIR + "/" + nazevPodslozkySeSnimky + "/"
        if not os.path.exists(cilovaSlozkaVcetnePodslozky):
            os.makedirs(cilovaSlozkaVcetnePodslozky)

        nazevVystupnihoSnimku = cilovaSlozkaVcetnePodslozky + nazevSnimkuBezPripony + "_" + oznaceni_kloubu + PouzePripona
        zapsatVystupniSnimekNaDisk(nazevVystupnihoSnimku, snimek_k_ulozeni)
    # end if


# end function


#######################################################################################################################
def zapsatVystupniSnimekNaDisk(nazevVystupnihoSnimkuVcetneCestyKNemu, snimekKteryMaBytUlozen):
    cv2.imwrite(nazevVystupnihoSnimkuVcetneCestyKNemu, snimekKteryMaBytUlozen)
    print("uklada se soubor " + nazevVystupnihoSnimkuVcetneCestyKNemu)
    print("")  # odradkovani


# end function

#######################################################################################################################
if __name__ == "__main__":
    main()
