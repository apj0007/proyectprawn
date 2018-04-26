import matplotlib.pyplot as plt 
import math
from skimage.io import imread
from skimage import io
class ImplementacionLecturaMuestraDeImagen():
    """
    Clase que contiene las clases para leer una imagen y mostrarla por pantalla     en grande o en peque�o.
    
    @author: Andr�s P�rez Ju�rez
    @version: 1.3
    """
    
    @classmethod
    def leer_mostrar_imagen(self,file):
        """
        Funci�n que permite leer y mostrar una imagen cargada
        
        @param file: imagen que se desea leer
 
        @return: se deuelve la imagen ya leida en python
        """

        img =imread(file)
        plt.subplot(211)
        io.imshow(img)
        return img

    @classmethod
    def muestra_imagenes(self,imagenes,grandes=False):
        """
        Funci�n que permite mostrar varias im�genes, deben ser mas de 2 y se pueden mostrar en tama�o grande o m�s peque�o

        @param imagenes: Lista con las im�genes que se desea mostrar
        @param grandes: Boolean, que por defecto se encuentra a False, si esta en True mostrar� las imagenes en tama�o grande

        """

        num_images = len(imagenes)
        if num_images<2:
            print("Se debe pasar m�s de una imagen")
            return 0
        if grandes:
            c=round(num_images/2)
            fig, num_images = plt.subplots(nrows=c, ncols=2, figsize=(16, 8), sharex=True, sharey=True)
            ax = num_images.ravel()
            for i in range(len(imagenes)):
                ax[i].imshow(imagenes[i], cmap=plt.cm.gray, interpolation='nearest')
                ax[i].axis('off')

            fig.tight_layout()
            plt.show()

            return
        lado = math.ceil(num_images**0.1)
        tam_image = 7
  
        for i in range(len(imagenes)):
            plt.subplot(lado,lado,i+1)
            io.imshow(imagenes[i],cmap=plt.cm.gray)
  
 
        io.show()
