from typing import NewType
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import sched
from firebase import firebase
from dotenv import load_dotenv
import os, gc

load_dotenv()



def P_ElNacional():

    datos = []

    website = 'https://elnacional.com.do/secciones/actualidad/'

    PATH = os.getenv('W_PATH')

    with  webdriver.Chrome(PATH) as driver:
        driver.get(website)

        time.sleep(5)

        main(driver, datos)
        # print('Pag')
        # paginacion(driver, datos)

        # Borrar cookies del navegador
        # cookies = driver.get_cookies()
        # print(f"main: cookies = {cookies}")
        # driver.delete_all_cookies()

        # driver.quit()
        return datos

    


def main(driver, datos):

    # datos = []

    # element1 = driver.find_elements_by_class_name("item-details")
    element1 = driver.find_elements_by_xpath("//div[@class='col-lg-8 col-12']//div[@class='utf_post_content']")
    element2 = driver.find_elements_by_xpath("//div[@class='col-md-12']")
    elementtos = element1 + element2

    for element in elementtos:
            
            Fuente = 'El Nacional'
            title = None
            fecha = None
            a = None

            title = element.find_element_by_tag_name('h2').text
            
            try:
            #    title= element.find_element_by_tag_name('h2').text
               herf = element.find_element_by_tag_name('a')
               if herf:
                   a = herf.get_attribute('href')
                
            except Exception:
                pass

            try:
                fecha= element.find_element_by_class_name('utf_post_date').text
            except Exception:
                    pass

            dic = dict(title= title, href=a, fuente = Fuente, fecha = fecha )
            
            if dic['title'] != '':
                datos.append(dic)
                print(dic)
            
            # del driver
            # gc.collect()
    cookies = driver.get_cookies()
    print(f"main: cookies = {cookies}")
    driver.delete_all_cookies()
    driver.quit()
    return datos


# def paginacion(driver, datos):
    
    
#     pageN = [1,2,3,4,5]
#     top = 0
#     print('perro')
#     while True:
#         try:
#             next_page = driver.find_element_by_xpath("//div[@class='paging']").find_elements_by_tag_name("a")
#             current = driver.find_element_by_xpath("//div[@class='page-nav td-pb-padding-side']").find_element_by_class_name("current")
#             link = next_page[-1].get_attribute('href') 
#             top = next_page[-1].get_attribute('title')
#             if top and current.text:
#                 if int(current.text) > int(top):
#                     break
#             driver.get(link)
#             time.sleep(5)
#             main(driver, datos)
#         except Exception as e:
#             print(e)
#             break


# def Modified(driver, datos):
#     fecha = []

FIREBASE = os.getenv('F_EndPoint')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)

P_datos = P_ElNacional()
result = firebase.post('/Monitoreo/El Nacional', P_datos)
print(result)

# for i in range(1, 32):
    
#     # website = f'https://elnacional.com.do/secciones/actualidad/'
#     # Periodico2(website)
    
#     P_datos = P_ElNacional(website)
#     result = firebase.post('/Monitoreo/El Nacional', P_datos)
#     print(result)



#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    
    # P_ElNacional()
    
    

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")