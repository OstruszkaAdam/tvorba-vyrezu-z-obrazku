import numpy as np
import cv2
import os

# module-level variables ##############################################################################################
INPUT_IMAGES_DIR = os.getcwd() + "/vstupy/"
OUTPUT_DIR = os.getcwd() + "/vystupy/"

pocet_zpracovanych_kloubu = 0
xx, yy = 0, 0
cropping = False

snimek_puvodni = None
nazev_puvodniho_snimku = None
nazev_puvodniho_snimku_vcetne_cesty_k_nemu = None



#######################################################################################################################
def main():

    global xx, yy, snimek_puvodni, nazev_puvodniho_snimku, nazev_puvodniho_snimku_vcetne_cesty_k_nemu
    xx, yy = 0, 0

    for subdir, dirs, files in os.walk(INPUT_IMAGES_DIR):
        for nazev_puvodniho_snimku in files:

            # preskoceni souboru, ktery neni snimek ###################################################################
            # if the file does not end in .jpg or .jpeg (case-insensitive), continue with the next iteration of the for loop
            if not (nazev_puvodniho_snimku.lower().endswith(".jpg") or
                    nazev_puvodniho_snimku.lower().endswith(".jpeg") or
                    nazev_puvodniho_snimku.lower().endswith(".png") or
                    nazev_puvodniho_snimku.lower().endswith(".tiff") or
                    nazev_puvodniho_snimku.lower().endswith(".tif")):
                continue
            # end if

            # otevrit a zpracovat snimek ##############################################################################
            nazev_puvodniho_snimku_vcetne_cesty_k_nemu = os.path.join(subdir, nazev_puvodniho_snimku)
            print("zpracovava se soubor " + nazev_puvodniho_snimku_vcetne_cesty_k_nemu)

            global pocet_zpracovanych_kloubu, cropping
            cropping = False
            pocet_zpracovanych_kloubu = 0

            snimek_puvodni = cv2.imread(nazev_puvodniho_snimku_vcetne_cesty_k_nemu)
            # if we were not able to successfully open the image, continue with the next iteration of the for loop
            if snimek_puvodni is None:
                print("soubor s nazvem " + nazev_puvodniho_snimku + " se nepovedlo nacist do OpenCV")
                continue
            # end if

            # zobrazit snimek (tak, aby se vesel na monitor) ##########################################################
            vyska_obrazku = np.size(snimek_puvodni, 0)
            sirka_obrazku = np.size(snimek_puvodni, 1)

            if vyska_obrazku > 1000:
                sirka_okna = round(sirka_obrazku * 0.6)
                vyska_okna = round(vyska_obrazku * 0.6)

            else:
                sirka_okna = sirka_obrazku
                vyska_okna = vyska_obrazku
            # end if

            cv2.namedWindow('Snimek ke zpracovani', cv2.WINDOW_NORMAL)  # cv2.WINDOW_NORMAL makes the output window resizealbe
            cv2.resizeWindow('Snimek ke zpracovani', sirka_okna, vyska_okna)  # resize the window

            cv2.imshow("Snimek ke zpracovani", snimek_puvodni)
            cv2.setMouseCallback("Snimek ke zpracovani", mouse_crop)

            cv2.waitKey(0)  # 0 = program ceka, dokud nestisknu libovolnou klavesu
            cv2.destroyWindow("Snimek ke zpracovani")
            cv2.destroyAllWindows()

            # zpracovat snimek #########################################################################################

        # end for
    # end for


# end main


#######################################################################################################################
def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global pocet_zpracovanych_kloubu
    global x_start, y_start, x_end, y_end, cropping
    global snimek_puvodni, nazev_puvodniho_snimku, nazev_puvodniho_snimku_vcetne_cesty_k_nemu
    global xx, yy

    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        cropping = True
        xx, yy = x, y
        pocet_zpracovanych_kloubu += 1
        print("Souřadnice kloubu číslo " + str(pocet_zpracovanych_kloubu) + " jsou: x = " + str(xx) + " y = " + str(yy))

    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # cropping = False  # cropping is finished
        x_start, y_start = xx - 150, yy - 150
        x_end, y_end = xx + 150, yy + 150

        # osetreni, aby se souradnice nedostaly mimo obrazek (vadi pouze presah pod nulu)
        if x_start < 0:
            x_start = 0
        # end if
        if y_start < 0:
            y_start = 0
        # end if


        ref_point = [(x_start, y_start), (x_end, y_end)]
        roi = snimek_puvodni[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
        cropped_image_name = "Cropped image " + str(pocet_zpracovanych_kloubu) + ".jpg"

        # tyhle dva radky prijdou asi smazat
        cv2.imshow("Cropped image", roi)
        # cv2.imwrite(cropped_image_name, roi)

        ulozitVystupniSnimek(nazev_puvodniho_snimku, nazev_puvodniho_snimku_vcetne_cesty_k_nemu, cropped_image_name, roi)

        xx, yy = 0, 0
        cropping = False  # cropping is finished


#######################################################################################################################
def ulozitVystupniSnimek(nazev_snimku, nazev_snimku_vcetne_cesty_k_nemu, oznaceni_kloubu, snimek_k_ulozeni):
    # oriznuti pripony z nazvu souboru
    nazevSnimkuBezPripony = os.path.splitext(nazev_snimku)[0]
    # vyjmuti samotne pripony
    PouzePripona = os.path.splitext(nazev_snimku)[1]

    cestaDoSlozkySeSnimkem = os.path.dirname(nazev_snimku_vcetne_cesty_k_nemu) + "/"  # ziskani cesty do slozky se snimkem

    # pokud se cesta ke snimku rovna ceste ke vstupni slozce (tzn. snimek uz neni dale zanoreny do podslozek)
    if cestaDoSlozkySeSnimkem == INPUT_IMAGES_DIR:
        # jenom zpracovat snimek BEZ zpracovani jmena podslozky

        nazevVystupnihoSnimku = OUTPUT_DIR + nazevSnimkuBezPripony + "_" + oznaceni_kloubu + PouzePripona
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


# end function

#######################################################################################################################
if __name__ == "__main__":
    main()
