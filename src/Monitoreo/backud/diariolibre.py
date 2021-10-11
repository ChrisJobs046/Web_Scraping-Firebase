from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By 
import time
import sched
# import listin
# import hoy
# import eldia
from firebase import firebase
from dotenv import load_dotenv
import os
#para borrar los datos en memoria
import gc



""" PATH = "C:/Users/jhoel/Downloads/chromedriver_win32 (1)/chromedriver" """

load_dotenv()

def diariolibre():

    datos = []
    website = 'https://www.diariolibre.com/resultados-busqueda/-/search/agosto/false/false/19790909/20210909/date/true/true/0/0/meta/0/0/0/53'
    PATH = os.getenv('W_PATH')
    driver = webdriver.Chrome(PATH)
    driver.get(website)

    time.sleep(5)
    articles = driver.find_elements_by_xpath("//div [@class='row']//h2 [@class='font-weight-regular']")
    # articles = driver.find_elements_by_tag_name('article')
    # articles2 = driver.find_element_by_xpath("//div [@class='pt-1 pb-1 author-container']//span[@class='author-date']")   
    elementtos = articles
    
    for element in elementtos:
        title = element.text
        Fuente = 'Diario Libre'
        a = None
        clasificados = None
        articles2 = element.find_element_by_xpath("//div [@class='pt-1 pb-1 author-container']//span [@class='author-date']").text 
        try:
         clasificados = element.find_elements_by_xpath("//div [@classr='mr-1 author']").text
         herf = element.find_element_by_class_name('col-8 py-3 px-3')
        #  articles2 = driver.find_elements_by_xpath("//div [@class='col-8 py-3 px-3']//span [@class='author-date']").text
            

         if herf:
            a = herf.get_attribute('href')
            
        except Exception:
            pass



        dic =  dict(title= title, href=a, fuente = Fuente, fecha = articles2, clasificados = clasificados)
        datos.append(dic)
        print(dic)
    driver.quit() 
    return datos
    


#para borrar la funcion lamama por lo tanto dara error
#del lamama()


FIREBASE = os.getenv('F_EndPoint')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)



data = diariolibre()
# data1 = hoy.Hoy()
# data2 = eldia.eldia()
# data3 = listin.listindiario()


#print(data)

result = firebase.post('/Monitoreo/Diario Libre',data)

# result1 = firebase.post('/Periodicos/periodico hoy',data1)

# result2 = firebase.post('/Periodicos/periodico el dia',data2)

# result3 = firebase.post('/Periodicos/periodico listindiario',data3)

#print(result)

#esta funcion borra los datos de memoria
#gc.collect()






#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    
    diariolibre()
    # listin.listindiario()
    # hoy.Hoy()
    # eldia.eldia()
    
    

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")