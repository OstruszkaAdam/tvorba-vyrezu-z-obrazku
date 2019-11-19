import cv2

input_image = cv2.imread('01_ruka_leva.jpg')
obrazek_ke_zobrazeni = input_image.copy()

x, y, w, h = 10, 10, 10, 10  # Rectangle parameters
cv2.rectangle(obrazek_ke_zobrazeni, (x, y), (x + w, y + h), (0, 200, 0), -1)  # A filled rectangle

alpha = 0.4  # Transparency factor.

# Following line overlays transparent rectangle over the image
image_new = cv2.addWeighted(obrazek_ke_zobrazeni, alpha, input_image, 1 - alpha, 0)

cv2.imshow("image", image_new)
cv2.waitKey(0)