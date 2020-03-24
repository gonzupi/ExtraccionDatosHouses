# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2019
@author: Gonzalo Bueno Santana
Programa pensado para extraer datos de la plataforma YouTube usando diferentes navegadores : Google Chrome, Mozilla Firefox, Microsoft Edge y Opera
El programa extrae informaci�n con sesi�n iniciada y sin la sesi�n iniciada para despu�s compararla
'''
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import threading
from selenium.webdriver.chrome import service
import socket
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.opera import options
import os
from selenium.webdriver.common.proxy import *
from scipy import integrate
from pickle import FALSE
from numpy.matlib import rand
import random
import time
from pathlib import Path
import sys
import pathlib
import urllib
import requests
import shutil
import winsound
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
import urllib.request
#Variables globales
################################################################################################################
#Consigo algunos par�metros para mostrar el nombre del dispositivo, calcular el tiempo que tarda el programa en funcionar y dem�s.
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
start_time = time.time()
frequency = 880  # Set Frequency To 880 Hertz
duration = 2000  # Set Duration To 1000 ms == 1 second

#Cambiar a true y modificar los valores si se va a trabajar con proxy
WithProxy=False # WithProxy = 1;
myProxy = None # "http://149.215.113.110:70"
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'ftpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy':''})

debug = True #Esto hace que vayan mostrandose los mensajes por el terminal, cambiar a False si se quiere más limpio todo.
tiempoEspera = 4
tiempoEsperaInicial = 100000
sleepTime = 3 # mas rand de 2 segundos
home = str(Path.home())
print("Ruta home : ", home)
#rutaGuardado = home + r"\Desktop\foto"
rutaGuardado = r"C:\fotosExtraccion"

##RELLENAR AQUI el enlace y el nombre del fichero
nombreArchivo = "fotocasa"
url_Prueba_Busqueda = "https://www.fotocasa.es/es/comprar/viviendas/marbella/playa-bajadilla-puertos/l?gridType=list&combinedLocationIds=724,1,29,320,551,29069,0,1511,442&latitude=36.507786292242265&latitudeCenter=36.511&longitude=-4.885036297776367&longitudeCenter=-4.8827"
################################################################################################################

#definicion de funciones
################################################################################################################
#Esta es la funci�n principal
def extractLinks(urlSearch):
    #INICIO FIREFOX
    #########################################################################################
    prefix = "MF_" #Para saber desde qu� hebra ejecuto cada cosa uso siempre el prefijo del navegador antes de mostrar un mensaje
