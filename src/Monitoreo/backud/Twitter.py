from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import time
import sched
from firebase import firebase
from dotenv import load_dotenv
import os,gc

load_dotenv()

def scarp():
    x= input("de que fecha desea buscar: ")
    website = 'http://www.trendinalia.com/twitter-trending-topics/republicadominicana/republicadominicana-{0}.html'.format(x)
    PATH = os.getenv('W_PATH')

    
    driver = webdriver.Chrome(PATH)
    driver.get(website)
    time.sleep(5)
    lst=[]
    fnl = []
    elements1 = driver.find_elements_by_xpath("//div [@align='left'] ")
    elements = elements1[0:10]
    for t in elements:
        lst.append([t.text])
        ti= None
        a = None
        f= None
        try:
            tittle = t.find_element_by_tag_name('a')    
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
        dic =  dict(title= ti, href=a, fecha='21/09/21')
        # dic2= dict(title= ti)
        # list = dic2.values()
        fnl.append(dic)
        print(fnl)

    return fnl


FIREBASE = os.getenv('F_EndPoint')



firebase = firebase.FirebaseApplication(FIREBASE, None)
# c = twint.Config()

# def Twitter_firebase():

Twitter = scarp()

# esta parte esta hecha por mi
result = firebase.post('/TwitterPrueba', Twitter)
print(result)