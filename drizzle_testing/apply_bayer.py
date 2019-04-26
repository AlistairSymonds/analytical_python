import numpy as np
import cv2
import argparse
import os
import glob
import pathlib

def apply_bayer(brg_img: np.ndarray):
    y,x,_ = brg_img.shape
    bayered_img = np.zeros((y,x))
    #simulating RGGB bayer pattern
    #odd rows -> r,g,r,g,r,g,.....
    #even rows -> g,b,g,b,g,b,....
    for i in range(0,y):
        for j in range(0,x):
            if( i & 1):
                if(j & 1):
                    bayered_img[i,j] = brg_img[i, j, 0] # top left, get red
                else:
                    bayered_img[i,j] = brg_img[i, j, 1] # top right, get green
            else:
                if(j & 1):
                    bayered_img[i, j] = brg_img[i, j, 1]  # bottom left, get green
                else:
                    bayered_img[i, j] = brg_img[i, j, 2]  # top right, get blue
    return bayered_img

ap = argparse.ArgumentParser()
ap.add_argument("--dir", "-d", help="path to folder containing images to bayer")
args = ap.parse_args()


for img_file in pathlib.Path('G:\Blender Output').glob('*.tif'):
    img = cv2.imread(str(img_file), cv2.IMREAD_COLOR)
    print("Bayering img: " + str(img_file))
    img_bayer = apply_bayer(img)
    cv2.imwrite(str(img_file)+"_bayered.tiff",img_bayer)