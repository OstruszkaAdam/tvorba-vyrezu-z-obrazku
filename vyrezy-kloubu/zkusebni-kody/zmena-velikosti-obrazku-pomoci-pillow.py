# Improting Image class from PIL module
from PIL import Image
import numpy as np

# Opens a image in RGB mode
snimek_puvodni = Image.open(r"C:\Users\Adam\Desktop\zdroj\pacos1\lateral.jpg")

# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = snimek_puvodni.size

# Cropped image of above dimension
# (It will not change original image)
newsize = (100, 100)
snimek_prevzorkovany = snimek_puvodni.resize(newsize, Image.ANTIALIAS)
# Shows the image in image viewer
# im1.show()

snimek_prevzorkovany_opencv = np.array(snimek_prevzorkovany)
# Convert RGB to BGR
snimek_prevzorkovany_opencv = snimek_prevzorkovany_opencv[:, :, ::-1].copy()

snimek_prevzorkovany.save(r"C:\Users\Adam\Desktop\cil\pacos1\lateral.jpg")