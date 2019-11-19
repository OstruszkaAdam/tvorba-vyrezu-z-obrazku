import cv2
from cv2 import imwrite
from random import seed
from random import random


# module-level variables ##############################################################################################
cropping = False

x_start, y_start, x_end, y_end = 0, 0, 0, 0

input_image = cv2.imread('01_ruka_leva.jpg')
oriImage = input_image.copy()

pocet_zpracovanych_kloubu = 0

#######################################################################################################################
def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global pocet_zpracovanych_kloubu
    global x_start, y_start, x_end, y_end, cropping

    if event == cv2.EVENT_MOUSEMOVE:
        x_start, y_start = x - 70, y - 70
        x_end, y_end = x + 70, y + 70

    # (x, y) coordinates and indicate that cropping is being
    elif event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start = x - 70, y - 70
        x_end, y_end = x + 70, y + 70
        cropping = True

    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        cropping = False  # cropping is finished
        pocet_zpracovanych_kloubu += 1
        print(pocet_zpracovanych_kloubu)

        ref_point = [(x_start, y_start), (x_end, y_end)]

        roi = oriImage[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]]
        cropped_image_name = "Cropped image " + str(pocet_zpracovanych_kloubu) + ".jpg"
        cv2.imshow("Cropped image", roi)
        imwrite(cropped_image_name, roi)
# end mouse_crop


#######################################################################################################################
cv2.namedWindow("image")
cv2.setMouseCallback("image", mouse_crop)

while True:

    obrazek_ke_zobrazeni = input_image.copy()

    if not cropping:
        # ohraniceni vyrezu
        cv2.rectangle(obrazek_ke_zobrazeni, (x_start, y_start), (x_end, y_end), (0.0, 165.0, 255.0), 2)
        # barevne zvyrazneni vnitrku vyrezu
        cv2.rectangle(obrazek_ke_zobrazeni, (x_start, y_start), (x_end, y_end), (0.0, 165.0, 255.0), -1)
        alpha = 0.4  # Transparency factor.
        # Following line overlays transparent rectangle over the image
        obrazek_se_zvyraznenim = cv2.addWeighted(obrazek_ke_zobrazeni, alpha, input_image, 1 - alpha, 0)
        cv2.imshow("image", obrazek_se_zvyraznenim)

    elif cropping:

        cv2.imshow("image", obrazek_ke_zobrazeni)

    cv2.waitKey(1)

# close all open windows
cv2.destroyAllWindows()
