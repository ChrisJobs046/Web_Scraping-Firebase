from typing import NewType
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



def P_ElCaribe(website = 'https://www.elcaribe.com.do/2021/01/01/page/1/'):

    datos = []

    PATH = os.getenv('W_PATH') 


    with  webdriver.Chrome(PATH) as driver:
        driver.get(website)

        time.sleep(5)

        main(driver, datos)
        paginacion(driver, datos)

        UpdateCaribe(datos)
        # Borrar cookies del navegador
        cookies = driver.get_cookies()
        print(f"main: cookies = {cookies}")
        driver.delete_all_cookies()

        driver.quit()
        return datos

    


def main(driver, datos):

    # datos = []

    PATH = os.getenv('W_PATH')

    element1 = driver.find_elements_by_class_name("item-details")
    elementtos = element1

    for element in elementtos:
            
            Fuente = 'El Caribe'
            title = None
            fecha = None
            a = None
            desc = None
            desc2 = None

            try:
               herf = element.find_element_by_tag_name('a')
               if herf:
                   a = herf.get_attribute('href')
               with webdriver.Chrome(PATH) as window:
                        window.get(a)

                        desc = window.find_element_by_class_name('td-post-content.td-pb-padding-side')
                        # desc = window.find_element_by_class_name("td-ss-main-content")


                        desc2 = desc.get_attribute('p')
                        # desc2 = desc.find_element_by_tag_name('p').text

                        if desc2 == '' or desc2 == None:
                            desc2 = desc.find_element(By.TAG_NAME, 'p').text

                            print(desc2)

                        # desc2 = desc.find_elements(By.TAG_NAME, 'p')

                        # # desc3 = desc.find_element(By.CSS_SELECTOR, "p").text

                        # desc5 = desc.find_element_by_tag_name('p')
                        # print(desc5.text)

                        # print(desc4)

                        # for e in desc2:
                        #     print(e.text)


                        window.close()

            except Exception as e:
                print(e)
                break

            try:
                title= element.find_element_by_tag_name('a') 
                if title:
                    title = title.get_attribute('title')  
            except Exception:
                    pass

            try:
                fecha= element.find_element_by_tag_name('time')
                if fecha:
                    fecha = fecha.get_attribute('datetime') 
                    fecha = fecha[8:10]+'/'+fecha[5:7]+'/'+fecha[0:4]
            except Exception:
                    pass

            dic = dict(title= title, href=a, descripcion = desc2, fuente = Fuente, fecha = fecha )
            print(dic)
            if dic['descripcion'] == '':
                    dic['descripcion'] = 'No hay descripcion o  contiene un video'
            if dic['title'] != '':
                datos.append(dic)
            # del driver
            # gc.collect()
    # driver.quit()
    return datos
    


def paginacion(driver, datos):
    
    
    pageN = [1,2,3,4,5]
    top = 0
    while True:
        try:
            next_page = driver.find_element_by_xpath("//div[@class='page-nav td-pb-padding-side']").find_elements_by_tag_name("a")
            current = driver.find_element_by_xpath("//div[@class='page-nav td-pb-padding-side']").find_element_by_class_name("current")
            link = next_page[-1].get_attribute('href') 
            top = next_page[-1].get_attribute('title')
            if top and current.text:
                if int(current.text) > int(top):
                    break
            driver.get(link)
            time.sleep(5)
            main(driver, datos)
        except Exception as e:
            print(e)
            break


# def Modified(driver, datos):
#     fecha = []

FIREBASE = os.getenv('F_EndPoint')

F_EndPoint = 'https://pythonfirebase-d51e6-default-rtdb.firebaseio.com/'



# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(F_EndPoint, None)

def UpdateCaribe(datos):
    
    try:
        Caribe = firebase.get('/Monitoreo/El Caribe', None)
        arr = list(zip(Caribe.keys(), Caribe.values()))
        for item in arr:
            for i in range(len(item[1])):
                if len(item[1]) < i and item[1][i]['title'] == datos[i]['title']:
                    # update = firebase.put(f'/Monitoreo/El Caribe/', f'{item[0]}/{i}', datos[i])
                    updatebyID = firebase.patch(f'/Monitoreo/El Caribe/', f'{item[0]}/{i}', datos[i])
                    
                    print(updatebyID)
                break
                
        # for i in range(len(arr[1])):
        #     for k in arr[1][i]:
        #         key = arr[0][i]
        #         for j in range(len(datos)):
        #             print(key,j)
        #             if k[j]['title'] == datos[j]['title']:
        #                 try:
        #                     print(key,j)
        #                     # update = firebase.put(f'/Monitoreo/El Caribe/', j, datos[j])
        #                     # print(update)
        #                     pass
        #                 except Exception as e:
        #                     print(e)
        #                     pass
                        
                        
        #                 break
    except Exception as e:
        print(e)
        pass


for i in range(1, 2):
    
    website = f'https://www.elcaribe.com.do/2021/01/{i}/'
    # Periodico2(website)
    
    P_datos = P_ElCaribe(website)
    result = firebase.post('/Monitoreo/El Caribe', P_datos)
    print(result)

    

#-------------------------------Actualizador automatico---------------------------------------
timeout = 0 # Segundos
s = sched.scheduler(time.time, time.sleep)

def do_something(sc):

    
    # P_ElCaribe()
    timeout = 3600
    s.enter(timeout, 1, do_something, (sc,))


s.enter(timeout, 1, do_something, (s,))
s.run()



print("------------------------------------------SE ACTUALIZA---------------------------------------------------------------------")