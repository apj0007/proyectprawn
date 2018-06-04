# -*- coding: utf-8 -*-
"""CuencaHidrografica.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UmS7W-fvGkWMP3hreWeE39CwpDBv_xMt
"""

# % matplotlib inline
import matplotlib.pyplot as plt
from google.colab import files
import os
from skimage.measure import label, regionprops
import itertools
import numpy as np
from heapq import merge

from skimage import io,color,util
from skimage.transform import rescale
from skimage.color import rgb2lab,rgb2gray
from skimage.filters import threshold_otsu, threshold_local,sobel
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed, mark_boundaries
from skimage.util import img_as_float

from PrawnView.proyecto.src.ProcesadoImagen.LeeImagen import LeeImagen
from PrawnView.proyecto.src.ProcesadoImagen.TratamientoDeImagen import TratamientoDeImagen
from PrawnView.proyecto.src.ProcesadoImagen.ProcesadorImagenAutomatico import ProcesadorImagenAutomatico
#from PrawnView.proyecto.FachadaCaracterísticas import FachadaCaracterísticas

class CuencaHidrografica():
    """
    Clase fachada para el mediador que se encargara de la entrada salida por ficheros.
    @var mediador: Instancia del mediador de pestañas que crea dicha fachada.
    @var escribecsv: Instancia de la clase que pasa a csv los datos o los lee de dicho fichero.
    @var dic: Diccionario de datos donde estalocalizado los string del codigo.
    @var configuraciontoxml: Instancia de la clase que lee y escribe los xml.
    @var estad: Instancia de la clase que se encarga de lasestadisticas.   
    """

    def __init__(self):
      self.pr_ProcesadorImagenAutomatico=ProcesadorImagenAutomatico()
      self.pr_LeeImagen=LeeImagen()
      self.pr_TratamientoDeImagen=TratamientoDeImagen()
        
    @classmethod        
    def cuencaAutomatica(self,path):
      self.pr_LeeImagen=LeeImagen()
      self.pr_TratamientoDeImagen=TratamientoDeImagen        
        
        
      img=self.pr_LeeImagen.leer_imagen(path)
      img=self.reducirImagen(img)
      gray=self.pr_TratamientoDeImagen.escala_grises3(img,[ 247,211,114])
      binary=self.pr_TratamientoDeImagen.binarizar(gray)
      inbin=self.pr_TratamientoDeImagen.invertirbinarizar1(binary)
      img,segmentos=self.cuenca(img,binary)
      segmentos_validos=self.descartarVacios(segmentos,binary)
      #areaRatio=self.descartarNoValidos(segmentos,segmentos_validos,path)
      combinaciones=self.combinarSegmentos(segmentos_validos)
      combinaciones_buenas=self.encontratCombinacionesBuenas(img,combinaciones,segmentos)

      return combinaciones_buenas,areaRatio

    @classmethod
    def reducirImagen(self,img1):
      img1 = rescale(img1, 0.25)
      img1.shape
      return img1
                

    @classmethod            
    def cuenca(self,img1,binary):
      img = img_as_float(img1)

      '''
      Aplico el watershed.
      Toma como argumentos la imagen de gradiente (detector de bordes de sobel)
      el numero de markers (semillas) a más markers más zonas se van a crear, 
      si el número es muy grande alguna zona estará vacia
      compactness: bajo-> regiones irregulares pero uniformes en los valores de sus pixels
      compactness: alto-> regiones cuadradas pero no tan uniformes en sus valores
      Usaremos por lo tanto uno bajo

      Para que funcione mejor hay que pasarle una mascara, que separe los langostinos del resto

      '''

      # Con la imagen de 6 langostinos me hacen falta más markers, sino se escapa alguno
      # para las otras imagenes con 9 markers lo hace ok
      gradient = sobel(rgb2gray(img))
      segments_watershed = watershed(gradient,markers=9,compactness=0.0001,mask=binary)

      '''
      Los segmentos son las zonas o regiones en las que ha separado la imagen
      mark_boundaries pone una linea amarilla separando las regiones
      '''
      segmentos = segments_watershed

      #fig, ax = plt.subplots()
      #ax.imshow(mark_boundaries(img, segments_fz))

      #fig, ax = plt.subplots()
      #ax.imshow(mark_boundaries(img, segments_watershed))        
      print("Número de segmentos: {}".format(len(np.unique(segments_watershed))))
                
      return img,segmentos
                
    @classmethod
    def descartarVacios(self,segmentos,binary):
      '''
      En cada ejecución puede haber segmentos vacios, o segmentos de más que lo que contengan sean
      regiones del fondo en vez de trozos de langostinos.

      Voy a recorrer todos los segmentos y usando su solape con la máscara sabré si es un segmento
      que contiene langostino o es un segmento que contiene fondo.

      Descarto los vacios o los que son regiones del fondo

      '''


      num_segmentos = len(np.unique(segmentos))
      fig, ax = plt.subplots(nrows=num_segmentos, ncols=2, figsize=(20, 20))

      segmentos_validos = []

      for i in range(num_segmentos):

          # saco tamaño del segmento y tamaño de la intersección con la mascara
          size_segment = (segmentos==i).sum()
          size_interseccion = ((segmentos==i) & binary).sum()

          if size_segment>0:    
              ax[i][0].imshow(segmentos==i)
              ax[i][1].imshow((segmentos==i) & binary)
              print(size_interseccion,size_segment,size_interseccion/size_segment)
              if size_interseccion/size_segment>0.8: # el numero depende del numero de segmentos
                  segmentos_validos.append(i)
    
      return segmentos_validos              

  
    @classmethod
    def descartarNoValidos(self,segmentos,segmentos_validos,path):
      areaRatio=set()
      ar=set()
      '''
      Aquí muestro solo los válidos

      Habría que sacar los validos de un gran conjunto de imágenes
      - obtener sus atributos: area, presencia_ojo, area_ratio (y el resto de características que podamos)
      - darles una clase manualmente: cola, gamba, gamba con melanosis, otro (fragmentos rotos, etc)

      Tendríamos pues un dataset asi:

      100,True,1,Gamba
      50,False,1,Cola
      100,True,20,Melanosis
      40,False,20,Otro

      Entrenaríamos un clasificador con esos datos

      '''

      fig, ax = plt.subplots(nrows=len(segmentos_validos), ncols=1, figsize=(10, 10))

      for i in range(len(segmentos_validos)):
          ax[i].imshow(segmentos==segmentos_validos[i])
          self.pr_ProcesadorImagenAutomatico=ProcesadorImagenAutomatico()
          areag,aream=ProcesadorImagenAutomatico.ProcesadorAutomatico(path,segmentos==segmentos_validos[i])
          ar=aream/areag
          #ar=FachadaCaracterísticas.ratio(path,segmentos==segmentos_validos[i])
          areaRatio.add(ar)
      return areaRatio
    @classmethod
    def combinarSegmentos(self,segmentos_validos):
      '''
      Aquí se podría hacer la poda, para que no hubiese tantas alternativas invalidas, lo dejo a tu elección

      Otra idea es hacer hacer combinaciones válidas entre los segmentos
      idea, si junto dos segmentos y me queda un objeto es unión valida

      El ejemplo lo hago con dos fragmentos, pero igual habría que hacer combinaciones de 1, de 2 y de 3
      '''

      comb=set()
      combinaciones1=set()
      if(len(segmentos_validos)==2):
        for j in range(len(segmentos_validos)):
          x=(segmentos_validos[j],segmentos_validos[j])
          combinaciones1.add(x)
          combinaciones2 = list(itertools.combinations(segmentos_validos, 2))
          comb=list(merge(combinaciones1,combinaciones2))
      elif(len(segmentos_validos)>2):
        combinaciones2 = list(itertools.combinations(segmentos_validos, 2))
        combinaciones3 = list(itertools.combinations(segmentos_validos, 3))
        comb=list(merge(combinaciones1,combinaciones2,combinaciones3))
      elif(len(segmentos_validos)==1):
        for j in range(len(segmentos_validos)):
          x=(segmentos_validos[j],segmentos_validos[j])
          combinaciones1.add(x)
          comb=combinaciones
    
      return comb
    
    @classmethod
    def encontratCombinacionesBuenas(self,img,combinaciones,segmentos):
      combinaciones_buenas = []
    
      fig, ax = plt.subplots(nrows=len(combinaciones), ncols=1, figsize=(10, 10))


      '''
      Abajo combinaciones de 2 segmentos que se tocan

      '''


      for i in range(len(combinaciones)):
          print(i)
          composicion = (segmentos==combinaciones[i][0]) | (segmentos==combinaciones[i][1])

          label_img = label(composicion)
          regions = regionprops(label_img)
          if len(regions)==1:
              combinaciones_buenas.append(combinaciones[i])
              combinaciones_buenas
          ax[i].imshow(composicion)

    
        
      fig, ax = plt.subplots(nrows=len(combinaciones_buenas), ncols=2, figsize=(20, 20))


      '''
          De los segmentos combinados saco las características y se lo paso al clasificador
          Que me va a decir cual es las combinaciones es langostino, cola, melanosis u otro

          '''    
      for i in range(len(combinaciones_buenas)):
          composicion = (segmentos==combinaciones_buenas[i][0]) | (segmentos==combinaciones_buenas[i][1])
          ax[i][0].imshow(composicion)
          copia = img.copy()
          copia[np.invert(composicion)]=250    
          ax[i][1].imshow(copia)          
          
      return combinaciones_buenas
    
    
