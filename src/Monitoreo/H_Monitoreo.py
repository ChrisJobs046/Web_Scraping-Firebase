from typing import cast
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By 
import time
import sched
from firebase import firebase
from dotenv import load_dotenv
import os
#para borrar los datos en memoria
import gc
#coding:utf-8
# import multiprocessing


date1 = 00
# date2 = 00


load_dotenv()

def Periodico2(website='https://hoy.com.do/str-search/?reseult'):

    # date_1 = ''
    # date_2 = ''
    datos = []
    PATH = os.getenv('W_PATH')

    with  webdriver.Chrome(PATH) as driver:
        driver.get(website)


    time.sleep(5)

    # main(driver, datos)
    paginacion(driver, datos)
    
    # Borrar cookies del navegador
    cookies = driver.get_cookies()
    print(f"main: cookies = {cookies}")
    driver.delete_all_cookies()
    driver.quit()
    return datos


def main(driver, datos):

    pag = driver.find_element_by_xpath("//span[@class='select2-selection__rendered']").click()
    pag = driver.find_element_by_xpath("//span[@class='select2-selection__rendered']")

    pag.click

    time.sleep(50)

    elements2 = driver.find_elements_by_xpath("//ul [@class='list-group list']//a [@class='lnktitle fltr-name']")

    fehcha = driver.find_element_by_xpath("//div [@class='mic-info']").text
    elements = elements2

            
    for element in elements:
            Fuente = 'Hoy'
            title = element.text
            a = None
            try:
                herf = element.find_element_by_xpath("//a [@class='lnktitle fltr-name']")
                # herf = element.find_element_by_tag_name('a')    
                if herf:
                    a = herf.get_attribute('href')
            except Exception:
                pass
            dic =  dict(title= title, href=a,fuente = Fuente, fecha = fehcha)
            
            datos.append(dic)
            print(dic)
    
    return datos

def paginacion(driver, datos):
    
    
    pageN = [1, 2, 3, 4, 5]
    
    for element in pageN:
        try:
            
            next_page = driver.find_element_by_class_name("pagination").find_element_by_link_text(str(element))
            # print(next_page.text)
            next_page.click()
            time.sleep(5)
            main(driver, datos)
        except: 
            break
        # cada vez que se ejecute click debe lanzar el scraping
    

FIREBASE = os.getenv('F_EndPoint')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)


#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    
    # Periodico2()
    
    

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")