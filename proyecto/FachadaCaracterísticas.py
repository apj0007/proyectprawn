# -*- coding: utf-8 -*-
"""FachadaCaracterísticas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UmS7W-fvGkWMP3hreWeE39CwpDBv_xMt
"""


from PrawnView.proyecto.src.ProcesadoImagen.LeeImagen import LeeImagen
from PrawnView.proyecto.src.ProcesadoImagen.TratamientoDeImagen import TratamientoDeImagen
from PrawnView.proyecto.src.ProcesadoImagen.ProcesadorImagenAutomatico import ProcesadorImagenAutomatico
from PrawnView.proyecto.src.ProcesadoImagen.TratamientoRegiones import TratamientoRegiones
from PrawnView.proyecto.src.ProcesadoImagen.CuencaHidrografica import CuencaHidrografica

class FachadaCaracterísticas():
    """
    Clase fachada para el mediador que se encargara de la entrada salida por ficheros.
    @var mediador: Instancia del mediador de pestañas que crea dicha fachada.
    @var escribecsv: Instancia de la clase que pasa a csv los datos o los lee de dicho fichero.
    @var dic: Diccionario de datos donde estalocalizado los string del codigo.
    @var configuraciontoxml: Instancia de la clase que lee y escribe los xml.
    @var estad: Instancia de la clase que se encarga de lasestadisticas.   
    """

    def __init__(self):
      """
      Constructor de la clase FachadaEntradaSalida que inicializa y prepara todos
      los objetos que tendremos que usar mas adelante en la clase.
      """
      self.pr_ProcesadorImagenAutomatico=ProcesadorImagenAutomatico()
      self.pr_LeeImagen=LeeImagen()
      self.pr_TratamientoDeImagen=TratamientoDeImagen()
      self.pr_TratamientoRegiones=TratamientoRegiones()
      self.pr_CuencaHidrografica=CuencaHidrografica()
    
    @classmethod
    def devolverBinario(self,path):
      self.pr_LeeImagen=LeeImagen()
      self.pr_TratamientoDeImagen=TratamientoDeImagen()
        
      img=self.pr_LeeImagen.leer_imagen(path)
      gray=self.pr_TratamientoDeImagen.escala_grises(img)
      binary=self.pr_TratamientoDeImagen.binarizar(gray)
    
      return img,gray,binary
    
    
    @classmethod
    def devolverMelanosis(self,img):
      self.pr_TratamientoRegiones=TratamientoRegiones()
    
      mel=self.pr_TratamientoRegiones.detectar_ojo(img)
        
      return mel

    @classmethod
    def devolverSkeleton(self,binary):
      self.pr_TratamientoDeImagen=TratamientoDeImagen()
    
      sk=self.pr_TratamientoDeImagen.skeleton(binary)
        
      return sk


    @classmethod
    def devolverSegmentos(self,image,binary):
      self.pr_CuencaHidrografica=CuencaHidrografica()
      im,seg=CuencaHidrografica.cuenca(image,binary)

      return im,seg
   
    
    @classmethod
    def ratio(self,path,binary):
      self.pr_ProcesadorImagenAutomatico=ProcesadorImagenAutomatico()
    
      areag,aream=ProcesadorImagenAutomatico.ProcesadorAutomatico(path,binary)
        
      ratio=aream/areag
    
      return areag,ratio
