# -*- coding: utf-8 -*-
"""TratamientoDeImagen.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bsWnvvnI84M1_74kIXj5g5f-CMkVCYVS
"""

import cv2

from scipy import ndimage
from scipy.spatial import distance

import numpy as np
from PIL import Image

import math
import matplotlib.pyplot as plt 

from skimage.util import invert
from skimage.morphology import closing, opening, erosion, dilation
from skimage.morphology import square
from skimage.io import imread, imshow
from skimage.filters import threshold_otsu
from skimage import io,color,util
from skimage.morphology import skeletonize,skeletonize_3d
from skimage.color import rgb2lab

class LeerMostrar():
    """
    Clase que contiene las clases para leer una imagen y mostrarla por pantalla     en grande o en pequeÃ±o.
    
    @author: AndrÃ©s PÃ©rez JuÃ¡rez
    @version: 1.3
    """
    
    @classmethod
    def erosionar(grey): 
      kernel = np.ones((5,5), np.uint8)
      img_erosion = cv2.erode(grey, kernel, iterations=1)
  
      return img_erosion

    @classmethod
    def elimina_ruido(grey):
      greym = ndimage.gaussian_filter(grey, 2)
      return greym
    
    @classmethod
    def escala_grises1(img, mostrar=False):
      img = color.rgb2gray(img)
      img_gris=elimina_ruido(img)
      if mostrar:
        muestra_imagenes([img, img_gris])

      return img_gris
    
    @classmethod
    '''
    Comparar contra colores de fondo
    lo que fuese fondo sería oscuro en la imagen de salida
    '''
    def escala_grises3(img,color, debug=False): 
      imagenLab = rgb2lab(img)
      colorLab = pixelRGB2LAB(color)
      img_gris = abs(imagenLab-color).mean(axis=2)/255
      if debug:
        muestra_imagenes([img, img_gris])

      return img_gris
    
    @classmethod
    def op_morfologicas(binary):
      binary = dilation(binary, square(12))
      binary = opening(binary, square(25))  
      binary = erosion(binary, square(8))

      return binary
    
    #Si se desea imprimir la imagen se debe enviar True
    @classmethod
    def binarizar(gray,mostrar=False):
      thresh = threshold_otsu(gray)
      binary = gray > thresh
      binary=op_morfologicas(binary)
      if mostrar:
        muestra_imagenes([gray, binary],True)
      return binary
    
    @classmethod
    def invertirbinarizar1(binary):
      inbin = util.invert(binary)
      muestra_imagenes([binary,inbin])
      return inbin

    @classmethod
    #Si deseamos enviar la imagen binaria sin invertir se pone binary a True
    def skeleton(data,is_binary=False):
      if is_binary:
        data = invert(data) 
      skeleton3d = skeletonize_3d(data)
      skeleton3d = dilation(skeleton3d, square(3))
      muestra_imagenes([data,skeleton3d])
 
      return skeleton3d