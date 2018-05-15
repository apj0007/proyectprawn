# -*- coding: utf-8 -*-
"""TratamientoSkeleton.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UmS7W-fvGkWMP3hreWeE39CwpDBv_xMt
"""

import cv2

from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data,io,color,util
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.color import label2rgb,rgb2lab
from skimage.feature import canny
from skimage.util import invert
from skimage.morphology import closing, opening, erosion, dilation, square, skeletonize,skeletonize_3d
from skimage.io import imread, imshow
from skimage.transform import (hough_line, hough_line_peaks,probabilistic_hough_line)


from scipy import ndimage
from scipy.spatial import distance

import numpy as np
from PIL import Image

import math

class TratamientoSkeleton():
  
  @classmethod
  def detectar_ojo(self,frame):  
    img_gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #Convertir a HSV

    #array con las posiciones min - max
    lower=np.array([0,0,0])
    upper=np.array([255,255,170])

    #Deteccion de colores
    mask = cv2.inRange(hsv, lower, upper)

    #Erosion de la imagen
    kernel = np.ones((6,6),np.uint8) 
    Erosion = cv2.erode(mask,kernel,iterations = 1)
    
    return Erosion
  
  @classmethod

    def detectar_region(self,im,imgBN,k=False):
        centro_region=[]
        area_total=0
    
    # crea una figura con dos subfiguras
        fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(16, 16))
    
    # hace las etiquetas de los ejes invisibles
        ax[0].yaxis.set_visible(False)
        ax[0].xaxis.set_visible(False)
    
        ax[1].yaxis.set_visible(False)
        ax[1].xaxis.set_visible(False)
    
    # en la primera subfigura está la imagen original
        ax[0].imshow(im)
    
    # en la segunda subfigura está la imagen en blanco y negro con las regiones encontradas
    a   x[1].imshow(imgBN, cmap=plt.cm.gray)
    
    
    # label es la primera función clave, toma una imagen en blanco y negro
    # y devuelve sus componentes conexas
        label_image = label(imgBN)

        for region in regionprops(label_image):  
            area_total=area_total+region.area

        # draw rectangle around segmented regions
            minr, minc, maxr, maxc = region.bbox
            centro_region.append([(minr+(maxr-minr)/2),(minc+(maxc-minc)/2)])
        # draw rectangle around segmented regions
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                    fill=False, edgecolor='red', linewidth=1)
            ax[1].add_patch(rect)

        plt.tight_layout()
        plt.show()

        return centro_region,area_total
