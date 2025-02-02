from urllib import request
import zipfile

#Función que descarga un archivo de internet
class EntradaZip():
  
  @classmethod
  def descargar_zip_url(self,url):
    # Nombre del archivo a partir del URL
    zipname = url[url.rfind("/") + 1:]
    while not zipname:
      zipname = raw_input("No se ha podido obtener el nombre del ""archivo.\nEspecifique uno: ")

    print("Descargando..." ,zipname)

    # Archivo local
    z = open(zipname, "wb")

    # Escribir en un nuevo fichero local los datos obtenidos via HTTP.
    z.write(request.urlopen(url).read())

    # Cerrar ambos
    z.close()

    print ("Descargado correctamente.",zipname)

    print (zipname, zipfile.is_zipfile(zipname))
    self.extraer_zip(zipname)

  @classmethod
  # abre y extrae todos los ficheros en un zip  
  def extraer_zip(self,zipname):
    password = None
    z = zipfile.ZipFile(zipname, "r")
    try:
        z.extractall(pwd=password)
        for file in z.namelist():
          print(z.getinfo(file))
          imshow(file)
    except:
        print('Error')
        pass
    z.close()
