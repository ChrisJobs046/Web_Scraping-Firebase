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

load_dotenv()

meses = {'enero':'01', 'febrero':'02', 'marzo':'03', 'abril':'04', 'mayo':'05', 'junio':'06', 'julio':'07', 'agosto':'08', 'septiembre':'09', 'octubre':'10', 'noviembre':'11', 'diciembre':'12'}


def get_month(fehcha: str):

    keys = meses.keys()
    
    for key in keys:
        if fehcha.find(key)!= -1:
            return meses[key]

def P_DiarioLibre(website='https://www.diariolibre.com/resultados-busqueda/-/search/agosto/false/false/19790909/20210909/date/true/true/0/0/meta/0/0/0/53'):
    
    datos = []
    PATH = os.getenv('W_PATH')

    with  webdriver.Chrome(PATH) as driver:
        driver.get(website)


        time.sleep(5)

        main(driver, datos)
        # paginacion(driver, datos)
        
        # Borrar cookies del navegador
        cookies = driver.get_cookies()
        # print(f"main: cookies = {cookies}")
        driver.delete_all_cookies()
        driver.quit()
        return datos
        page = [1, 2, 3, 4, 5]



def main(driver, datos):

    PATH = os.getenv('W_PATH')

    elements2 = driver.find_elements_by_xpath("//div[@class='col-8 py-3 px-3']")
    elements = elements2

    print (elements2)

            
    for element in elements:

            Fuente = 'Listin Diario'

            a = None
            clasificados = None
            fehcha = None
            desc = None

            try:
                title = element.find_element_by_tag_name('h2').text
                fehcha = element.find_element_by_class_name('author-date').text[-29:-9]

                print(fehcha[-5:])
                fehcha = str(fehcha[0:2]+'/'+get_month(fehcha)+'/'+fehcha[-5:])

                herf = element.find_element_by_tag_name('a')
                clasificados = element.find_element_by_class_name("col-10").text
                if herf:
                    a = herf.get_attribute('href')
                    with webdriver.Chrome(PATH) as window:
                        window.get(a)
                        desc = window.find_element_by_xpath("//div [@class='paragraph']").text

            except Exception as e:
                print(e)
                pass



            dic =  dict(title= title, href=a, descripcion = desc, fuente = Fuente, fecha = fehcha, clasificados = clasificados)
            
            datos.append(dic)
            print(dic)
            #prueba y error
            # driver.quit()
    
    return datos

FIREBASE = os.getenv('F_EndPoint')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)


for i in range(53, 1937):
    
    website = f'https://www.diariolibre.com/resultados-busqueda/-/search/agosto/false/false/19790909/20210909/date/true/true/0/0/meta/0/0/0/{i}'

    P_datos = P_DiarioLibre(website)
    result = firebase.post('/Monitoreo/Prueba', P_datos)
    # driver.quit()
    print(result)
    # print(f'https://listindiario.com/buscar?find=&datefrom={i}-08-2021&dateto={i}-08-2021')


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