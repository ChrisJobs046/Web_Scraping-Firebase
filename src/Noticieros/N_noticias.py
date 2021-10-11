from typing import NewType
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



def P_N_Nacional(website = 'https://n.com.do/category/nacionales/'):

    datos = []

    PATH = os.getenv('W_PATH')

    with  webdriver.Chrome(PATH) as driver:
        driver.get(website)

        time.sleep(5)

        main(driver, datos)
        print('Pag')
        paginacion(driver, datos)

        # Borrar cookies del navegador
        cookies = driver.get_cookies()
        print(f"main: cookies = {cookies}")
        driver.delete_all_cookies()

        driver.quit()
        return datos

    


def main(driver, datos):


    elements2 = driver.find_elements_by_xpath("//div[@class='saxon-grid-post saxon-post format-']")
    elementtos = elements2

    for element in elementtos:
            
            Fuente = 'N DIGITAL'
            title = None
            fecha = None
            a = None
            clasificados = None
            
            try:
               clasificados = 'Nacionales'
            
               herf = element.find_element_by_tag_name('a')
               if herf:
                   a = herf.get_attribute('href')
                
            except Exception:
                pass

            try:
                title= element.find_element_by_tag_name('h3').text

            except Exception:
                    pass

            try:
                fecha= element.find_element_by_class_name('post-date').text
                
            except Exception:
                    pass

            dic = dict(title= title, href=a, fuente = Fuente, fecha = fecha, clasificados = clasificados)
            print(dic)
            datos.append(dic)
    # driver.quit()
    return datos


def paginacion(driver, datos):
    
    pageN = [1, 2, 3, 4, 5]
    
    for element in pageN:
        try:
            
            next_page = driver.find_element_by_class_name("wp-pagenavi").find_element_by_link_text(str(element))
            # print(next_page.text)
            next_page.click()
            time.sleep(5)
            main(driver, datos)
        except: 
            break


# def Modified(driver, datos):
#     fecha = []

FIREBASE = os.getenv('F_EndPoint')

F_EndPoint = 'https://pythonfirebase-d51e6-default-rtdb.firebaseio.com/'



# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(F_EndPoint, None)

P_datos = P_N_Nacional()
result = firebase.post('/Monitoreo/N Digital', P_datos)

# for i in range(1, 32):
    
#     website = f'https://n.com.do/category/nacionales/'
#     # Periodico2(website)
    
#     P_datos = P_ElCaribe(website)
#     result = firebase.post('/Monitoreo/N Digital', P_datos)
#     print(result)



#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    
    # P_N_Nacional()
    
    

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")