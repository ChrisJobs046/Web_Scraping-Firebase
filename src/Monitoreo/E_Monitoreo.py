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
#coding:utf-8



load_dotenv()

def P_ElDia(website='https://eldia.com.do/nacionales/'):

    datos = []
    PATH = os.getenv('W_PATH')

    with  webdriver.Chrome(PATH) as driver:
        driver.get(website)


        time.sleep(60)

        # main(driver, datos)
        paginacion(driver, datos)
        
        # Borrar cookies del navegador
        cookies = driver.get_cookies()
        print(f"main: cookies = {cookies}")
        driver.delete_all_cookies()
        driver.quit()
        return datos
        page = [1, 2, 3, 4, 5]



def main(driver, datos):
    
    try:
        elements2 = driver.find_elements_by_xpath("//div[@class='col-md-8']")
    except  Exception:
        pass

    print(elements2)

    fehcha = driver.find_element_by_xpath("//div [@class='col-md-8']//i [@class='fa fa-clock-o']").text
    elements = elements2

            
    for element in elements:
            Fuente = 'El Dia'
            title = element.text
            a = None,
            clasificados = None
            try:
                herf = element.find_element_by_xpath("//div [@class='col-md-8']//div [@class='post-content']")
                des = element.find_element_by_xpath("//p [@style='text-align: justify;']").text
                clasificados = 'Nacionales'
                # herf = element.find_element_by_tag_name('a')    
                if herf:
                    a = herf.get_attribute('href')
            except Exception:
                pass
            dic =  dict(title= title, href=a,fuente = Fuente, descripcion=des, fecha = fehcha, clasificados = clasificados)
            
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
        

FIREBASE = os.getenv('F_EndPoint')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)


for i in range(28, 100):
    
    website = f'https://eldia.com.do/nacionales/page/{i}/'
    
    P_datos = P_ElDia(website)
    result = firebase.post('/Monitoreo/El Dia', P_datos)
    print(result)

#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")