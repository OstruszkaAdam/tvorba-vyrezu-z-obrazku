from collections import OrderedDict
import numpy as np
import cv2
import os
import pickle

# module-level variables ##############################################################################################
INPUT_IMAGES_DIR = os.getcwd() + "/vstupy/"
OUTPUT_DIR = os.getcwd() + "/vystupy/"

pocet_zpracovanych_kloubu = 0
x_souradnice_kloubu, y_souradnice_kloubu = 0, 0
cropping = False

dorovnavat_rozmery_na_ctverec = True

snimek_puvodni = None
nazev_puvodniho_snimku = None
nazev_puvodniho_snimku_vcetne_cesty_k_nemu = None

souradnice_vsech_kloubu = OrderedDict()

nazvy_vsech_kloubu = {
    # poradi kloubu je od ukazovacku k malicku (tzn od 2 do 5) a od MCP k DIP
    # klouby zapesti a palce nejsou pro tyto ucely relevantni, a proto jsou vynechany

    # MCP vrstva (nejblize k zapesti)
    0: "MCP-2",  # ukazovacek
    1: "MCP-3",  # prostrednicek
    2: "MCP-4",  # prstenicek
    3: "MCP-5",  # malicek

    # PIP vrstva
    4: "PIP-5",  # ukazovacek
    5: "PIP-4",  # prostrednicek
    6: "PIP-3",  # prstenicek
    7: "PIP-2",  # malicek

    # DIP vrstva (kloub mezi predposlednim a poslednim clankem)
    8: "DIP-2",  # ukazovacek
    9: "DIP-3",  # prostrednicek
    10: "DIP-4",  # prstenicek
    11: "DIP-5",  # malicek

    # zapesti
    12: "zapesti"  # malicek
}


#######################################################################################################################
def main():
    global x_souradnice_kloubu, y_souradnice_kloubu, snimek_puvodni, nazev_puvodniho_snimku, nazev_puvodniho_snimku_vcetne_cesty_k_nemu
    x_souradnice_kloubu, y_souradnice_kloubu = 0, 0

    for subdir, dirs, files in os.walk(INPUT_IMAGES_DIR):
        for nazev_puvodniho_snimku in files:

            # nasetovani a vynulovani promennych
            global x_start, y_start, x_end, y_end, cropping
            x_start, y_start = 0, 0
            x_end, y_end = 10,10
            global pocet_zpracovanych_kloubu, cropping, souradnice_vsech_kloubu
            cropping = False
            pocet_zpracovanych_kloubu = 0
            souradnice_vsech_kloubu.clear()

            # preskoceni souboru, ktery neni snimek ###################################################################
            # if the file does not end in .jpg or .jpeg (case-insensitive), continue with the next iteration of the for loop
            if not (nazev_puvodniho_snimku.lower().endswith(".jpg") or
                    nazev_puvodniho_snimku.lower().endswith(".jpeg") or
                    nazev_puvodniho_snimku.lower().endswith(".png") or
                    nazev_puvodniho_snimku.lower().endswith(".tif") or
                    nazev_puvodniho_snimku.lower().endswith(".tiff")):
                continue
            # end if

            # otevrit a zpracovat snimek ##############################################################################
            nazev_puvodniho_snimku_vcetne_cesty_k_nemu = os.path.join(subdir, nazev_puvodniho_snimku)
            print("zpracovava se soubor " + nazev_puvodniho_snimku_vcetne_cesty_k_nemu)

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
                pomer_zmenseni = 0.5
                sirka_okna = round(sirka_obrazku * pomer_zmenseni)
                vyska_okna = round(vyska_obrazku * pomer_zmenseni)

            else:
                sirka_okna = sirka_obrazku
                vyska_okna = vyska_obrazku
            # end if

            cv2.namedWindow('Snimek ke zpracovani', cv2.WINDOW_NORMAL)  # cv2.WINDOW_NORMAL makes the output window resizealbe
            cv2.resizeWindow('Snimek ke zpracovani', sirka_okna, vyska_okna)  # resize the window

            cv2.imshow("Snimek ke zpracovani", snimek_puvodni)
            cv2.setMouseCallback("Snimek ke zpracovani", mouse_crop)

            cv2.waitKey(0)  # 0 = program ceka, dokud nestisknu libovolnou klavesu
            if pocet_zpracovanych_kloubu != 0:
                zapsatPopiskyKvystupnimuSnimkuNaDisk(nazev_puvodniho_snimku_vcetne_cesty_k_nemu, souradnice_vsech_kloubu)
            # end if
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
    global nazvy_vsech_kloubu
    global x_souradnice_kloubu, y_souradnice_kloubu
    global souradnice_vsech_kloubu
    global pomer_zmenseni

    obrazek_ke_zobrazeni = snimek_puvodni.copy()

    # pokud jsme zatim nedosahli mnozstvi kloubu ve snimku
    if pocet_zpracovanych_kloubu < 13:

        # rozmery vyrezu kloubu na prstech odpovidaji vstupnimu formatu inception, ktery je 299x299 px
        kratsi_polovina_strany = 149
        delsi_polovina_strany = 150

        # pokud ale jde o kloub zapesti, je nutne pouzi vetsi rozmer, aby se do vyrezu vubec vesel
        if pocet_zpracovanych_kloubu == 12:
            kratsi_polovina_strany = 249
            delsi_polovina_strany = 250
        # end if

        if event == cv2.EVENT_MOUSEMOVE:
            x_start, y_start = x - kratsi_polovina_strany, y - kratsi_polovina_strany
            x_end, y_end = x + delsi_polovina_strany, y + delsi_polovina_strany

            # barevne zvyrazneni vnitrku vyberu
            cv2.rectangle(obrazek_ke_zobrazeni, (x_start, y_start), (x_end, y_end), (0.0, 165.0, 255.0), -1)

            # pridani polopruhledneho vyberu k puvodnimu obrzaku
            mira_pruhlednosti = 0.75
            obrazek_ke_zobrazeni = cv2.addWeighted(obrazek_ke_zobrazeni, 1 - mira_pruhlednosti, snimek_puvodni, mira_pruhlednosti, 0)

            # ohraniceni vyberu
            cv2.rectangle(obrazek_ke_zobrazeni, (x_start, y_start), (x_end, y_end), (0.0, 165.0, 255.0), 2)

            # zobrazeni obrazku se zvyraznenym vyberem
            cv2.imshow("Snimek ke zpracovani", obrazek_ke_zobrazeni)


        # (x, y) coordinates and indicate that cropping is being
        elif event == cv2.EVENT_LBUTTONDOWN:
            cropping = True
            x_souradnice_kloubu, y_souradnice_kloubu = x, y
            print(str(pocet_zpracovanych_kloubu) + ". kloub v poradi je " + nazvy_vsech_kloubu[pocet_zpracovanych_kloubu]
                  + ", jeho souradnice jsou: x = " + str(x_souradnice_kloubu) + " y = " + str(y_souradnice_kloubu))

        # if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            souradnice_vsech_kloubu.update(
                {nazvy_vsech_kloubu[pocet_zpracovanych_kloubu]: [x_souradnice_kloubu, y_souradnice_kloubu]})
            print(souradnice_vsech_kloubu)

            x_start, y_start = x_souradnice_kloubu - kratsi_polovina_strany, y_souradnice_kloubu - kratsi_polovina_strany
            x_end, y_end = x_souradnice_kloubu + delsi_polovina_strany, y_souradnice_kloubu + delsi_polovina_strany

            # osetreni, aby se souradnice nedostaly mimo obrazek (vadi pouze presah pod nulu)
            if x_start < 0:
                x_start = 0
            # end if
            if y_start < 0:
                y_start = 0
            # end if

            ref_point = [(x_start, y_start), (x_end, y_end)]
            roi = snimek_puvodni[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]

            # pokud je vyrez udelany prilis blizko okraje puvodniho obrazku, je nutne k verzu pridat prazdne misto, aby zustal dodrzen format 299 x 299 px
            tloustka_horniho_ramecku = 0
            tloustka_leveho_ramecku = 0
            tloustka_dolniho_ramecku = 0
            tloustka_praveho_ramecku = 0

            vzdalenost_k_okraji_prava = np.size(snimek_puvodni, 1) - x_souradnice_kloubu
            vzdalenost_k_okraji_dolni = np.size(snimek_puvodni, 0) - y_souradnice_kloubu

            if dorovnavat_rozmery_na_ctverec:
                # levy a horni ramecek
                if x_souradnice_kloubu < kratsi_polovina_strany:
                    tloustka_leveho_ramecku = kratsi_polovina_strany - x_souradnice_kloubu
                # end if
                if y_souradnice_kloubu < kratsi_polovina_strany:
                    tloustka_horniho_ramecku = kratsi_polovina_strany - y_souradnice_kloubu
                # end if
                # pravy a dolni ramecek
                if vzdalenost_k_okraji_prava < delsi_polovina_strany:
                    tloustka_praveho_ramecku = delsi_polovina_strany - vzdalenost_k_okraji_prava
                # end if
                if vzdalenost_k_okraji_dolni < delsi_polovina_strany:
                    tloustka_dolniho_ramecku = delsi_polovina_strany - vzdalenost_k_okraji_dolni
                # end if
                roi = cv2.copyMakeBorder(roi, tloustka_horniho_ramecku, tloustka_dolniho_ramecku, tloustka_leveho_ramecku,
                                         tloustka_praveho_ramecku, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                # cv2.copyMakeBorder(obrazek, horni, dolni, leva, prava ,typ_okraje, barva)
            # end if

            # cropping = False  # cropping is finished

            # tyhle dva radky prijdou asi smazat
            # cv2.imshow("Cropped image", roi)
            # cv2.imwrite(cropped_image_name, roi)

            ulozitVystupniSnimek(nazev_puvodniho_snimku,
                                 nazev_puvodniho_snimku_vcetne_cesty_k_nemu,
                                 nazvy_vsech_kloubu[pocet_zpracovanych_kloubu],
                                 roi)

            x_souradnice_kloubu, y_souradnice_kloubu = 0, 0
            cropping = False  # cropping is finished
            pocet_zpracovanych_kloubu += 1
        # end if
    # pokud uz jsme maximalniho mnozstvi kloubu dosahli
    else:
        if event == cv2.EVENT_LBUTTONDOWN:
            print("Prejdete na dalsi snimek")
            print("")
    # end if


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
    print("uklada se soubor " + nazevVystupnihoSnimkuVcetneCestyKNemu)
    print("")  # odradkovani


# end function


#######################################################################################################################
def zapsatPopiskyKvystupnimuSnimkuNaDisk(nazev_snimku_vcetne_cesty_k_nemu, souradnice_vsech_kloubu):
    nazev_snimku_vcetne_cesty_ale_bez_pripony = nazev_snimku_vcetne_cesty_k_nemu.rsplit('.', 1)[0]  # odebrani obrazove pripony
    nazev_soubory_s_popisky = nazev_snimku_vcetne_cesty_ale_bez_pripony + ".p"  # pridani pripony formatu pickle
    pickle.dump(souradnice_vsech_kloubu, open(
        nazev_soubory_s_popisky, "wb"))

    print("uklada se soubor " + nazev_soubory_s_popisky)
    print("")  # odradkovani


# end function


#######################################################################################################################
if __name__ == "__main__":
    main()
