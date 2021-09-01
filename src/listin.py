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

load_dotenv()

def listindiario():

    datos3 = []

    website = 'https://listindiario.com'

    PATH = os.getenv('W_PATH')

    driver = webdriver.Chrome(PATH)

    driver.get(website)

    time.sleep(5)
 
    elements1 = driver.find_elements_by_xpath("//div [@class='topcentermain_titulo']")
    elements2 = driver.find_elements_by_xpath("//div [@class='topleftmain_titulo']")
    
    fehcha = driver.find_element_by_xpath("//span [@style='text-transform:lowercase; color:#333333; font-weight:bold;']").text
    elements = elements1+elements2
  
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
        print(dic)
        datos3.append(dic)
        
    
    driver.quit()
    return datos3 