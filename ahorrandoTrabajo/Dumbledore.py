# -*- coding: utf-8 -*-
'''
Created on 19 nov. 2019
@author: Gonzalo Bueno Santana
Programa pensado para extraer datos de plataformas de alquiler usando diferentes navegadores : Google Chrome, Mozilla Firefox, Microsoft Edge y Opera
De momento el programa extrae los datos desde dos webs:fotocasa y idealista.
He restringido el uso de selenium a Firefox puesto que es el que menos fallos me da a la hora de migrar el proyecto.
'''
# FOTOCASA.COM

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

#VARIABLES
################################################################################################################
frequency = 880  # Set Frequency To 880 Hertz
duration = 2000  # Set Duration To 1000 ms == 1 second
#Cambiar a true y modificar los valores si se va a trabajar con proxy
withProxy=False # withProxy = 1;
myProxy = None # "http://149.215.113.110:70"
proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'ftpProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy':''})
debug = True #Esto hace que vayan mostrandose los mensajes por el terminal, cambiar a False si se quiere
waitTimeDefault = 5
waitTimeLong = 100000
sleepTime = 2 # mas rand de 2 segundos
################################################################################################################

#Esta es la función de extracción para IDEALISTA
def extractLinksFotocasa(URLText, startTime,saveDir, dataFileName ):
    #INICIO FIREFOX
    #########################################################################################
    prefix = "MF_" #Para saber desde qu� hebra ejecuto cada cosa si uso varios navegadores uso siempre el prefijo del navegador antes de mostrar un mensaje
    print(prefix,'Iniciando Firefox')
    caps = DesiredCapabilities().FIREFOX
    caps["pageLoadStrategy"] = "normal"
    profile = webdriver.FirefoxProfile()
    profile.set_preference('javascript.enabled', True)
    options = webdriver.FirefoxOptions()
    options.add_argument("--enable-javascript")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
    profile.update_preferences()
    if withProxy==1 :
        driver = webdriver.Firefox(desired_capabilities=caps,  proxy=proxy, firefox_profile=profile, options=options)
    if withProxy == 0 :
        driver = webdriver.Firefox(desired_capabilities=caps, firefox_profile=profile, options=options)#executable_path='/your/path/to/geckodriver'
    wait = WebDriverWait(driver,waitTimeDefault)
    waitLong = WebDriverWait(driver,waitTimeLong)
    driver.maximize_window()
    ###########################################################################################
    sleepRand()
    driver.get(URLText)
    waitLong.until(EC.url_contains(URLText))
    sleepRand()
    sleepRand()
    try:
        wait.until(EC.presence_of_element_located((By.XPATH,"//h1[text()='Pardon Our Interruption...']")))
        print("Ey! un capcha!")
        winsound.Beep(frequency, duration)
        waitLong.until(EC.presence_of_element_located((By.CSS_SELECTOR,".sui-AtomButton--primary")))
        print("Capcha pasado, amos q nos vamos")
    except:
        print("No veo capcha...")
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".sui-AtomButton--primary"))).click()
        sleepRand()
    except:
        print("No he podido hacer click en la cookies...")
    sleepRand()
    StringNumObjects = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".re-SearchTitle-count"))).text
    NumObjects = int(StringNumObjects)
    print("Hay ", NumObjects, " resultados")
    pages = NumObjects/31;
    print("Hay ",pages, " paginas aproximadamente...")
    page = 0
    linkActual = 0
    df = pd.DataFrame(columns = ['Link', 'Título','Precio', 'metros cuadrados','Planta','Referencia del portal', 'Inmobiliaria', 'número de fotos','Orientación','Tipo de anuncio', 'Descripción del anuncio'])
    numPthotos = []
    numPthotos.clear()
    exit = NumObjects;
    while exit > 0:
        page = page+1
        print("Extrayendo : pagina ", page, " de ", pages)
        print("Quedan ", exit, " links aún");
        goDownPageLoadingAll(wait)
        try:
                wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='re-Searchresult-itemRow']//div[@class='re-Card-secondary']/a[@class='re-Card-link']")))
                houses = driver.find_elements_by_xpath("//div[@class='re-Searchresult-itemRow']//div[@class='re-Card-secondary']/a[@class='re-Card-link']")
                numPhotograph=driver.find_elements_by_xpath("//div[@class='re-Searchresult-itemRow']/div/div[@class='re-Card-primary']/a/div[@class='re-Card-photosCounter']/span")
                print("Numero de fotos extraidos : ", len(numPhotograph))
        except:
                print("error extrayendo links... intento otra vez")
                time.sleep(sleepTime*2)
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='re-Searchresult-itemRow']//div[@class='re-Card-secondary']/a[@class='re-Card-link']")))
                    houses = driver.find_elements_by_xpath("//div[@class='re-Searchresult-itemRow']//div[@class='re-Card-secondary']/a[@class='re-Card-link']")
                    numPhotograph=driver.find_elements_by_xpath("//div[@class='re-Searchresult-itemRow']/div/div[@class='re-Card-primary']/a/div[@class='re-Card-photosCounter']/span")
                    print("Links extraidos")
                except:
                    print("ERROR : No encuentro los links...")
        allLinks = []
        allLinks.clear()
        for i in houses:
            try:
                allLinks.append(i.get_attribute('href'))
                #print("Extraido el link :", i.get_attribute('href'))
            except:
                print(prefix , 'EEROR : Link ERROR')
        print("Extraidos ", len(allLinks), " links")
        exit=exit-len(allLinks)
        for i in numPhotograph:
            try:
                photosDef = i.text.replace('1/', '')
                numPthotos.append(photosDef)
                print("Extraido el número de fotos :", photosDef)
            except:
                print(prefix , 'EEROR : numFotos ERROR')
        if(len(numPthotos)==0):
            print("Algo raro pasa")
            sleepRand()
            try:
                numPhotograph=driver.find_elements_by_xpath("//div[@class='re-Searchresult-itemRow']/div/div[@class='re-Card-primary']/a/div[@class='re-Card-multimediaCounter']/div[@class='re-Card-photosCounter']/span[last()]")
                for i in numPhotograph:
                    try:
                        photosDef = i.text.replace('1/', '')
                        numPthotos.append(photosDef)
                        print("Extraido el número de fotos :", photosDef)
                    except:
                        printt(prefix , 'EEROR : numFotos ERROR')
            except:
                print("Raro rarísimo con las fotitos de los huevos")
        for link in allLinks:
            print("Extrayendo página ", linkActual, " de un total de ", NumObjects)
            printElapsedTieme(startTime)
            linkActual = linkActual+1
            sleepRand()
            driver.get(link)
            try:
                wait.until(EC.presence_of_element_located((By.XPATH,"//h1[text()='Pardon Our Interruption...']")))
                print("Ey! un capcha!")
                winsound.Beep(frequency, duration)
                waitLong.until(EC.presence_of_element_located((By.CSS_SELECTOR,".sui-AtomButton--primary")))
                print("Capcha pasado, amos q nos vamos")
            except:
                print("No veo capcha...")
            #EXTRAIGO LOS DATOS
            if(debug==True): print(link)
            v_titleHouse = getTitle(wait)
            if(debug==True): print(v_titleHouse)
            v_priceHouse = getPrice(wait)
            if(debug==True): print(v_priceHouse, " €")
            v_areaHouse = getArea(wait)
            if(debug==True): print(v_areaHouse, " m^2")
            v_reference = getReference(wait, driver)
            if(debug==True): print(v_reference)
            v_seller = getSeller(wait, driver)
            if(debug==True): print(v_seller)
            v_orientation = getOrientation(wait)
            if(debug==True): print("Orientación : ",v_orientation)
            try:
                if(debug==True): print('Número de fotos :', numPthotos[linkActual-1])
            except:
                numPthotos.append('ERROR')
            v_houseType = getHouseType(wait, driver)
            if(debug==True): print("Tipo de oferta : ",v_houseType)
            if(v_houseType == 'Piso'):
                v_floor = getFloor(wait)
                if(debug==True): print(v_floor)
            elif(v_houseType == 'Apartamento'):
                v_floor = getFloor(wait)
                if(debug==True): print(v_floor)
            else:
                v_floor = 'No es un piso ni un apartamento'
            getPhotography(wait,linkActual,dataFileName, saveDir)
            v_comment = getComment(wait)
            df.loc[len(df)] = [link,v_titleHouse,v_priceHouse ,v_areaHouse,v_floor, v_reference,v_seller, numPthotos[linkActual-1],v_orientation, v_houseType, v_comment]
        print("Amos a hacer click en siguiente")
        driver.get(URLText)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        sleepRand()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        sleepRand()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        ClickNextPage(wait,waitLong,driver)
        sleepRand()
        try:
            wait.until(EC.presence_of_element_located((By.XPATH,"//h1[text()='Pardon Our Interruption...']")))
            print("Ey! un capcha!")
            winsound.Beep(frequency, duration)
            waitLong.until(EC.presence_of_element_located((By.CSS_SELECTOR,".sui-AtomButton--primary")))
            print("Capcha pasado, amos q nos vamos")
        except:
            print("No veo capcha...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
        URLText = driver.current_url
    driver.close()
    print("Extraidos ", pages, " links")
    #TODOS LOS DATOS EXTRAIDOS
    #################################################################
    print(prefix,'Iniciando : Copia de datos al excel')
    frames = [df]
    df_copy = pd.concat(frames, axis=0, join='outer', ignore_index=True,
              keys=None, levels=None, names=None, verify_integrity=False,
              copy=True)
    df_copy.to_csv(saveDir + "\datos_"+dataFileName+'.csv', encoding='utf-8', index=False)
    print(prefix,'Finalizado : Copia de datos al excel')
    print("Los datos estan en ", saveDir)
    printElapsedTieme(startTime)

def goDownPageLoadingAll(wait):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    sleepRand()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    sleepRand()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    sleepRand()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    sleepRand()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    sleepRand()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    sleepRand()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
    sleepRand()

def sleepRand():
    timeDelay = sleepTime + random.randrange(0, 3)
    time.sleep(timeDelay)

def sleepRandLong():
    timeDelay = sleepTime*25 + random.randrange(0, 5)
    time.sleep(timeDelay)

def ClickNextPage(wait, waitLong, driver):
    try:
        nextButton = wait.until(EC.presence_of_element_located((By.XPATH,"//ul[@class='sui-PaginationBasic-list']/li[last()]/a")))
        driver.get(nextButton.get_attribute('href'))
        print("Click en siguiente exitoso")
    except:
        print("ERROR haciendo click en siguiente")

def printElapsedTieme(started_time):
    temp = time.time() - started_time
    hours = temp//3600
    temp = temp - 3600*hours
    minutes = temp//60
    seconds = temp - 60*minutes
    print('Tiempo transcurrido')
    print('%d:%d:%d' %(hours,minutes,seconds))

def save_image_to_file(image, dirname, suffix):
    with open('{dirname}/img_{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)

############################################
# Estas funciones consiguen cada uno de los atributos de la página.

def getHouseType(wait, driver):
    try:
        v_housetype = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='re-DetailFeaturesList-featureContent']/p[@class='re-DetailFeaturesList-featureLabel' and contains(text(), 'Tipo de inmueble')]/../p[@class='re-DetailFeaturesList-featureValue']"))).text
    except :
        try:
            v_housetype = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='re-DetailFeaturesList-featureContent']/p[@class='re-DetailFeaturesList-featureLabel' and contains(text(), 'Tipo de inmueble')]/../p[@class='re-DetailFeaturesList-featureValue']"))).text
        except:
            print('ERROR : Obteniendo el tipo de oferta')
            v_housetype = 'ERROR'
    return v_housetype

def getFloor(wait):
    try:
        v_floor = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='re-DetailFeaturesList-featureContent']/p[@class='re-DetailFeaturesList-featureLabel' and contains(text(), 'Planta')]/../p[@class='re-DetailFeaturesList-featureValue']"))).text
    except :
        try:
            v_floor = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='re-DetailFeaturesList-featureContent']/p[@class='re-DetailFeaturesList-featureLabel' and contains(text(), 'Planta')]/../p[@class='re-DetailFeaturesList-featureValue']"))).text
        except:
            print('ERROR : Obteniendo la planta')
            v_floor = 'ERROR'
    return v_floor

def getTitle(wait):
    try:
        v_houseTitle = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.re-DetailHeader-propertyTitle"))).text
    except :
        try:
            v_houseTitle = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.re-DetailHeader-propertyTitle"))).text
        except:
            print('ERROR : Obteniendo el título')
            v_houseTitle = 'ERROR'
    return v_houseTitle

def getPrice(wait):
    try:
        v_housePrice = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.re-DetailHeader-price"))).text
    except :
        try:
            v_housePrice = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.re-DetailHeader-price"))).text
        except:
            print('ERROR : Obteniendo el precio')
            v_housePrice = 'ERROR'
    return v_housePrice

def getOrientation(wait):
    try:
        v_orientation = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='re-DetailFeaturesList-featureContent']/p[@class='re-DetailFeaturesList-featureLabel' and contains(text(), 'Orientación')]/../p[@class='re-DetailFeaturesList-featureValue']"))).text
    except :
        try:
            v_orientation = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='re-DetailFeaturesList-featureContent']/p[@class='re-DetailFeaturesList-featureLabel' and contains(text(), 'Orientación')]/../p[@class='re-DetailFeaturesList-featureValue']"))).text
        except:
            print('ERROR : Obteniendo la orientación')
            v_orientation = 'ERROR'
    return v_orientation

def getArea(wait):
    try:
        v_houseArea = wait.until(EC.presence_of_element_located((By.XPATH,"//ul[@class='re-DetailHeader-features']//span[text()=' m²']/span[@class='re-DetailHeader-featuresItemValue']"))).text
    except :
        try:
            v_houseArea = wait.until(EC.presence_of_element_located((By.XPATH,"//ul[@class='re-DetailHeader-features']//span[text()=' m²']/span[@class='re-DetailHeader-featuresItemValue']"))).text
        except:
            print('ERROR : Obteniendo el area')
            v_houseArea = 'ERROR'
    return v_houseArea

def getPhotography(wait, numImage,dataFileName, saveDir):
    try:
        img =  wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='re-DetailSlider']//div/ul/li[1]/div[@class='re-DetailMultimediaImage-container re-DetailMultimediaImage-container--withHorizontalBorder']/img")))
        #print("Imagen obtenida")
    except :
        try:
            img =  wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='re-DetailSlider']//div/ul/li[1]/div[@class='re-DetailMultimediaImage-container re-DetailMultimediaImage-container--withHorizontalBorder']/img")))
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
        print("ERROR guardando la imagen ")
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

def getReference(wait, driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
    sleepRand()
    try:
        v_reference = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.re-ContactDetail-referenceContainer-reference"))).text
    except :
        try:
            v_reference = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.re-ContactDetail-referenceContainer-reference"))).text
        except:
            print('ERROR : Obteniendo la referencia')
            v_reference = 'ERROR'
    driver.execute_script("window.scrollTo(0, 0);")
    return v_reference

def getSeller(wait, driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_UP)
    sleepRand()
    try:
        v_seller = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.re-ContactDetail-inmoContainer-clientName"))).text
    except :
        try:
            v_seller = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".re-ContactDetail-inmoContainer-clientName"))).text
        except:
            print('ERROR : Obteniendo el vendedor')
            v_seller = 'ERROR'
    driver.execute_script("window.scrollTo(0, 0);")
    return v_seller

def getComment(wait):
    try:
        v_comment = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".fc-DetailDescription"))).text
    except :
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR," body"))).send_keys(Keys.PAGE_DOWN)
            v_comment = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".fc-DetailDescription"))).text
        except:
            print('ERROR : Obteniendo el comentario')
            v_comment = 'ERROR'
    return v_comment
