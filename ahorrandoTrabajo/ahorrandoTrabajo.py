# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2019
@author: Gonzalo Bueno Santana
Programa pensado para extraer datos de plataformas de alquiler usando diferentes navegadores : Google Chrome, Mozilla Firefox, Microsoft Edge y Opera
De momento el programa extrae los datos desde dos webs:fotocasa y idealista.
He restringido el uso de selenium a Firefox puesto que es el que menos fallos me da a la hora de migrar el proyecto.
'''
import time
import threading
import socket
from pathlib import Path
import sys
import os

import Dumbledore
import jackSparrow
import Erebor

#Variables globales
################################################################################################################
#Consigo algunos parámetros para mostrar, calcular el tiempo que tarda el programa en funcionar y demás.
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
start_time = time.time()
home = str(Path.home())
rutaGuardado = os.path.dirname(os.path.realpath(__file__))# r"C:\selenium"
################################################################################################################
nombreArchivo = ""
url_text = ""

def saveConfig():
    print("La ruta donde se guardará la carpeta de la extracción será : ",rutaGuardado)
    print("Ahora establezca el nombre de esta carpeta en la que se guardarán los datos : ")
    nombreArchivo =input()
    directorio = rutaGuardado + "\Extraccion_" + nombreArchivo
    try:
      os.stat(directorio)
    except:
      os.mkdir(directorio)
    print("Los datos se guardarán en ", directorio)

################################################################################################################
print('Iniciando...')
#mainCode
#print("IP local del dispositivo : ",host_ip)
if len(sys.argv) == 2:
    url_text = sys.argv[1]
    saveConfig()
elif len(sys.argv) == 3:
    url_text = sys.argv[1]
    nombreArchivo = sys.argv[2]
elif len(sys.argv) < 2:
    while(url_text.find("www.idealista") == -1 and url_text.find("www.fotocasa") == -1 and url_text.find("www.pisos") == -1):
        url_text = input("Introduzca la url de IDEALISTA, FOTOCASA o PISOS para realizar la extracción : \n")
        if(url_text.find("www.idealista") == -1 and url_text.find("www.fotocasa") == -1 and url_text.find("www.pisos") == -1):
            print("Link no valido, prueba otra vez")
    saveConfig()
if(url_text.find("www.fotocasa") != -1):
    print("Iniciando extracción de datos para fotocasa.com")
    FirefoxThread = threading.Thread(target=Dumbledore.extractLinksFotocasa(url_text, start_time, rutaGuardado, nombreArchivo))
elif(url_text.find("www.idealista") != -1):
    print("Iniciando extracción de datos para idealista.com")
    FirefoxThread = threading.Thread(target=jackSparrow.extractLinksIdealista(url_text, start_time, rutaGuardado, nombreArchivo))
elif(url_text.find("www.pisos") != -1):
    print("Iniciando extracción de datos para pisos.com")
    FirefoxThread = threading.Thread(target=Erebor.extractLinksPisos(url_text, start_time, rutaGuardado, nombreArchivo))
FirefoxThread.start()
FirefoxThread.join()
print('Fin del programa principal.')
################################################################################################################
