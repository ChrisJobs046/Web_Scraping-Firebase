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


meses = {'enero':'01', 'febrero':'02', 'marzo':'03', 'abril':'04', 'mayo':'05', 'junio':'06', 'julio':'07', 'agosto':'08', 'septiembre':'09', 'octubre':'10', 'noviembre':'11', 'diciembre':'12'}

def get_month(meses):

    keys = meses.keys()
    
    for key in keys:
        if key in meses:
            return meses[key]

def P_Z101Digital():

    datos = []


    website = 'https://z101digital.com/'
    PATH = os.getenv('W_PATH')
    with  webdriver.Chrome(PATH) as driver:
        driver.get(website)


        element1 = driver.find_elements_by_xpath("//div [@class='local-news section-space ']")
        element3 = driver.find_elements_by_xpath("//div [@class='col-xs-6 col-sm-4 col-md-4']")
        # element4 = driver.find_elements_by_class_name('title-news v-ellipsis')
        element5 = driver.find_elements_by_xpath("//div [@class='col-xs-6 col-sm-4 col-md-4']/h2")
        elementtos = element3 + element5

        for element in elementtos:
            
            Fuente = 'Z101Digital'
            title = None
            fecha = None
            a = None
            
            try:
                herf = element.find_element_by_tag_name('a')
                if herf:
                    a = herf.get_attribute('href')
                
            except Exception:
                pass

            try:
                title= element.find_element_by_tag_name('h2').text
            except Exception:
                    pass

            try:
                fecha = driver.find_element_by_xpath("//span [@class='letter-spacing theme-color-text date-time-website']").text
                fecha = str(fecha[0:2]+'/'+get_month(fecha)+'/'+fecha[-10:-14])#[:-15]
                # if fecha:
                #     fecha = fecha.get_attribute('datetime')#[-15:]
            except Exception:
                    pass

            dic = dict(title= title, href=a, fuente = Fuente, fecha = fecha)
            print(dic)
            datos.append(dic)
            cookies = driver.get_cookies()
            # print(f"main: cookies = {cookies}")
            driver.delete_all_cookies()
        driver.quit()
        return datos



FIREBASE = os.getenv('F_EndPoint')

F_EndPoint = 'https://pythonfirebase-d51e6-default-rtdb.firebaseio.com/'

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(F_EndPoint, None)

P_datos = P_Z101Digital()

result = firebase.post('/Monitoreo/prueba1', P_datos)
print(result)

#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    
    # P_Z101Digital()
    
    

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")