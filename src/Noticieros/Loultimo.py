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


def P_LoUltimo():

    datos = []

    PATH = os.getenv('W_PATH')


    website = 'https://loultimodigital.com'
    with  webdriver.Chrome(PATH) as driver:
        driver.get(website)

        time.sleep(5)
        articles = driver.find_elements_by_class_name("jet-smart-listing__post-content")
        elementtos = articles

        for element in elementtos: 

            Fuente = 'Lo Ultimo Digital'
            a = None
            title = None
            fecha = None
            clasificados = 'Noticias'
            try:

                title= element.find_element_by_tag_name('h6').text  
            except Exception:
                pass
            
            try: 
                
                herf = element.find_element_by_tag_name('a')
                if herf:
                    a = herf.get_attribute('href')
            except Exception:
                    pass

            try: 

                fecha = element.find_element_by_tag_name('div').find_element_by_tag_name('span').text
            except Exception:
                pass



            dic = dict(title= title, href=a, fuente = Fuente,fecha = fecha,clasificados= clasificados)
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

P_datos = P_LoUltimo()

result = firebase.post('/Monitoreo/Lo Ultimo', P_datos)
print(result)
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
    
    # P_LoUltimo()
    
    

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")