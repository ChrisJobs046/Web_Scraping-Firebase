""" from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By 
import time
import sched
from firebase import firebase
from dotenv import load_dotenv
import os
#para borrar los datos en memoria
import gc

load_dotenv()

def  lamama():
    #load_dotenv()
    website = 'https://listindiario.com'
    PATH = os.getenv('W_PATH')

    driver = webdriver.Chrome(PATH)

    driver.get(website)

    time.sleep(5)
    articles = driver.find_elements_by_class_name('topleftmain_titulo')
    #print(articles.text)

    datos = []
    for element in articles:
        title = element.text
        a = None
        try:
            herf = element.find_element_by_tag_name('a')    
            if herf:
                a = herf.get_attribute('href')
        except Exception:
            pass
        dic =  dict(title= title, href=a)
        #print(dic)
        datos.append(dic)
    driver.quit() 
    print(datos)
    return datos """
    

#para borrar la funcion lamama por lo tanto dara error
#del lamama()

""" 
FIREBASE = os.getenv('F_EndPoint')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)

data = lamama()

print(data)

result = firebase.post('/Periodicos/',data)

result2 = firebase.get('/Periodicos/', None)
print (result2)

#print(result)

#esta funcion borra los datos de memoria
#gc.collect()


timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    

    lamama()
    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()


print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------") """