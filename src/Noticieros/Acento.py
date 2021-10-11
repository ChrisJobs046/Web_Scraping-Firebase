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

def P_Acento():

    datos = []

    PATH = os.getenv('W_PATH')

    website = 'https://acento.com.do/seccion/actualidad.html'
    with  webdriver.Chrome(PATH) as driver:
        driver.get(website)

        time.sleep(5)
        articles = driver.find_elements_by_tag_name("article")
        elementtos = articles

        for element in elementtos:     
            Fuente = 'Noticias SIN'
            a = None
            title = None
            fecha = None
            clasificados = None
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
                    with webdriver.Chrome(PATH) as window: #esto habre una nueva pagina 
                        window.get(a)
                        fecha = window.find_element_by_xpath("//span [@class='post-date']").text[:-2]
            except Exception:
                pass

            try: 
                clasificados = element.find_element_by_tag_name('div').find_element_by_tag_name('span').text
            except Exception:
                pass



            dic = dict(title= title, href=a, fuente = Fuente,fecha = fecha,clasificados = clasificados)
            if dic['title'] != '':
                datos.append(dic)
            print(dic)
            
            cookies = driver.get_cookies()
            print(f"main: cookies = {cookies}")
            driver.delete_all_cookies()
        driver.quit()
        return datos




FIREBASE = os.getenv('F_EndPoint')

F_EndPoint = 'https://pythonfirebase-d51e6-default-rtdb.firebaseio.com/'

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(F_EndPoint, None)

P_datos = P_Acento()

result = firebase.post('/Monitoreo/Acento', P_datos)
print(result)