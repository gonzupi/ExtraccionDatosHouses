# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2019
@author: Gonzalo Bueno Santana
Programa pensado para extraer datos de plataformas de alquiler usando diferentes navegadores : Google Chrome, Mozilla Firefox, Microsoft Edge y Opera
De momento el programa extrae los datos desde dos webs:fotocasa y idealista.
He restringido el uso de selenium a Firefox puesto que es el que menos fallos me da a la hora de migrar el proyecto.
'''
#IDEALISTA.COM

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
import shutil
import winsound
import urllib.request
################################################################################################################
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
home = str(Path.home())
debug = True #Esto hace que vayan mostrandose los mensajes por el terminal, cambiar a False si se quiere
waitTimeDefault = 5
waitTimeLong = 100000
sleepTime = 2 # mas rand de 2 segundos
################################################################################################################
def extractLinksIdealista(URLText, startTime, saveDir, dataFileName):
    #INICIO FIREFOX
    #########################################################################################
    prefix = "MF_" #Para saber desde qué hebra ejecuto cada cosa uso siempre el prefijo del navegador antes de mostrar un mensaje
    print(prefix,'Iniciando Firefox')
    caps = DesiredCapabilities().FIREFOX
    caps["pageLoadStrategy"] = "normal"
    if WithProxy==1 :
        driver = webdriver.Firefox(desired_capabilities=caps,  proxy=proxy)
    if WithProxy == 0 :
            driver = webdriver.Firefox(desired_capabilities=caps)#executable_path='/your/path/to/geckodriver'
    wait = WebDriverWait(driver,waitTimeDefault)
    driver.maximize_window()
    ###########################################################################################
    driver.get(URLText)
    sleepRand()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    StringNumObjects = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.listing-title"))).text
    NumObjects = [int(Numero) for Numero in StringNumObjects.split() if Numero.isdigit()]
    print("Hay ", NumObjects[0], " resultados")
    pages = NumObjects[0]/30;
    print("Hay ",pages, " páginas")
    page = 0
    linkActual = 0;
    df = pd.DataFrame(columns = ['Link', 'Título','Precio', 'metros cuadrados','Num habitaciones', 'Piso', 'Referencia del portal','Inmoviliaria', 'Nº fotos','tipo de portada', 'Comentario'])
    while page < pages:
        print("Extrayendo : página ", page, " de ", pages)
        page = page+1
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.item_contains_branding')))
            sleepRand()
        except:
            sleepRand()
            print("ERROR : No encuentro el body")
        try:
                wait.until(EC.presence_of_element_located((By.XPATH,"//article/div[@class='item-info-container']/a")))
                houses = driver.find_elements_by_xpath("//article/div[@class='item-info-container']/a")
        except:
                time.sleep(sleepTime*2)
                try:
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"//article/div[@class='item-info-container']/a")))
                    houses = driver.find_elements_by_xpath("//article/div[@class='item-info-container']/a")
                except:
                    print("ERROR : No encuentro los links...")
        links = []
        links.clear()
        for i in houses:
            try:
                links.append(i.get_attribute('href'))
            except:
                print(prefix , 'EEROR : Link ERROR')
        print("Extraidos ", len(links), " links")
        for x in links:
            print("Extrayendo página ", linkActual, " de un total de ", NumObjects[0])
            printElapsedTieme(startTime)
            linkActual = linkActual+1
            sleepRand()
            driver.get(x)
            #Extraigo los datos
            if(debug==True): print(x)
            v_titleHouse = getTitle(wait)
            if(debug==True): print(v_titleHouse)
            v_priceHouse = getPrice(wait)
            if(debug==True): print(v_priceHouse, " €")
            v_areaHouse = getArea(wait)
            if(debug==True): print(v_areaHouse, " m^2")
            v_NumRooms = getNumRooms(wait)
            if(debug==True): print(v_NumRooms, " habitaciones")
            v_floor = getFloor(wait)
            if(debug==True): print(v_floor)
            v_reference = getReference(wait)
            if(debug==True): print(v_reference)
            v_numPhotos = getNumberOfPhotos(wait)
            if(debug==True): print(v_numPhotos)
            v_seller = getSeller(wait)
            if(debug==True): print(v_seller)
            v_comment = getComment(wait)
            photoName = getPhotography(wait,linkActual )
            photoText = photoName.split(' ')
            if(photoText[1] == "de"): photoText[1]=photoText[2]
            print("Palabra clave de la imagen : ", photoText[1])
            #if(debug==True): print(v_comment)
            #['Link', 'Título','Precio', 'metros cuadrados','Piso', 'Referencia del portal','Inmoviliaria', 'Nº fotos'])
            df.loc[len(df)] = [x,v_titleHouse,v_priceHouse ,v_areaHouse,v_NumRooms, v_floor,v_reference,v_seller, v_numPhotos, photoText[1], v_comment]
        driver.get(URLText)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        sleepRand()
        print("Click en siguiente")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        sleepRand()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        clickNextPage(wait)
        URLText = driver.current_url
    driver.close()
    print("Extraidos ", pages, " links")
    #Datos extraidos
    #############
    print(prefix,'Iniciando : Copia de datos al excel')
    frames = [df]
    df_copy = pd.concat(frames, axis=0, join='outer', ignore_index=True,
              keys=None, levels=None, names=None, verify_integrity=False,
              copy=True)
    df_copy.to_csv(saveDir + "\datos_"+dataFileName+'.csv', encoding='utf-8', index=False)
    print(prefix,'Finalizado : Copia de datos al excel')
    print("Los datos están en ", home, "\Desktop\datos_", dataFileName, ".csv")
    printElapsedTieme(startTime)

def printElapsedTieme(started_time):
    temp = time.time() - started_time
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print('Tiempo transcurrido')
    print('%d:%d:%d' %(hours,minutes,seconds))

def  clickNextPage(wait):
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".icon-arrow-right-after > span"))).click()
    except:
        print("Error haciendo click en siguiente")

def sleepRand():
    timeDelay = sleepTime + random.randrange(0, 3)
    time.sleep(timeDelay)

def getTitle(wait):
    try:
        v_houseTitle = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.main-info__title h1.h2-simulated span.main-info__title-main"))).text
    except :
        try:
            v_houseTitle = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.main-info__title h1.h2-simulated span.main-info__title-main"))).text
        except:
            print('ERROR : Obteniendo el título')
            v_houseTitle = 'ERROR'
    return v_houseTitle

def getPrice(wait):
    try:
        v_housePrice = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.info-data-price span.txt-bold"))).text
    except :
        try:
            v_housePrice = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.info-data-price span.txt-bold"))).text
        except:
            print('ERROR : Obteniendo el precio')
            v_housePrice = 'ERROR'
    return v_housePrice

def getArea(wait):
    try:
        v_houseArea = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='info-features']/span[1]/span"))).text
    except :
        try:
            v_houseArea = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='info-features']/span[1]/span"))).text
        except:
            print('ERROR : Obteniendo el area')
            v_houseArea = 'ERROR'
    return v_houseArea

def getNumRooms(wait):
    try:
        v_numberRooms = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='info-features']/span[2]/span"))).text
    except :
        try:
            v_numberRooms = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='info-features']/span[2]/span"))).text
        except:
            print('ERROR : Obteniendo el número de habitaciones')
            v_numberRooms = 'ERROR'
    return v_numberRooms

def getPhotography(wait, numImage):
    try:
        img =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.main-image_first img")))
        #print("Imagen obtenida")
    except :
        try:
            img =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.main-image_first img")))
            #print("Imagen obtenida")
        except:
            print('ERROR : Obteniendo la imagen')
            img = 'ERROR'
    try:
        src = img.get_attribute('src')
        print("Imagen src : ", src)
        imageName = str(numImage) + "_" + dataFileName + r".jpg"
        print("Nombre del archivo : ",imageName)
        imageCompleteName = saveDir+ "\img_" + imageName
        print("Ruta del archivo :", imageCompleteName)
        print("Nombre del archivo : ",imageName)
        urllib.request.urlretrieve(src,imageCompleteName)
        print("Imagen guardada")
    except :
        print("Error guardando la imagen ")
    try:
        name = img.get_attribute('title')
        print("Nombre de la imagen web: ", name)
    except OSError as err:
        print("OS error: {0}".format(err))
    except ImportError:
        print("NO module found")
    except ValueError:
        print("Could not convert data to an integer.")
    except:
        print("ERROR con el nombre de la imagen")
        name = 'ERROR ERROR'
    return name

def getFloor(wait):
    try:
        v_floor = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='info-features']/span[3]/span"))).text
    except :
        try:
            v_floor = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='info-features']/span[3]/span"))).text
        except:
            print('ERROR : Obteniendo la planta')
            v_floor = 'ERROR'
    return v_floor

def getReference(wait):
    try:
        v_reference = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".txt-ref"))).text
    except :
        try:
            v_reference = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".txt-ref"))).text
        except:
            print('ERROR : Obteniendo la referencia')
            v_reference = 'ERROR'
    return v_reference

def getNumberOfPhotos(wait):
    try:
        v_NumPhotos = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".btn.fa-button.icon-no-pics.with-text > .fa-button-text"))).text
    except :
        try:
            v_NumPhotos = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".btn.fa-button.icon-no-pics.with-text > .fa-button-text"))).text
        except:
            print('ERROR : Obteniendo el numero de fotos')
            v_NumPhotos = 'ERROR'
    return v_NumPhotos

def getSeller(wait):
    try:
        v_seller = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".about-advertiser-name"))).text
    except :
        try:
            v_seller = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".about-advertiser-name"))).text
        except:
            print('ERROR : Obteniendo el vendedor')
            v_seller = 'ERROR'
    return v_seller

def getComment(wait):
    try:
        v_comment = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".comment"))).text
    except :
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
            v_comment = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".comment"))).text
        except:
            print('ERROR : Obteniendo el comentario')
            v_comment = 'ERROR'
    return v_comment
