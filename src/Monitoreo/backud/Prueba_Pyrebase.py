from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import sched
from dotenv import load_dotenv
import os
import pyrebase

load_dotenv()

date1 = 00

PATH = os.getenv('W_PATH')

def P_ListinDiario(website='https://listindiario.com/buscar?find=&datefrom=01-08-2021&dateto=01-08-2021'):

    datos = []

    with  webdriver.Chrome(PATH) as driver:
        
        driver.get(website)


        time.sleep(15)

        # main(driver, datos)
        paginacion(driver, datos)
        # driver.quit()
        # Borrar cookies del navegador
        cookies = driver.get_cookies()
        # print(f"main: cookies = {cookies}")
        driver.delete_all_cookies()
        
        driver.quit()

        return datos



def main(driver, datos):

    elements2 = driver.find_elements_by_xpath("//div [@class='LstItem100']")

    fehcha = driver.find_element_by_xpath("//div [@class='mic-info']").text[-10:]
    # print(fehcha[-10:])
    elements = elements2

            
    for element in elements:
            Fuente = 'Listin Diario'
            title = element.text
            a = None,
            clasificados = None
            desc = None

            try:
                # herf = element.find_element_by_xpath("//a [@class='lnktitle fltr-name']")
                clasificados = element.find_element_by_xpath("//span [@class='label label-warning button-bottom fltr-seccion']").text
                herf = element.find_element_by_tag_name('a')
                if herf:
                    a = herf.get_attribute('href')

                with webdriver.Chrome(PATH) as window:
                    window.get(a)
                    # desc = window.find_element("//div [@id='ArticleBody']/p")
                    desc = window.find_element_by_id('ArticleBody')
                    desc2 = desc.find_elements_by_tag_name('p')
                    # realizar una condicion que busque por etiqueta div, y span aparte del p
                    for element in desc2:
                        if element.text != '\n':
                            print(element.text)
                            desc = element.text
                            break
                            # desc = desc.replace(element, ' ')
                    # if desc == '':
                    #     desc = window.find_element_by_xpath("//div [@id='ArticleBody']/p/p").text
                window.close()
                
                

            except Exception as e:
                print(e)
                pass
            dic =  dict(title= title, href=a,fuente = Fuente, descripcion = desc, fecha = fehcha, clasificados = clasificados)
            if dic['descripcion'] == '':
                    dic['descripcion'] = 'No hay descripcion o  contiene un video'
            if dic['title'] != '':
                datos.append(dic)
                # print(dic)

    # driver.quit()
    return datos

def paginacion(driver, datos):
    
    
    pageN = [1, 2, 3, 4, 5]
    
    for element in pageN:
        try:
            
            next_page = driver.find_element_by_class_name("pagination").find_element_by_link_text(str(element))
            
            next_page.click()
            time.sleep(5)
            main(driver, datos)
        except: 
            break
        # cada vez que se ejecute click debe lanzar el scraping

APIKEY = os.getenv('apiKey')
AUTHDOMAIN = os.getenv('authDomain')
DATABASEURL = os.getenv('databaseURL')
STORAGE_B = os.getenv('storageBucket')

config = {
  "apiKey": APIKEY,
  "authDomain": AUTHDOMAIN,
  "databaseURL": DATABASEURL,
  "storageBucket": STORAGE_B
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

for i in range(1, 2):
    
    website = f'https://www.elcaribe.com.do/2021/01/{i}/'
    # Periodico2(website)

    P_datos = P_ListinDiario(website)
    result = db.child("Prueba").child("Morty").set(P_datos)
    print(result)
    print("Data added to real time database ")

    

#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):

    
    # P_ElCaribe()
    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")


