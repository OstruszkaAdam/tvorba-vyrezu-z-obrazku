from collections import OrderedDict
import numpy as np
import cv2
import os
import pickle
import fnmatch

# module-level variables ##############################################################################################
# INPUT_IMAGES_DIR = os.getcwd() + "/vstupy/"
INPUT_IMAGES_DIR = r"H:\MachineLearning\OZ_nove datasety_leto2019\_roztridene ruce\_2_rozrezane_na_prave_a_leve_a_prevracene\_RA\originaly_a_souradnice\1-2znaky"
# OUTPUT_DIR = os.getcwd() + "/vystupy/"

output_dir_abs = "Rozrezane (absolutni rozmery)"
output_dir_rel = "Rozrezane (relativni rozmery)"

OUTPUT_DIR = os.path.join(INPUT_IMAGES_DIR, output_dir_abs)
OUTPUT_DIR_REL = os.path.join(INPUT_IMAGES_DIR, output_dir_rel)

kolik_oriznout_z_vyberu = 0

pocet_zpracovanych_snimku = 0
pocet_zpracovanych_kloubu = 0
x_souradnice_kloubu, y_souradnice_kloubu = 0, 0
cropping = False
relativni_velikost_vyrezu = False

dorovnavat_rozmery_na_ctverec = True

snimek_puvodni = None
filename = None
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
    12: "RK"  # malicek
}


#######################################################################################################################
def main():
    global x_souradnice_kloubu, y_souradnice_kloubu, snimek_puvodni, filename, nazev_puvodniho_snimku_vcetne_cesty_k_nemu
    x_souradnice_kloubu, y_souradnice_kloubu = 0, 0

    # pocet snimku ve slozce (bez vnorenych slozek)
    image_count_jpg = len(fnmatch.filter(os.listdir(INPUT_IMAGES_DIR), '*.jpg'))
    image_count_jpeg = len(fnmatch.filter(os.listdir(INPUT_IMAGES_DIR), '*.jpeg'))
    image_count_png = len(fnmatch.filter(os.listdir(INPUT_IMAGES_DIR), '*.png'))
    image_count_tif = len(fnmatch.filter(os.listdir(INPUT_IMAGES_DIR), '*.tif'))
    image_count_tiff = len(fnmatch.filter(os.listdir(INPUT_IMAGES_DIR), '*.tiff'))
    image_count_total = image_count_jpg + image_count_jpeg + image_count_png + image_count_tif + image_count_tiff

    for subdir, dirs, files in os.walk(INPUT_IMAGES_DIR):
        for filename in files:
            # nasetovani a vynulovani promennych
            global x_start, y_start, x_end, y_end, cropping
            x_start, y_start = 0, 0
            x_end, y_end = 10, 10
            global pocet_zpracovanych_snimku, pocet_zpracovanych_kloubu, cropping, souradnice_vsech_kloubu
            cropping = False
            pocet_zpracovanych_kloubu = 0
            souradnice_vsech_kloubu.clear()

            # preskoceni souboru, ktery neni snimek ###################################################################
            # if the file does not end in .jpg or .jpeg (case-insensitive), continue with the next iteration of the for loop
            if not (filename.lower().endswith(".jpg") or
                    filename.lower().endswith(".jpeg") or
                    filename.lower().endswith(".png") or
                    filename.lower().endswith(".tif") or
                    filename.lower().endswith(".tiff")):
                continue
            # end if

            # otevrit a zpracovat snimek ##############################################################################
            nazev_puvodniho_snimku_vcetne_cesty_k_nemu = os.path.join(subdir, filename)

            pocet_zpracovanych_snimku += 1
            kolik_z_kolika_je_zpracovano = str(pocet_zpracovanych_snimku) + " z " + str(image_count_total) + " celkem"

            print("Zpracovava se soubor " + kolik_z_kolika_je_zpracovano + ": " + nazev_puvodniho_snimku_vcetne_cesty_k_nemu)

            snimek_puvodni = cv2.imread(nazev_puvodniho_snimku_vcetne_cesty_k_nemu)
            # if we were not able to successfully open the image, continue with the next iteration of the for loop
            if snimek_puvodni is None:
                print("Soubor s nazvem " + filename + " se nepovedlo nacist do OpenCV")
                continue
            # end if

            # pokud uz byl vytvoren soubor se souradnicemu kloubu (tzn. pokud byl snimek uz zpracovat) preskocime dal
            nazev_bez_pripony = os.path.splitext(filename)[0]
            nezev_souboru_se_souradnicemi = nazev_bez_pripony + ".p"
            nezev_souboru_se_souradnicemi_vcetne_cesty_k_nemu = os.path.join(subdir, nezev_souboru_se_souradnicemi)

            if os.path.isfile(nezev_souboru_se_souradnicemi_vcetne_cesty_k_nemu):
                print("Soubor uz byl zpracovan drive (souradnice kloubu jiz jsou ulozeny)")
                print("")
                continue
            # end if

            # zobrazit snimek (tak, aby se vesel na monitor) ##########################################################
            vyska_obrazku = np.size(snimek_puvodni, 0)
            sirka_obrazku = np.size(snimek_puvodni, 1)
            print("rozmery jsou " + str(sirka_obrazku) + " x " + str(vyska_obrazku))

            if vyska_obrazku > 1000:
                vyska_okna = 1000   # vysku okna stanovim napevno
                pomer_zmenseni = 1000 / vyska_obrazku   # vypocitam pomer zmenseni tak, aby odpovidal cilove vysce 1000 px
                sirka_okna = round(sirka_obrazku * pomer_zmenseni)  # s pomerem nasledne dopocitam sirku


            else:
                sirka_okna = sirka_obrazku
                vyska_okna = vyska_obrazku
            # end if

            cv2.namedWindow('Tvorba vyrezu kloubu', cv2.WINDOW_NORMAL)  # cv2.WINDOW_NORMAL makes the output window resizealbe
            cv2.resizeWindow('Tvorba vyrezu kloubu', sirka_okna, vyska_okna)  # resize the window

            cv2.imshow("Tvorba vyrezu kloubu", snimek_puvodni)
            cv2.setMouseCallback("Tvorba vyrezu kloubu", mouse_crop)

            cv2.waitKey(0)  # 0 = program ceka, dokud nestisknu libovolnou klavesu
            if pocet_zpracovanych_kloubu == 13:
                zapsatPopiskyKvystupnimuSnimkuNaDisk(nazev_puvodniho_snimku_vcetne_cesty_k_nemu, souradnice_vsech_kloubu)
            # end if
            cv2.destroyWindow("Tvorba vyrezu kloubu")
            cv2.destroyAllWindows()

            # zpracovat snimek #########################################################################################

        # end for
    # end for


# end main

#######################################################################################################################
def mouse_crop(event, x, y, flag=0, param=None):
    # grab references to the global variables
    global pocet_zpracovanych_kloubu
    global x_start, y_start, x_end, y_end, cropping
    global snimek_puvodni, filename, nazev_puvodniho_snimku_vcetne_cesty_k_nemu
    global nazvy_vsech_kloubu
    global x_souradnice_kloubu, y_souradnice_kloubu
    global souradnice_vsech_kloubu
    global pomer_zmenseni

    obrazek_ke_zobrazeni = snimek_puvodni.copy()

    # podklady pro vypocet relativnich rozmeru vyrezu
    sirka_obrazku = np.size(snimek_puvodni, 1)
    rozmer_vyrezu_kloubu_prstu = round(sirka_obrazku * 0.18)
    rozmer_vyrezu_kloubu_zapesti = round(sirka_obrazku * 0.3)

    # pokud jsme zatim nedosahli mnozstvi kloubu ve snimku
    if pocet_zpracovanych_kloubu < 13:

        # rozmery vyrezu kloubu na prstech odpovidaji vstupnimu formatu inception, ktery je 299x299 px
        kratsi_polovina_strany = 149
        delsi_polovina_strany = 150

        #relativni rozmery
        kratsi_polovina_strany_rel = round(rozmer_vyrezu_kloubu_prstu / 2) - 1
        delsi_polovina_strany_rel = round(rozmer_vyrezu_kloubu_prstu / 2)

        # pokud ale jde o kloub zapesti, je nutne pouzi vetsi rozmer, aby se do vyrezu vubec vesel
        if pocet_zpracovanych_kloubu == 12:
            kratsi_polovina_strany = 249
            delsi_polovina_strany = 250

            # relativni rozmery
            kratsi_polovina_strany_rel = round(rozmer_vyrezu_kloubu_zapesti / 2) - 1
            delsi_polovina_strany_rel = round(rozmer_vyrezu_kloubu_zapesti / 2)
        # end if

        global kolik_oriznout_z_vyberu

        if event == cv2.EVENT_MOUSEWHEEL:
            if flag > 0:  # Scroll up
                kolik_oriznout_z_vyberu = kolik_oriznout_z_vyberu + 5
                get_coordinates_and_refresh_screen(delsi_polovina_strany, delsi_polovina_strany_rel, kolik_oriznout_z_vyberu,
                                                   kratsi_polovina_strany, kratsi_polovina_strany_rel, obrazek_ke_zobrazeni,
                                                   snimek_puvodni, x, y)

            elif flag < 0:  # Scroll down
                kolik_oriznout_z_vyberu = kolik_oriznout_z_vyberu - 5
                get_coordinates_and_refresh_screen(delsi_polovina_strany, delsi_polovina_strany_rel, kolik_oriznout_z_vyberu,
                                                   kratsi_polovina_strany, kratsi_polovina_strany_rel, obrazek_ke_zobrazeni,
                                                   snimek_puvodni, x, y)


        elif event == cv2.EVENT_MOUSEMOVE:

            get_coordinates_and_refresh_screen(delsi_polovina_strany, delsi_polovina_strany_rel, kolik_oriznout_z_vyberu,
                                               kratsi_polovina_strany, kratsi_polovina_strany_rel, obrazek_ke_zobrazeni,
                                               snimek_puvodni, x, y)


        # (x, y) coordinates and indicate that cropping is being
        elif event == cv2.EVENT_LBUTTONDOWN:
            cropping = True
            x_souradnice_kloubu, y_souradnice_kloubu = x, y

            # pokud uzivatel klikne do roku, povazuje to program za neexistujici kloub, ktery reprezentuje nulovymi souradnicemi snimek nebude ukladat
            if (x, y) < (30, 30):
                x_souradnice_kloubu, y_souradnice_kloubu = 0,0
            # end if

            print(str(pocet_zpracovanych_kloubu + 1) + ". kloub v poradi je " + nazvy_vsech_kloubu[pocet_zpracovanych_kloubu]
                  + ", jeho souradnice jsou: x = " + str(x_souradnice_kloubu) + " y = " + str(y_souradnice_kloubu))

        # if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            souradnice_vsech_kloubu.update(
                {nazvy_vsech_kloubu[pocet_zpracovanych_kloubu]: [x_souradnice_kloubu, y_souradnice_kloubu]})
            print(souradnice_vsech_kloubu)

            x_start, y_start = x - kratsi_polovina_strany, y - kratsi_polovina_strany
            x_end, y_end = x + delsi_polovina_strany, y + delsi_polovina_strany

            x_start_rel, y_start_rel = x - (kratsi_polovina_strany_rel + kolik_oriznout_z_vyberu), y - (kratsi_polovina_strany_rel + kolik_oriznout_z_vyberu)
            x_end_rel, y_end_rel = x + delsi_polovina_strany_rel + kolik_oriznout_z_vyberu, y + delsi_polovina_strany_rel + kolik_oriznout_z_vyberu

            # osetreni, aby se souradnice nedostaly mimo obrazek (vadi pouze presah pod nulu)
            if x_start < 0:
                x_start = 0
            # end if
            if y_start < 0:
                y_start = 0
            # end if

            ref_point = [(x_start, y_start), (x_end, y_end)]
            roi = snimek_puvodni[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]

            ref_point_rel = [(x_start_rel, y_start_rel), (x_end_rel, y_end_rel)]
            roi_rel = snimek_puvodni[ref_point_rel[0][1]:ref_point_rel[1][1], ref_point_rel[0][0]:ref_point_rel[1][0]]

            # pokud je vyrez udelany prilis blizko okraje puvodniho obrazku, je nutne k verzu pridat prazdne misto, aby zustal dodrzen format 299 x 299 px
            tloustka_horniho_ramecku = 0
            tloustka_leveho_ramecku = 0
            tloustka_dolniho_ramecku = 0
            tloustka_praveho_ramecku = 0

            vzdalenost_k_okraji_prava = np.size(snimek_puvodni, 1) - x_souradnice_kloubu
            vzdalenost_k_okraji_dolni = np.size(snimek_puvodni, 0) - y_souradnice_kloubu

            if dorovnavat_rozmery_na_ctverec:
                # absolutni rozmery

                # levy a horni ramecek
                roi = spocitat_rozmery_a_vytvorit_vyrez(
                    delsi_polovina_strany, kratsi_polovina_strany, roi, tloustka_dolniho_ramecku, tloustka_horniho_ramecku,
                    tloustka_leveho_ramecku, tloustka_praveho_ramecku, vzdalenost_k_okraji_dolni, vzdalenost_k_okraji_prava,
                    x_souradnice_kloubu, y_souradnice_kloubu)

                # relativni rozmery

                # levy a horni ramecek
                roi_rel = spocitat_rozmery_a_vytvorit_vyrez(
                    delsi_polovina_strany_rel, kratsi_polovina_strany_rel, roi_rel, tloustka_dolniho_ramecku, tloustka_horniho_ramecku,
                    tloustka_leveho_ramecku, tloustka_praveho_ramecku, vzdalenost_k_okraji_dolni, vzdalenost_k_okraji_prava,
                    x_souradnice_kloubu, y_souradnice_kloubu)

            # end if

            # cropping = False  # cropping is finished

            # tyhle dva radky prijdou asi smazat
            # cv2.imshow("Cropped image", roi)
            # cv2.imwrite(cropped_image_name, roi)

            if (x_souradnice_kloubu, y_souradnice_kloubu) > (0, 0): # ulozime vyrez, ale pouze pokud kloub existuje (tzn. pokud ma nenulove souradnice)
                ulozitVystupniSnimky(filename,
                                     nazev_puvodniho_snimku_vcetne_cesty_k_nemu,
                                     nazvy_vsech_kloubu[pocet_zpracovanych_kloubu],
                                     roi, roi_rel)
            # end if


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
def spocitat_rozmery_a_vytvorit_vyrez(delsi_polovina_strany, kratsi_polovina_strany, roi, tloustka_dolniho_ramecku, tloustka_horniho_ramecku,
                                      tloustka_leveho_ramecku, tloustka_praveho_ramecku, vzdalenost_k_okraji_dolni, vzdalenost_k_okraji_prava,
                                      x_souradnice_kloubu, y_souradnice_kloubu):
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
    if vzdalenost_k_okraji_dolni < delsi_polovina_strany :
        tloustka_dolniho_ramecku = delsi_polovina_strany - vzdalenost_k_okraji_dolni
    # end if
    roi = cv2.copyMakeBorder(roi, tloustka_horniho_ramecku, tloustka_dolniho_ramecku, tloustka_leveho_ramecku,
                             tloustka_praveho_ramecku, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    # cv2.copyMakeBorder(obrazek, horni, dolni, leva, prava ,typ_okraje, barva)
    return roi


#######################################################################################################################
def get_coordinates_and_refresh_screen(delsi_polovina_strany, delsi_polovina_strany_rel, kolik_oriznout_z_vyberu,
                                       kratsi_polovina_strany, kratsi_polovina_strany_rel, obrazek_ke_zobrazeni, snimek_puvodni,
                                       x, y):
    global x_start, y_start, x_end, y_end
    x_start, y_start = x - kratsi_polovina_strany, y - kratsi_polovina_strany
    x_end, y_end = x + delsi_polovina_strany, y + delsi_polovina_strany
    x_start_rel, y_start_rel = x - (kratsi_polovina_strany_rel + kolik_oriznout_z_vyberu), y - (
                kratsi_polovina_strany_rel + kolik_oriznout_z_vyberu)
    x_end_rel, y_end_rel = x + delsi_polovina_strany_rel + kolik_oriznout_z_vyberu, y + delsi_polovina_strany_rel + kolik_oriznout_z_vyberu

    x_start_rel_orig, y_start_rel_orig = x - kratsi_polovina_strany_rel, y - kratsi_polovina_strany_rel
    x_end_rel_orig, y_end_rel_orig = x + delsi_polovina_strany_rel, y + delsi_polovina_strany_rel

    if pocet_zpracovanych_kloubu < 4:
        barva_obdelniku = (0.0, 165.0, 255.0) # oranzova
    elif pocet_zpracovanych_kloubu < 8:
        barva_obdelniku = (0.0, 165.0, 70.0) # zelena
    elif pocet_zpracovanych_kloubu < 12:
        barva_obdelniku = (230.0, 150.0, 0.0) # modra
    elif pocet_zpracovanych_kloubu == 12:
        barva_obdelniku = (150.0, 0.0, 150.0) # fialova

    # barevne zvyrazneni vnitrku vyberu
    # cv2.rectangle(obrazek_ke_zobrazeni, (x_start, y_start), (x_end, y_end), (0.0, 165.0, 255.0), -1)    # absolutni rozmery
    cv2.rectangle(obrazek_ke_zobrazeni, (x_start_rel, y_start_rel), (x_end_rel, y_end_rel), barva_obdelniku, -1)
    # pridani polopruhledneho vyberu k puvodnimu obrazku
    mira_pruhlednosti = 0.75
    obrazek_ke_zobrazeni = cv2.addWeighted(obrazek_ke_zobrazeni, 1 - mira_pruhlednosti, snimek_puvodni, mira_pruhlednosti, 0)
    # ohraniceni vyberu s absolutnim rozmerem
    cv2.rectangle(obrazek_ke_zobrazeni, (x_start, y_start), (x_end, y_end), (150.0, 150.0, 150.0), 2)
    # ohraniceni vyberu s relativnim rozmerem
    cv2.rectangle(obrazek_ke_zobrazeni, (x_start_rel, y_start_rel), (x_end_rel, y_end_rel), barva_obdelniku, 2)
    cv2.rectangle(obrazek_ke_zobrazeni, (x_start_rel_orig, y_start_rel_orig), (x_end_rel_orig, y_end_rel_orig), (150.0, 150.0, 150.0), 2)
    # zobrazeni obrazku se zvyraznenym vyberem
    cv2.imshow("Tvorba vyrezu kloubu", obrazek_ke_zobrazeni)


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
def ulozitVystupniSnimky(nazev_snimku, nazev_snimku_vcetne_cesty_k_nemu, oznaceni_kloubu, snimek_k_ulozeni, snimek_k_ulozeni2):
    # oriznuti pripony z nazvu souboru
    nazevSnimkuBezPripony = os.path.splitext(nazev_snimku)[0]
    # vyjmuti samotne pripony
    # PouzePripona = os.path.splitext(nazev_snimku)[1]
    PouzePripona = ".png"

    cestaDoSlozkySeSnimkem = os.path.dirname(nazev_snimku_vcetne_cesty_k_nemu) + "/"  # ziskani cesty do slozky se snimkem

    # pokud se cesta ke snimku rovna ceste ke vstupni slozce (tzn. snimek uz neni dale zanoreny do podslozek)
    if cestaDoSlozkySeSnimkem == INPUT_IMAGES_DIR:
        # jenom zpracovat snimek BEZ zpracovani jmena podslozky

        nazevVystupnihoSnimku = OUTPUT_DIR + nazevSnimkuBezPripony + "_" + oznaceni_kloubu + PouzePripona
        zapsatVystupniSnimekNaDisk(nazevVystupnihoSnimku, snimek_k_ulozeni)

        nazevVystupnihoSnimku2 = OUTPUT_DIR_REL + nazevSnimkuBezPripony + "_" + oznaceni_kloubu + "_relativni_velikost_" + PouzePripona
        zapsatVystupniSnimekNaDisk(nazevVystupnihoSnimku2, snimek_k_ulozeni2)

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

        cilovaSlozkaVcetnePodslozky_rel = OUTPUT_DIR_REL + "/" + nazevPodslozkySeSnimky + "/"
        if not os.path.exists(cilovaSlozkaVcetnePodslozky_rel):
            os.makedirs(cilovaSlozkaVcetnePodslozky_rel)

        nazevVystupnihoSnimku = cilovaSlozkaVcetnePodslozky + nazevSnimkuBezPripony + "_" + oznaceni_kloubu + PouzePripona
        zapsatVystupniSnimekNaDisk(nazevVystupnihoSnimku, snimek_k_ulozeni)

        nazevVystupnihoSnimku2 = cilovaSlozkaVcetnePodslozky_rel + nazevSnimkuBezPripony + "_" + oznaceni_kloubu + "_relativni_velikost_" + PouzePripona
        zapsatVystupniSnimekNaDisk(nazevVystupnihoSnimku2, snimek_k_ulozeni2)
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
