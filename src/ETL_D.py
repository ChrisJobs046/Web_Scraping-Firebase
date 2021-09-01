from typing import Dict
import pandas as pd
from seaborn import load_dataset
from firebase import firebase
import os
from dotenv import load_dotenv
from openpyxl import Workbook

load_dotenv()


FIREBASE = os.getenv('F_EndPoint')


F_Periodico = os.getenv('F_Periodio_General')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)

resultFinal = firebase.get(F_Periodico, None)

print(resultFinal[list(resultFinal.keys())[0]].keys())

periodicos = dict(
    title=[],
    fecha=[],
    fuente=[],
    href=[],
)

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

# Ruta_excel = os.getenv('Ruta')

# pedro.to_excel(Ruta_excel, sheet_name='WebScraping')