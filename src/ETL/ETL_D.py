from typing import Dict
import pandas as pd
from seaborn import load_dataset
from firebase import firebase
import os
from dotenv import load_dotenv
from openpyxl import Workbook

load_dotenv()


FIREBASE = os.getenv('F_EndPoint')


# F_Periodico = os.getenv('F_Periodico_General')
F_Periodico2 = os.getenv('F_Periodico_General2')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)

resultFinal = firebase.get(F_Periodico2, None)

# print(resultFinal[list(resultFinal.keys())[0]].keys())

periodicos = dict(
    title=[],
    fecha=[],
    fuente=[],
    href=[],
    clasificados=[],
)

news_papers = []
for key in resultFinal.keys():
    for key2 in resultFinal[key]:
        news_papers += resultFinal[key][key2]
# print(news_papers)


keys = [key for key in periodicos.keys()]
for s in news_papers:
    for key in keys:
        try:
            periodicos[key].append(s[key])
        except KeyError:
            periodicos[key].append("N/A")

pedro = pd.DataFrame(periodicos)

print(pedro)


# keys = [key for key in periodicos.keys()]
# for s in resultFinal:
#     for key in keys:
#         try:
#             periodicos[key].append(s[key])
#         except KeyError:
#             periodicos[key].append("N/A")

# pedro = pd.DataFrame(periodicos)

# print(pedro)
# pedro = pd.DataFrame(periodico, columns=['Periodico'])


#si quito el parametro de la columna me imprime los datos en una sola fila
#antes me daba un error porque no estaba encasulando los datos de firebasse en un arreglo

# Visualización del uso de memoria
# df.info()

# A partir de pandas 0.17.1, también puede hacer df.info(memory_usage='deep')para ver el uso de la memoria, incluidos los objetos.



Ruta_excel = os.getenv('Ruta')

pedro.to_excel('D:/Defensoria del pueblo/Web_Scraping&Firebase/assets/WebScrapingXX.xlsx', sheet_name='WebScraping')