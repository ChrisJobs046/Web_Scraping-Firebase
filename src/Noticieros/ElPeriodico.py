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

def ElPeriodico():

    datos = []

    website = 'https://www.elperiodico.com.do/category/noticias/'

    PATH = os.getenv('W_PATH')

    with  webdriver.Chrome(PATH) as driver:
        driver.get(website)

        time.sleep(5)

        main(driver, datos)
        # print('Pag')
        # paginacion(driver, datos)

        # driver.quit()
        return datos


def main(driver, datos):

    # datos = []

    # elementX = driver.find_elements_by_xpath("//div[@class='vc_column tdi_119  wpb_column vc_column_container tdc-column td-pb-span9']")
    # element1 = driver.find_elements_by_xpath("//div[@class='col-lg-8 col-12']//div[@class='utf_post_content']")
    # element2 = driver.find_elements_by_xpath("//div[@class='col-md-12']")
    element3 = driver.find_elements_by_class_name('td_block_inner tdb-block-inner td-fix-index')
    elementtos = element3

    for element in elementtos:
            
            Fuente = 'El Periodico'
            title = None
            fecha = None
            a = None

            title = element.find_element_by_tag_name('h3').text
            
            try:
            #    title= element.find_element_by_tag_name('h2').text
               herf = element.find_element_by_tag_name('a')
               if herf:
                   a = herf.get_attribute('href')
                
            except Exception:
                pass

            try:
                fecha= element.find_element_by_tag_name('time')
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
    
    #validacion para buscar coincidencias dentro del diccionario y retornar ese objeto
    for key in datos:
        print(key, ":", datos[key])

    return datos



FIREBASE = os.getenv('F_EndPoint')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)

P_datos = ElPeriodico()
result = firebase.post('/Monitoreo/El Periodico', P_datos)

Defensor = firebase.post('/Defensor', None)
print(result)