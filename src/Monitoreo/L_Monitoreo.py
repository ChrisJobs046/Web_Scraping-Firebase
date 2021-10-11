from typing import cast
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By 
import time
import sched
from firebase import firebase
import pyrebase
from dotenv import load_dotenv
import os
#para borrar los datos en memoria
import gc
from selenium.webdriver.chrome.options import Options
#coding:utf-8
# import multiprocessing
import json

load_dotenv()

chrome_options = Options()
# options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'")

chrome_options.add_argument('--disable-gpu')
# options.add_argument('--headless')

chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('enable-automation')
chrome_options.add_argument('--dns-prefetch-disable')
chrome_options.add_argument("--disable-offline-load-stale-cache") 
chrome_options.add_argument("--disk-cache-size=0")
chrome_options.add_argument("--aggressive-cache-discard")
chrome_options.add_argument("--disable-cache")
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument ("-disable-plugins")
chrome_options.add_argument ("-disable-popup-block")
chrome_options.add_argument('--ignore-certificate-error')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('-incognito')
chrome_options.add_argument('test-type')
# chrome_options.add_argument("enable-features=NetworkServiceInProcess")
# chrome_options.add_argument("disable-features=NetworkService")
chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-browser-side-navigation")

# chrome_options.setPageLoadStrategy('normal')

# options.add_argument('log-level=3')
# chrome_options.add_argument('-no-sandbox')
chrome_options.add_argument("--disable-webgl")
# chrome_options.add_argument ('blink-settings = imagesEnabled = false') #no carga las imagenes, acelera

prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# chrome_options.add_argument('--disable-logging')

# options.add_argument(f"user-agent={userAgent}")

chrome_options.add_argument("no-default-browser-check")
# options.add_argument("no-first-run")

# chrome_options.add_argument('--single-process') # Operación de un solo proceso 

# chrome_options.add_argument("--process-per-site") # Cada sitio usa un proceso separado

caps = webdriver.DesiredCapabilities.CHROME.copy()
caps['acceptInsecureCerts'] = True
caps['acceptSslCerts'] = True

# proxy='222.221.11.119:3128'
# chrome_options.add_argument('--proxy-server=http://'+ proxy) ා set proxy

PATH = os.getenv('W_PATH')

def P_ListinDiario(website='https://listindiario.com/buscar?find=&datefrom=01-01-2021&dateto=01-01-2021'):

    datos = []

    # options = webdriver.ChromeOptions()
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.headless = True

    with  webdriver.Chrome(PATH, options=chrome_options, desired_capabilities=caps) as driver:

        driver.get(website)

        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")  #desliza la pag hasta abajo


        time.sleep(4)
        # driver.save_screenshot('screenshot.png') #guarda la pantalla

        agent = driver.execute_script ("return navigator.userAgent")
        print(agent)

        # main(driver, datos)
        paginacion(driver, datos)
        # Borrar cookies del navegador
        cookies = driver.get_cookies()
        # print(f"main: cookies = {cookies}")
        driver.delete_all_cookies()
        driver.quit()

    # driver.quit()
    return datos


def WebElement():
    print("WebElement")


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

                with webdriver.Chrome(PATH,  options=chrome_options, desired_capabilities=caps) as window:
                    
                    window.get(a)

                    window.set_page_load_timeout(4)
                    window.implicitly_wait(5)

                    # desc = window.find_element("//div [@id='ArticleBody']/p")
                    desc = window.find_element_by_id('ArticleBody')
                    desc2 = desc.find_elements_by_tag_name('p')
                    # realizar una condicion que busque por etiqueta div, y span aparte del p
                    for element in desc2:
                        if element.text != '\n' and element.text != " ":
                            # print(element.text)
                            desc = element.text
                            break
                            # desc = desc.replace(element, ' ')
                    # if desc == '':
                    #     desc = window.find_element_by_xpath("//div [@id='ArticleBody']/p/p").text
                    if type(desc) is not str:
                        try:
                                desc2 = desc.find_elements_by_tag_name('div').text
                                for element in desc2:
                                    if element.text != '\n' and element.text != " ":
                                        # print(element.text)
                                        desc = element.text
                                        break
                        except Exception as e:
                            print(e)
                        else:
                            desc = desc2 = desc.find_elements_by_tag_name('span').text
                        finally:
                            if type(desc) is not str:
                                desc = 'no se encontro una descripcion'
                    window.close()
                    window.quit()

            except Exception as e:
                print(e)
                break

            dic =  dict(title= title, href=a,fuente = Fuente, descripcion = desc, fecha = fehcha, clasificados = clasificados)
            
            if dic['descripcion'] == '' or len(dic['descripcion']) < 13:
                    dic['descripcion'] = 'No hay descripcion o  contiene un video'
            if dic['title'] != '':
                datos.append(dic)
                print(dic)
    print(type(datos))
    return datos


def paginacion(driver, datos):
    
    pageN = [1, 2, 3, 4, 5]
    
    for element_num in pageN:
        try:
            
            next_page = driver.find_element_by_class_name("pagination").find_element_by_link_text(str(element_num))
            
            next_page.click()

            time.sleep(2)

            main(driver, datos)
            # return datos
        except:
            driver.quit() 
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

# FIREBASE = os.getenv('F_EndPoint')

# # esta parte esta hecha por mi
# firebase = firebase.FirebaseApplication(FIREBASE, None)

for i in range(1, 32):

    website = f'https://listindiario.com/buscar?find=&datefrom={i}-01-2021&dateto={i}-01-2021'
    
    P_datos = P_ListinDiario(website)

    print(type(P_datos))
    # json_object = json.dumps(P_datos) 
    # json_object = json.dumps(P_datos, default=lambda o: '<not serializable>')
    # json.dumps(P_datos)
    print('punto antes de que me muestre lo que hay en p_datos')
    print(P_datos)
    result = db.child("Monitoreo").child("Listin Diario").push(P_datos)
    print(result)
    print("Data added to real time database ")
    # result = firebase.post('/Monitoreo/Prueba', json_object)
    # result = firebase.post('/Monitoreo/Prueba', P_datos)
    # print(result)
    # print(f'https://listindiario.com/buscar?find=&datefrom={i}-08-2021&dateto={i}-08-2021')

# result = multiprocessing.Pool(1).map(paginacion, main, Periodico2 #[]
# )[0]

#esta funcion borra los datos de memoria
#gc.collect()


#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    
    

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")