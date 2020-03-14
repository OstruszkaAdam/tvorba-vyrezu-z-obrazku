import os
import shutil
import cv2
import numpy as np
import uuid
from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter

# https://gist.github.com/erniejunior/601cdf56d2b424757de5

INPUT_DIR = r"C:\Users\Adam\Desktop\smazat"

output_dir_name = "elasticky_deformovane"
OUTPUT_DIR = os.path.join(INPUT_DIR, output_dir_name)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


#######################################################################################################################
def main():
    count_of_processed_files = 0

    # Walk through all files in the directory that contains the files to copy
    for subdir, dirs, files in os.walk(INPUT_DIR):
        for filename in files:

            # if the file does not end in .jpg or .jpeg (case-insensitive) or other formats, continue with the next iteration of the for loop
            if not (filename.lower().endswith(".jpg") or
                    filename.lower().endswith(".jpeg") or
                    filename.lower().endswith(".png") or
                    filename.lower().endswith(".tif") or
                    filename.lower().endswith(".tiff")):
                continue
            # end if

            old_name_and_path = os.path.join(os.path.abspath(subdir), filename)
            print(old_name_and_path)
            base, extension = os.path.splitext(filename)  # Separate base from extension
            new_filename = "ctverec_" + base + extension
            # new_filename = "ctverec_" + base + str(uuid.uuid1()) + extension

            new_name_and_path = os.path.join(OUTPUT_DIR, new_filename)
            # print(new_name_and_path)

            snimek_puvodni = cv2.imread(old_name_and_path)
            vyska_obrazku = np.size(snimek_puvodni, 0)
            sirka_obrazku = np.size(snimek_puvodni, 1)
            print("rozmery jsou " + str(sirka_obrazku) + " x " + str(vyska_obrazku))

            snimek_upraveny = elastic_transform(snimek_puvodni, 500, 8)


            zapsatVystupniSnimekNaDisk(new_name_and_path, snimek_upraveny)

            # Increment and show count of all copied files
            count_of_processed_files += 1
            print("Pocet zpracovanych souboru = " + str(count_of_processed_files))
            print()

        # end for
    # end for


# end main


#######################################################################################################################
def zapsatVystupniSnimekNaDisk(nazevVystupnihoSnimkuVcetneCestyKNemu, snimekKteryMaBytUlozen):
    cv2.imwrite(nazevVystupnihoSnimkuVcetneCestyKNemu, snimekKteryMaBytUlozen)
    print("uklada se soubor " + nazevVystupnihoSnimkuVcetneCestyKNemu)
    print("")  # odradkovani


# end function


#######################################################################################################################
def elastic_transform(image, alpha, sigma):
    """Elastic deformation of images as described in [Simard2003]_.
    .. [Simard2003] Simard, Steinkraus and Platt, "Best Practices for
       Convolutional Neural Networks applied to Visual Document Analysis", in
       Proc. of the International Conference on Document Analysis and
       Recognition, 2003.
    """
    random_state = np.random.RandomState(None)

    shape = image.shape
    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dz = np.zeros_like(dx)

    x, y, z = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), np.arange(shape[2]))
    print(x.shape)
    indices = np.reshape(y+dy, (-1, 1)), np.reshape(x+dx, (-1, 1)), np.reshape(z, (-1, 1))

    distored_image = map_coordinates(image, indices, order=1, mode='reflect')
    return distored_image.reshape(image.shape)

# end function

#######################################################################################################################
if __name__ == "__main__":
    main()
