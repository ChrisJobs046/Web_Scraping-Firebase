from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By 
import time
import sched
from dotenv import load_dotenv
import os

load_dotenv()

def elcaribe():

    PATH = os.getenv('W_PATH')



    website = 'https://www.elcaribe.com.do/2021/01/01/'

    driver = webdriver.Chrome(PATH)

    driver.get(website)

    element1 = driver.find_elements_by_class_name("item-details")
    elementtos = element1

    for element in elementtos:
            
            Fuente = 'El Caribe'
            title = None
            fecha = None
            a = None
            
            try:
               title = element.find_element_by_xpath("//h3 [@class='entry-title td-module-title']").text
               herf = element.find_element_by_tag_name('a')

               if herf:
                   a = herf.get_attribute('href')
                
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
    driver.quit()


#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):
    
    elcaribe()
    
    

    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")