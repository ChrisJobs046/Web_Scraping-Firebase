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

def NoticiasSIN():

    datos = []

    website = 'https://noticiassin.com/seccion/ultimas-noticias'
    PATH = os.getenv('W_PATH')
    driver = webdriver.Chrome(PATH)
    driver.get(website)

    time.sleep(5)
    articles = driver.find_elements_by_tag_name("article")
    elementtos = articles

    for element in elementtos:     
        Fuente = 'Noticias SIN'
        a = None
        title = None
        fecha = None
        clasificados= element.find_element_by_xpath("//div [@class='entry-data'] /span [@class='volanta']").text
        try:
            title= element.find_element_by_tag_name('a') 
            if title:
                title = title.get_attribute('title')  
        except Exception:
            pass

        try: 
            herf = element.find_element_by_tag_name('a')
            if herf:
                a = herf.get_attribute('href')
                with webdriver.Chrome(PATH) as window:
                    window.get(a)
                    fecha = window.find_element_by_xpath("//span [@class='fecha']").text[:-2]
        except Exception:
            pass
        try: 
            fecha = element.find_element_by_link_text('title').find_element_by_class_name('fecha')
            fecha.click()
            fecha.text
        except Exception:
            pass

        dic = dict(title= title, href=a, fuente = Fuente,fecha = fecha,clasificados = clasificados)
        datos.append(dic)
        print(dic)
    cookies = driver.get_cookies()
    print(f"main: cookies = {cookies}")
    driver.delete_all_cookies()
    driver.quit()
    return datos

FIREBASE = os.getenv('F_EndPoint')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)

P_datos = NoticiasSIN()
result = firebase.post('/Monitoreo/NoticiasSIN', P_datos)
# driver.quit()
print(result)

# for i in range(53, 1937):
    
#     website = f'https://www.diariolibre.com/resultados-busqueda/-/search/agosto/false/false/19790909/20210909/date/true/true/0/0/meta/0/0/0/{i}'
#     # Periodico2(website)
    
#     P_datos = NoticiasSIN(website)
#     result = firebase.post('/Monitoreo/NoticiasSIN', P_datos)
#     # driver.quit()
#     print(result)
#     # print(f'https://listindiario.com/buscar?find=&datefrom={i}-08-2021&dateto={i}-08-2021')


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