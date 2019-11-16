import cv2
from cv2 import imwrite
from random import seed
from random import random


# module-level variables ##############################################################################################
cropping = False

x_start, y_start, x_end, y_end = 0, 0, 0, 0

input_image = cv2.imread('vstupy/01test.png')
oriImage = input_image.copy()

pocet_zpracovanych_kloubu = 0

#######################################################################################################################
def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global pocet_zpracovanych_kloubu
    global x_start, y_start, x_end, y_end, cropping

    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_LBUTTONDOWN:
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

    i = input_image.copy()

    if not cropping:
        cv2.imshow("image", input_image)

    elif cropping:
        cv2.rectangle(i, (x_start, y_start), (x_end, y_end), (0.0, 165.0, 255.0), 3)
        cv2.imshow("image", i)

    cv2.waitKey(1)

# close all open windows
cv2.destroyAllWindows()
