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

def eldia():

    datos2 = []

    PATH = os.getenv('W_PATH')

    website = 'https://eldia.com.do/'

    driver = webdriver.Chrome(PATH)

    driver.get(website)

    lst=[]
    elements1 = driver.find_elements_by_xpath("//div [@class='td-block-span12']")
    elements2 = driver.find_elements_by_xpath("//div [@class='item-details']")
    elements = elements1


    for t in elements:

        lst.append([t.text])
        ti= None
        a = None
        f= None
        try:
            tittle = t.find_element_by_tag_name('a')
            if tittle:
                    ti = tittle.get_attribute('title')
        except Exception:
                pass
        try:
            herf = t.find_element_by_tag_name('a')
            if herf:
                    a = herf.get_attribute('href')
        except Exception:
                pass
        try:
            fecha= t.find_element_by_tag_name('time')
            if fecha:
                f = fecha.get_attribute('datetime')
        except Exception:
                pass
        
        dic = dict(title= ti, href=a, fuente='El Dia', fecha =f )
        print(dic)
        datos2.append(dic)
        
    driver.quit()
    return datos2 