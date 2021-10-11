from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By 
import time
import sched
# from firebase import firebase
from dotenv import load_dotenv
import os
import pyrebase

load_dotenv()



def P_ElCaribe(website = 'https://www.elcaribe.com.do/2021/01/01/'):

    datos = []

    PATH = os.getenv('W_PATH')

    driver = webdriver.Chrome(PATH)

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

    # datos = []

    # element1 = driver.find_elements_by_class_name("item-details")
    element2 =  driver.find_elements_by_xpath("//div[@class='td-ss-main-content']")
    # PagN = driver.find_elements_by_class_name("td-ss-main-content")
    elementtos = element2

    for element in elementtos:
            
            Fuente = 'El Caribe'
            title = None
            fecha = None
            a = None
            
            try:
            #    title = element.find_elements_by_xpath("//h3 [@class='entry-title td-module-title']").text
            #    title = element.find_elements_by_class_name("item-details").text
               herf = element.find_element_by_tag_name('a')

               if herf:
                   a = herf.get_attribute('href')
                
            except Exception:
                pass

            try:
                title = element.find_element_by_tag_name('a') 
                title = element.find_element_by_xpath("//h3 [@class='entry-title td-module-title']/a")
                # if title:
                #     title = title.get_attribute('title')  
            except Exception:
                    pass

            try:
                fecha= element.find_element_by_tag_name('time') 
                if fecha:
                    fecha = fecha.get_attribute('datetime')
            except Exception:
                    pass

            dic =  dict(title= title, href=a, fuente = Fuente, fecha = fecha )
            print(dic)
            datos.append(dic)
    # driver.quit()
    return datos


def paginacion(driver, datos):

    # title = "//div[@class='page-nav td-pb-padding-side']/div[@class='clearfix']"
    pageN = [1, 2, 3, 4, 5]
    
    for element in pageN:
            try:
                
                next_page = driver.find_element_by_xpath("//div[@class='page-nav td-pb-padding-side']/a[@class='page']").find_element_by_link_text(str(element))
                
                # print(next_page.text)

                next_page.click()
                time.sleep(5)
                main(driver, datos)
            except Exception as e:
                print(e)
                pass

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
    
    website = f'https://www.elcaribe.com.do/2021/01/{i}/'
    # Periodico2(website)

    data = P_ElCaribe(website)

    db.child("users").child("Morty").set(data)
    print(data)
    print("Data added to real time database ")
    
    # P_datos = P_ElCaribe(website)
    # result = firebase.post('/Monitoreo/Listin Diario', P_datos)
    # print(result)



#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    
    P_ElCaribe()
    
    

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")