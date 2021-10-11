from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    # if meses.included("enero"):
    #     return meses[keys]

def P_Cdn(website = 'https://cdn.com.do/noticias/nacionales/'):

    datos = []

    # website = 'https://cdn.com.do/noticias/nacionales/'
    PATH = os.getenv('W_PATH')
    with  webdriver.Chrome(PATH) as driver:
        driver.get(website)

        time.sleep(5)

        element1 = driver.find_elements_by_class_name("item-details")
        elementtos = element1

        for element in elementtos:

            Fuente = 'CDN'
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
                title= element.find_element_by_tag_name('a') 
                if title:
                    title = title.get_attribute('title')  
            except Exception:
                    pass

            try:
                fecha= element.find_element_by_tag_name('time')
                if fecha:
                    fecha = fecha.get_attribute('datetime')[:-15]
                    fecha = fecha[8:10]+'/'+fecha[5:7]+'/'+fecha[0:4]
                    # fecha = str(fecha[0:2]+'/'+get_month(fecha)+'/'+fecha[-10:-14])[:-15]
            except Exception:
                    pass

            dic = dict(title= title, href=a, fuente = Fuente, fecha = fecha )
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
P_datos = P_Cdn()
result = firebase.post('/Monitoreo/Cdn', P_datos)
print(result)

# for i in range(1, 32):
    
#     website = f'https://cdn.com.do/noticias/nacionales/'
#     # Periodico2(website)
    
#     P_datos = P_Cdn(website)
#     result = firebase.post('/Monitoreo/Cdn', P_datos)
#     print(result)



#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    
    P_Cdn()
    
    

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")