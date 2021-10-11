from selenium import webdriver
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
#coding:utf-8



date1 = 00
# date2 = 00


load_dotenv()

def Periodico2(website='https://listindiario.com/buscar?find=&datefrom=01-08-2021&dateto=01-08-2021'):

    # date_1 = ''
    # date_2 = ''
    datos = []
    PATH = os.getenv('W_PATH')

    driver = webdriver.Chrome(PATH)

    driver.get(website)


    time.sleep(5)

    main(driver, datos)

    page = [1, 2, 3, 4, 5]

    #     # localizar un botón
    # all_matches_button = driver.find_element_by_xpath("//ul [@class='pagination']//a [@class='page']")
    # # dar click en un botón
    # all_matches_button.click(page)

    # aqui traemos el numero de paginas disponibles
    # total_pages = len(driver.find_element_by_class_name("pagination").find_elements_by_tag_name("li"))
    # print ("total_pages is %s" %(total_pages))

    # next_page = driver.find_element_by_class_name("pagination").find_element_by_link_text("1")
    # next_page.click()

    # total_pages = 5
    
    # for page_number in range(0, total_pages):
    #     driver.find_element_by_css_selector()
    #     time.sleep(10)





def main(driver, datos):

    elements2 = driver.find_elements_by_xpath("//ul [@class='list-group list']//a [@class='lnktitle fltr-name']")

    fehcha = driver.find_element_by_xpath("//div [@class='mic-info']").text
    elements = elements2

            
    for element in elements:
            Fuente = 'Listin Diario'
            title = element.text
            a = None
            try:
                herf = element.find_element_by_tag_name('a')    
                if herf:
                    a = herf.get_attribute('href')
            except Exception:
                pass
            dic =  dict(title= title, href=a,fuente = Fuente, fecha = fehcha)
            
            datos.append(dic)
            print(dic)
    
    next_page = driver.find_element_by_class_name("pagination").find_element_by_link_text("2")
    # print(next_page.text)
    next_page.click()
    # cada vez que se ejecute click debe lanzar el scraping

    # driver.quit()
    return datos


for i in range(1, 32):
    
    website = f'https://listindiario.com/buscar?find=&datefrom={i}-08-2021&dateto={i}-08-2021'
    Periodico2(website)
    
    # print(f'https://listindiario.com/buscar?find=&datefrom={i}-08-2021&dateto={i}-08-2021')



FIREBASE = os.getenv('F_EndPoint')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)


# data = Periodico2()


# result = firebase.post('/Monitoreo/Listin Diario', data)

# print(result)


#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    
    # Periodico2()
    
    

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")