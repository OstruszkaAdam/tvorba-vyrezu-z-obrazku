import numpy as np
import cv2
from cv2 import imwrite
import os

# module-level variables ##############################################################################################
INPUT_IMAGES_DIR = os.getcwd() + ""
OUTPUT_DIR = os.getcwd() + "/smazat/"

cropping = False

# rozrezani obrazku na podobrazky #####################################################################################
def vyriznout_z_obrazku_ctverec(event, x, y, flags, param):
    pocet_zpracovanych_prstu = 0
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping

    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start = x - 50, y - 50
        x_end, y_end = x + 50, y + 50
        cropping = True

    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False  # cropping is finished
        pocet_zpracovanych_prstu += 1
        print(pocet_zpracovanych_prstu)

        ref_point = [(x_start, y_start), (x_end, y_end)]

        roi = oriImage[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
        cropped_image_name = "Cropped image " + str(pocet_zpracovanych_prstu) + ".jpg"
        cv2.imshow("Cropped image", roi)
        imwrite(cropped_image_name, roi)
# end function

#######################################################################################################################
def main():
    x_start, y_start, x_end, y_end = 0, 0, 0, 0


    for fileName in os.listdir(INPUT_IMAGES_DIR):
        # if the file does not end in .jpg or .jpeg (case-insensitive), continue with the next iteration of the for loop
        if not (fileName.lower().endswith(".jpg") or fileName.lower().endswith(".jpeg")):
            continue
        # end if

        # oriznuti pripony z nazvu souboru
        fileNameWithoutExtension = os.path.splitext(fileName)[0]

        # vyjmuti samotne pripony
        JustExtension = os.path.splitext(fileName)[1]

        # show the file name on std out
        print("zpracovava se soubor " + fileName)

        # get the file name and full path of the current image file
        imageFileWithPath = os.path.join(INPUT_IMAGES_DIR, fileName)
        # attempt to open the image with OpenCV
        snimek_puvodni = cv2.imread(imageFileWithPath)

        # if we were not able to successfully open the image, continue with the next iteration of the for loop
        if snimek_puvodni is None:
            print("unable to open " + fileName + " as an OpenCV image")
            continue
        # end if


    oriImage = snimek_puvodni.copy()

    zpracovat_obrazek(oriImage)

    while True:

        i = snimek_puvodni.copy()

        if not cropping:
            cv2.imshow("image", snimek_puvodni)

        elif cropping:
            cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (0.0, 165.0, 255.0), 3)
            cv2.imshow("image", i)

        cv2.waitKey(1)

    # close all open windows
    cv2.destroyAllWindows()

    # end for

# end function

#######################################################################################################################
def zpracovat_obrazek(oriImage):
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", vyriznout_z_obrazku_ctverec)

# end function

#######################################################################################################################
if __name__ == "__main__":
    main()



