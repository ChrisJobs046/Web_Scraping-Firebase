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

def Hoy():
        
    datos1 = []

    website = 'https://hoy.com.do/secciones/el-pais/'

    PATH = os.getenv('W_PATH')

    driver = webdriver.Chrome(PATH)

    driver.get(website)

    lst=[]
    elements1 = driver.find_elements_by_xpath("//div [@class='post-content']")
    elements = elements1

    for t in elements:
        lst.append([t.text])
        ti= None
        a = None
        f= None
        try:
            tittle = t.find_element_by_tag_name('h3')
            if tittle:
                    ti = tittle.text
        except Exception:
                pass
        try:
            herf = t.find_element_by_tag_name('a')
            if herf:
                    a = herf.get_attribute('href')
        except Exception:
                pass
        try:
            fecha= t.find_element_by_tag_name('span')
            if fecha:
                f = fecha.text
        except Exception:
                pass
        
        dic = dict(title= ti, href=a, fuente='Hoy', fecha =f )
        datos1.append(dic)
        print(dic)
        
        
    driver.quit()
    return datos1 
