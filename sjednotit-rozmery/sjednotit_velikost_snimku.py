import os
import shutil
import cv2
from PIL import Image
import numpy as np

INPUT_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_2_rozrezane_na_prave_a_leve_a_prevracene\_NEART"
# OUTPUT_DIR = r"C:\Users\Adam\Desktop\cil"

output_dir_base = os.path.dirname(INPUT_DIR)
output_dir_name = "zmensene"

OUTPUT_DIR = os.path.join(output_dir_base, output_dir_name)
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

TARGET_SIZE = 299


#######################################################################################################################
def main():
    count_of_processed_files = 0

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

            old_name_and_path = os.path.join(os.path.abspath(root), filename)
            print(old_name_and_path)

            # snimek_puvodni = cv2.imread(old_name_and_path)
            snimek_puvodni = Image.open(old_name_and_path)
            sirka_obrazku, vyska_obrazku = snimek_puvodni.size
            print("rozmery jsou " + str(sirka_obrazku) + " x " + str(vyska_obrazku))

            action_name = ""
            base, extension = os.path.splitext(filename)  # Separate base from extension

            newsize = (TARGET_SIZE, TARGET_SIZE)


            # TODO predeleat pouze na jeden rozmer (je to prece ctverec)
            if sirka_obrazku < TARGET_SIZE:
                # snimek_prevzorkovany = cv2.resize(snimek_puvodni, (TARGET_SIZE, TARGET_SIZE), interpolation = cv2.CV_INTER_CUBIC)

                snimek_prevzorkovany = snimek_puvodni.resize(newsize, Image.ANTIALIAS)
                action_name = "upscaled"
                new_name = base + "_" + action_name + "_" + extension  # Create new name
                new_name = os.path.join(OUTPUT_DIR, new_name)

                snimek_prevzorkovany_opencv = np.array(snimek_prevzorkovany)    # Convert to OpenCV
                snimek_prevzorkovany_opencv = snimek_prevzorkovany_opencv[:, :, ::-1].copy()    # Convert RGB to BGR
                cv2.imwrite(new_name, snimek_prevzorkovany_opencv)
                print(action_name)
                print("uklada se soubor " + str(new_name))

            elif sirka_obrazku > TARGET_SIZE:   # samostatnou vetev pro vetsi sirku ponechavam, aby se neztratila infromace o provedene akci a aby bylo mozne pripadne zvolit jinou metodu interpolace pro zmensovani
                # snimek_prevzorkovany = cv2.resize(snimek_puvodni, (TARGET_SIZE, TARGET_SIZE), interpolation=cv2.INTER_AREA) # INTER_AREA je vhodna pro zmensovani, nevytvari tolik sumu v obraze

                snimek_prevzorkovany = snimek_puvodni.resize(newsize, Image.ANTIALIAS)
                action_name = "downscaled"
                new_name = base + "_" + action_name + "_" + extension  # Create new name
                new_name = os.path.join(OUTPUT_DIR, new_name)

                snimek_prevzorkovany_opencv = np.array(snimek_prevzorkovany)    # Convert to OpenCV
                snimek_prevzorkovany_opencv = snimek_prevzorkovany_opencv[:, :, ::-1].copy()    # Convert RGB to BGR
                cv2.imwrite(new_name, snimek_prevzorkovany_opencv)
                print(action_name)
                print("uklada se soubor " + str(new_name))

            elif sirka_obrazku == TARGET_SIZE:
                action_name = "untouched"
                # vytvoreni noveho nazvu
                new_name = base + "_" + action_name + "_" + extension  # Create new name

                # Save the file to the new path
                new_name = os.path.join(OUTPUT_DIR, new_name)
                print(new_name)

                shutil.copyfile(old_name_and_path, new_name)
            # end if

            # print(action_name)

            # Increment and show count of all copied files
            count_of_processed_files += 1
            print("Count of copied files = " + str(count_of_processed_files))
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