# https://www.pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/

# import the necessary packages
import numpy as np
import argparse
import imutils
import cv2
import os

INPUT_DIR = r"C:\Users\Adam\Desktop\zdroj"
OUTPUT_DIR = r"C:\Users\Adam\Desktop\cil"

COUNT_OF_COPIED_FILES = 0

# zpracovani vsech souboru ve slozce ###################################################################################
for nazevSnimku in os.listdir(INPUT_DIR):

    # if the file does not end in .jpg or .jpeg (case-insensitive) or other formats, continue with the next iteration of the for loop
    if not (nazevSnimku.lower().endswith(".jpg") or
            nazevSnimku.lower().endswith(".jpeg") or
            nazevSnimku.lower().endswith(".png") or
            nazevSnimku.lower().endswith(".tif") or
            nazevSnimku.lower().endswith(".tiff")):
        continue
    # end if

    # show the file name on std out
    print("zpracovava se soubor " + nazevSnimku)

    # get the file name and full path of the current image file
    imageFileWithPath = os.path.join(INPUT_DIR, nazevSnimku)
    # attempt to open the image with OpenCV
    snimek_puvodni = cv2.imread(imageFileWithPath)
    gray = cv2.cvtColor(snimek_puvodni, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edged = cv2.Canny(gray, 20, 100)

    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # ensure at least one contour was found
    if len(cnts) > 0:
        # grab the largest contour, then draw a mask for the pill
        c = max(cnts, key=cv2.contourArea)
        mask = np.zeros(gray.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)

        # compute its bounding box of pill, then extract the ROI,
        # and apply the mask
        (x, y, w, h) = cv2.boundingRect(c)
        imageROI = snimek_puvodni[y:y + h, x:x + w]
        maskROI = mask[y:y + h, x:x + w]
        imageROI = cv2.bitwise_and(imageROI, imageROI, mask=maskROI)

        # loop over the rotation angles
        for angle in np.arange(0, 360, 15):
            snimek_otoceny = imutils.rotate(imageROI, angle)
            cv2.imshow("Rotated (Problematic)", snimek_otoceny)
            cv2.waitKey(0)

        # loop over the rotation angles again, this time ensure the
        # entire pill is still within the ROI after rotation
        for angle in np.arange(0, 360, 15):
            snimek_otoceny = imutils.rotate_bound(imageROI, angle)
            cv2.imshow("Rotated (Correct)", snimek_otoceny)
            cv2.waitKey(0)

new_name = "FAKE_OTOCENA_" + nazevSnimku

# Save the file to the new path
new_name = os.path.join(OUTPUT_DIR, new_name)
print(new_name)

cv2.imwrite(new_name, snimek_otoceny)

# end for
