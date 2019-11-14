import numpy as np
import cv2
import os

# module-level variables ##############################################################################################
INPUT_IMAGES_DIR = os.getcwd() + "/vstupy/"
OUTPUT_DIR = os.getcwd() + "/vystupy/"


#######################################################################################################################
def main():
    for subdir, dirs, files in os.walk(INPUT_IMAGES_DIR):
        for nazevSnimku in files:

            # preskoceni souboru, ktery neni snimek ###################################################################
            # if the file does not end in .jpg or .jpeg (case-insensitive), continue with the next iteration of the for loop
            if not (nazevSnimku.lower().endswith(".jpg") or nazevSnimku.lower().endswith(".jpeg")):
                continue
            # end if

            # otevrit a zpracovat snimek ##############################################################################
            nazevSnimkuVcetneCestyKNemu = os.path.join(subdir, nazevSnimku)
            print("zpracovava se soubor " + nazevSnimkuVcetneCestyKNemu)

            snimek_puvodni = cv2.imread(nazevSnimkuVcetneCestyKNemu)
            # if we were not able to successfully open the image, continue with the next iteration of the for loop
            if snimek_puvodni is None:
                print("unable to open " + nazevSnimku + " as an OpenCV image")
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
            cv2.resizeWindow('Snimek ke zpracovani', sirka_okna,
                             vyska_okna)  # resize the window according to the screen resolution
            cv2.imshow("Snimek ke zpracovani", snimek_puvodni)
            cv2.waitKey(0)  # 0 = program ceka, dokud nestisknu libovolnou klavesu

            cv2.destroyWindow("Snimek ke zpracovani")
            # cv2.destroyAllWindows()

            # zpracovat snimek #########################################################################################
            jakeRuceJsouNaSnimku = "obe"

            if jakeRuceJsouNaSnimku == "obe":
                vyska = np.size(snimek_puvodni, 0)
                sirka = np.size(snimek_puvodni, 1)
                sirka_k_oriznuti = round(sirka / 2)
                # print (vyska)
                # print (sirka)
                # print (sirka_k_oriznuti)

                #                                       vyska          sirka
                snimek_orezany_levy = snimek_puvodni[0:vyska, 0:sirka_k_oriznuti]
                jakeRuceJsouNaSnimku = "leva"
                ulozitVystupniSnimek(nazevSnimku, nazevSnimkuVcetneCestyKNemu, jakeRuceJsouNaSnimku, snimek_orezany_levy)

                snimek_orezany_pravy = snimek_puvodni[0:vyska, sirka_k_oriznuti:sirka]
                jakeRuceJsouNaSnimku = "prava"
                ulozitVystupniSnimek(nazevSnimku, nazevSnimkuVcetneCestyKNemu, jakeRuceJsouNaSnimku, snimek_orezany_pravy)
            else:
                jakeRuceJsouNaSnimku = ""
                ulozitVystupniSnimek(nazevSnimku, nazevSnimkuVcetneCestyKNemu, jakeRuceJsouNaSnimku, snimek_puvodni)

            # endif

        # end for
    # end for


# end main

#######################################################################################################################
def ulozitVystupniSnimek(fileName, nazevSnimkuVcetneCestyKNemu, jakeRuceJsouNaSnimku, snimek_puvodni):
    # oriznuti pripony z nazvu souboru
    nazevSnimkuBezPripony = os.path.splitext(fileName)[0]
    # vyjmuti samotne pripony
    PouzePripona = os.path.splitext(fileName)[1]

    cestaDoSlozkySeSnimkem = os.path.dirname(nazevSnimkuVcetneCestyKNemu) + "/"  # ziskani cesty do slozky se snimkem

    # pokud se cesta ke snimku rovna ceste ke vstupni slozce (tzn. snimek uz neni dale zanoreny do podslozek)
    if cestaDoSlozkySeSnimkem == INPUT_IMAGES_DIR:
        # jenom zpracovat snimek BEZ zpracovani jmena podslozky

        nazevVystupnihoSnimku = OUTPUT_DIR + nazevSnimkuBezPripony + "_" + jakeRuceJsouNaSnimku + PouzePripona
        zapsatVystupniSnimekNaDisk(nazevVystupnihoSnimku, snimek_puvodni)

    # pokud snimek je dale zanoreny do podslozek
    else:
        # zpracovat snimek a zpracovat i jmeno podslozky (tzn. vytvorit ji v cilovem umisteni)

        # ziskani nazvu podslozky, ve ktere je snimek umisteny
        cestaDoSlozkySeSnimkem = os.path.dirname(nazevSnimkuVcetneCestyKNemu)  # ziskani cesty do slozky se snimkem
        nazevPodslozkySeSnimky = os.path.split(cestaDoSlozkySeSnimkem)[1]  # ziskani nazvu pouze posledni slozky

        # vytvoreni podlozky v cilove slozky (pokud jeste neexistuje)
        cilovaSlozkaVcetnePodslozky = OUTPUT_DIR + "/" + nazevPodslozkySeSnimky + "/"
        if not os.path.exists(cilovaSlozkaVcetnePodslozky):
            os.makedirs(cilovaSlozkaVcetnePodslozky)

        nazevVystupnihoSnimku = cilovaSlozkaVcetnePodslozky + nazevSnimkuBezPripony + "_" + jakeRuceJsouNaSnimku + PouzePripona
        zapsatVystupniSnimekNaDisk(nazevVystupnihoSnimku, snimek_puvodni)
    # end if


# end function


#######################################################################################################################
def zapsatVystupniSnimekNaDisk(nazevVystupnihoSnimkuVcetneCestyKNemu, snimekKteryMaBytUlozen):
    cv2.imwrite(nazevVystupnihoSnimkuVcetneCestyKNemu, snimekKteryMaBytUlozen)


# end function

#######################################################################################################################
if __name__ == "__main__":
    main()
