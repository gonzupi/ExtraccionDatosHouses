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
hostName = socket.gethostname()
hostIP = socket.gethostbyname(hostName)
startTime = time.time()
homePath = str(Path.home())
savePath = os.path.dirname(os.path.realpath(__file__))# r"C:\selenium"
dataFileName = ""
URLText = ""
################################################################################################################
#Funciones
def saveConfig():
    print("La ruta donde se guardará la carpeta de la extracción será : ",savePath)
    print("Ahora establezca el nombre de esta carpeta en la que se guardarán los datos : ")
    dataFileName =input()
    saveDir = savePath + "\Extraccion_" + dataFileName
    try:
      os.stat(saveDir)
    except:
        try:  
          os.mkdir(saveDir)
        except:
          print("No he podido crear el directorio, sigo usando ", saveDir)
    print("Los datos se guardarán en ", saveDir)
    return saveDir

################################################################################################################
#mainCode
#Input
print('Iniciando...')
#print("IP local del dispositivo : ",hostIP)
if len(sys.argv) == 2: #python.py + link
    URLText = sys.argv[1]
    savePath=saveConfig()
elif len(sys.argv) == 3: #python.py + link + fileName
    URLText = sys.argv[1]
    savePath = savePath + "\Extraccion_" + sys.argv[2]
    try:
      os.stat(savePath)
    except:
        try:  
          os.mkdir(savePath)
        except:
          print("No he podido crear el directorio, sigo usando ", saveDir)
    dataFileName=sys.argv[2]
elif len(sys.argv) < 2: #python.py, input by keyboard
    while(URLText.find("www.idealista") == -1 and URLText.find("www.fotocasa") == -1 and URLText.find("www.pisos") == -1):
        URLText = input("Introduzca la url de IDEALISTA, FOTOCASA o PISOS para realizar la extracción : \n")
        if(URLText.find("www.idealista") == -1 and URLText.find("www.fotocasa") == -1 and URLText.find("www.pisos") == -1):
            print("Link no valido, prueba otra vez")
    savePath=saveConfig()
################################################################################################################
#Start the browser
if(URLText.find("www.fotocasa") != -1):
    print("Iniciando extracción de datos para fotocasa.com")
    FirefoxThread = threading.Thread(target=Dumbledore.extractLinksFotocasa(URLText, startTime, saveDir, dataFileName))
elif(URLText.find("www.idealista") != -1):
    print("Iniciando extracción de datos para idealista.com")
    FirefoxThread = threading.Thread(target=jackSparrow.extractLinksIdealista(URLText, startTime, saveDir, dataFileName))
elif(URLText.find("www.pisos") != -1):
    print("Iniciando extracción de datos para pisos.com")
    FirefoxThread = threading.Thread(target=Erebor.extractLinksPisos(URLText, startTime, saveDir, dataFileName))
FirefoxThread.start()
FirefoxThread.join()
print('Fin del programa principal.')
################################################################################################################
