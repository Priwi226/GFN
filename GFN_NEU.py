#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:18:05 2024

@author: priwi
"""

import selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
import time
import anmeldung
from datetime import datetime
import sys
import Localization


abmeldung = None
log_message = ("")
                            # Selenium chrome richtige folder !! richtige version !!
chromedriver_path = "/home/priwi/Selenium/chromedriver"

                            # browser einstelungen 
chrome_options = Options()
if anmeldung.browser == 0:
    chrome_options.add_argument("--headless")  # ohne window startup /// fur cron

service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://lernplattform.gfn.de/login/?land=de")

                            # Aktual datum zeit
aktual_datum = datetime.now().strftime("%d.%m.%Y")
aktual_zeit = datetime.now().strftime("%H:%M")


                            # Log in
                                # user name 
try:
    email_zehle = driver.find_element(By.ID, "username")
    email_zehle.send_keys(anmeldung.user_name)
    log_message = ("Zehle user name gefunden ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
except NoSuchElementException:
    log_message = ("Zehle user name nicht gefunden ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
    print(log_message)
    sys.exit()

                            # not fur passwort
email_zehle.send_keys(Keys.TAB)

activ_zehler = driver.switch_to.active_element  # passwort zehler

try:                # funkzuniert kein ID XPATH CLASS_NAME vrrrrrr
    # password_zehle = driver.find_element(By.CLASS_NAME, "login-form-password form-group")
    # print("PASSWORD ID " + password_zehler)
    # password_zehle.click()
    # password_zehle.send_keys(anmeldung.passwort)
    activ_zehler.send_keys(anmeldung.passwort)
    log_message = ("Passwort eingegeben ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
except Exception as e:
    log_message = ("Zehler Passwort ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + " ; " + str(e))
    print(log_message)
    sys.exit()


                    # LOG_IN BUTTON
try:
    log_in = driver.find_element(By.ID, "loginbtn")
    time.sleep(5)
    log_in.click()
    log_message = ("Button Login geklickt ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
except NoSuchElementException:
    log_message = ("Button Login ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
    print(log_message)
    sys.exit()

# print(log_message)

                        # ALERT window
try:
    alert = driver.switch_to.alert
    # print("Text alert:", alert.text)
    alert.accept()
    # print("Alert ist gefunden")
    alert = ("Alert")
except:
    # print("Alert fehler")
    alert = ("no Alert")

                        # Feile / seite panel
                        
try:
    time.sleep(5)
    feile = driver.find_element(By.CSS_SELECTOR, "button.btn.icon-no-margin[title='Blockleiste öffnen']")
    #feile = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.icon-no-margin[title='Blockleiste öffnen']")))
    # print(feile)
    feile.click()
    log_message = ("Button gefunden und geklickt ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
except (NoSuchElementException, ElementNotInteractableException, TimeoutException) as e:
    log_message = ("Button nicht gefunden oder nicht interagierbar ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + " ; " + str(e))
    print(log_message)
    sys.exit()

# print(log_message)

# Alte kod

                        # star button / funkcion
try:
    wait = WebDriverWait(driver, 20)
    time.sleep(2)            
    anfang = EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'bitte starte jetzt')]"))
    
    if anfang:
        ok = driver.find_element(By.XPATH, "//button[text()='OK']")
        #print(ok)
        ok.click()
        time.sleep(5)
 
except Exception:
    pass


                                # kein untericht
try:
    untericht = driver.find_element(By.XPATH, "//div[@class='alert alert-warning' and text()='Heute kein Unterricht!']")
    print("Heute kein Unterricht!")
    log_message = ("Heute kein Unterricht! ; " + str(aktual_datum) + " ; " + str(aktual_zeit)) 
except NoSuchElementException:
    untericht = None  # Pridanie tejto línie

# print(untericht)



                            # 
if untericht is None:
    latitude, longitude, standort = Localization.get_geolocation()
    if standort == 1:
        try:
            homeoffice = driver.find_element(By.ID, "flexRadioDefault2")  # flexRadioDefault1 = Homeoffice  /// flexRadioDefault2 = Standort
            log_message = ("Ellement homeoffice ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
            homeoffice.click()
            
            Homeofficebestetigung = driver.find_element(By.XPATH, "//input[@value='Starten']")
            log_message = ("Start bei homeoffice ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
            Homeofficebestetigung.click()
            
            print("Bin angemeldet um:/n " + aktual_zeit)
            log_message = ("Angemeldet ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
            
        except NoSuchElementException:
            try:
                                            # abmeldung
                abmelbung = driver.find_element(By.XPATH, "//button[text()='Beenden']")
                log_message = ("Beende bei abmeldung ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
                print(abmelbung)
                abmelbung.click()
                
                print("Bin abgemeldet um:/n " + aktual_zeit)
                log_message = ("Abgemeldet ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
            
                time.sleep(5)
            except NoSuchElementException:
                                # nach untericht 
                if abmeldung == None and untericht == None:
                    log_message = ("Heute ist dein unterich angeschlosen ;" + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
                    print(log_message)
                
                else:
                    print("Abmeldung nicht möglich\nEs gibt keine BEENDEN button auf die seite")
                    log_message = ("Beende button feld ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
    else:
        try:
            homeoffice = driver.find_element(By.ID, "flexRadioDefault1")  # flexRadioDefault1 = Homeoffice  /// flexRadioDefault2 = Standort
            log_message = ("Ellement homeoffice ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
            homeoffice.click()
            
            Homeofficebestetigung = driver.find_element(By.XPATH, "//input[@value='Starten']")
            log_message = ("Start bei homeoffice ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
            Homeofficebestetigung.click()
            
            print("Bin angemeldet um:/n " + aktual_zeit)
            log_message = ("Angemeldet ; " + str(aktual_datum) + " ; " + str(aktual_zeit) +  + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
            
        except NoSuchElementException:
            try:
                                            # abmeldung
                abmelbung = driver.find_element(By.XPATH, "//button[text()='Beenden']")
                log_message = ("Beende bei abmeldung ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
                print(abmelbung)
                abmelbung.click()
                
                print("Bin abgemeldet um:/n " + aktual_zeit)
                log_message = ("Abgemeldet ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
            
                time.sleep(5)
            except NoSuchElementException:
                                # nach untericht 
                if abmeldung == None and untericht == None:
                    log_message = ("Heute ist dein unterich abgeschlosen ;" + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
                    print(log_message)
                
                else:
                    print("Abmeldung nicht möglich\nEs gibt keine BEENDEN button auf die seite")
                    log_message = ("Beende button feld ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
    
    try:
        homeoffice = driver.find_element(By.ID, "flexRadioDefault2")  # flexRadioDefault1 = Homeoffice  /// flexRadioDefault2 = Standort
        log_message = ("Ellement homeoffice ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
        homeoffice.click()
        
        Homeofficebestetigung = driver.find_element(By.XPATH, "//input[@value='Starten']")
        log_message = ("Start bei homeoffice ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
        Homeofficebestetigung.click()
        
        print("Bin angemeldet um:/n " + aktual_zeit)
        log_message = ("Angemeldet ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
        
    except NoSuchElementException:
        try:
                                        # abmeldung
            abmelbung = driver.find_element(By.XPATH, "//button[text()='Beenden']")
            log_message = ("Beende bei abmeldung ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
            print(abmelbung)
            abmelbung.click()
            
            print("Bin abgemeldet um:/n " + aktual_zeit)
            log_message = ("Abgemeldet ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
        
            time.sleep(5)
        except NoSuchElementException:
                            # nach untericht 
            if abmeldung == None and untericht == None:
                log_message = ("Heute ist dein unterich angeschlosen ;" + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
                print(log_message)
            
            else:
                print("Abmeldung nicht möglich\nEs gibt keine BEENDEN button auf die seite")
                log_message = ("Beende button feld ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))
            
else:
    print("HOMMEOFFICE  nich gefunden ")
    log_message = ("Hommeoffice button feld ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + ";" + "GPS lokalisation: " + str(latitude) + " : " + str(longitude))

log_file_path = "/home/priwi/Plocha/Python/GFN/log.txt"
with open(log_file_path, 'a') as file:
    file.write(log_message + " " + alert + '\n')