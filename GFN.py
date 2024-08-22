# -*- coding: utf-8 -*-
"""
Created on Wed May  8 07:56:42 2024

@author: Student #Priwi
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import time
import anmeldung
from datetime import datetime

aktual_datum = datetime.now().strftime("%d.%m.%Y")
aktual_zeit = datetime.now().strftime("%H:%M")

log_message = ("")

driver = webdriver.Firefox()

 
driver.get("https://lernplattform.gfn.de/login/?land=de")

try:
    untericht = None
    try:
        Abreschnen = driver.find_element(By.XPATH, "//button[text()='Abbrechen']")
        Abreschnen.click()
    except NoSuchElementException:
        pass
    
    time.sleep(5)
    try:
        email_zehle = driver.find_element(By.ID, "username")
        email_zehle.send_keys(anmeldung.user_name)
        log_message = ("Zehle user name nicht gefunden ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
    
        
        email_zehle.send_keys(Keys.TAB)
        
        activ_zehler = driver.switch_to.active_element              # passwort zehler
        log_message = ("Zehler Passwort ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
        activ_zehler.send_keys(anmeldung.passwort)
        log_in = driver.find_element(By.ID, "loginbtn")
        
        log_message = ("Button Login ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
        
        log_in.click()
    except NoSuchElementException:
        abrechnen = driver.find_element(By.ID, "single_button663b33eb779583")
        log_message = ("Beenden bei log ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
        abrechnen.click()

    try:
        time.sleep(10)            
        anfang = EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'bitte starte jetzt')]"))
        
        if anfang:
            ok = driver.find_element(By.XPATH, "//button[text()='OK']")
            print(ok)
            ok.click()
            time.sleep(5)
     
    except Exception:
        pass
                
    try:
        untericht = driver.find_element(By.XPATH, "//div[@class='alert alert-warning' and text()='Heute kein Unterricht!']")
        print("Heute kein Unterricht!")
        # print(untericht)
        log_message = ("Heute kein Unterricht! ; " + str(aktual_datum) + " ; " + str(aktual_zeit)) 
    except NoSuchElementException:
        pass
        
    print(untericht)
    
    
    if untericht == None:
        try:
            homeoffice = driver.find_element(By.ID, "flexRadioDefault1")
            log_message = ("Ellement homeoffice ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
            homeoffice.click()
            
            Homeofficebestetigung = driver.find_element(By.XPATH, "//input[@value='Starten']")
            log_message = ("Start bei homeoffice ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
            Homeofficebestetigung.click()
            
            print("Bin angemeldet um:/n " + aktual_zeit)
            log_message = ("Angemeldet ; " + str(aktual_datum) + " ; " + str(aktual_zeit) + " ; ")
            
        except NoSuchElementException:
            try:
                abmelbung = driver.find_element(By.XPATH, "//button[text()='Beenden']")
                log_message = ("Beende bei abmeldung ist problem ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
                print(abmelbung)
                abmelbung.click()
                
                print("Bin abgemeldet um:/n " + aktual_zeit)
                log_message = ("Abgemeldet ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
            
                time.sleep(5)
            except NoSuchElementException:
                print("Abmeldung nicht möglich\nEs gibt keine BEENDEN button auf die seite")
                log_message = ("Beende button feld ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
                
    else:
        print("HOMMEOFFICE  nich gefunden ")
        log_message = ("Hommeoffice button feld ; " + str(aktual_datum) + " ; " + str(aktual_zeit))

except Exception as e:
    log_message = ("Error: " + str(e) + " ; " + str(aktual_datum) + " ; " + str(aktual_zeit))
    
    with open("Log.txt", "a") as file:
        file.write(log_message + "\n")

