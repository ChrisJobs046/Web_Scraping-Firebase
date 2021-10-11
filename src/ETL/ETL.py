from typing import Dict
import pandas as pd
from seaborn import load_dataset
from firebase import firebase
import os
from dotenv import load_dotenv
from openpyxl import Workbook

load_dotenv()

FIREBASE = os.getenv('F_EndPoint')
# Endpoint del diariolibre
Diario = os.getenv('DiarioLibre1')
Diario1 = os.getenv('DiarioLibre2')
Diario2 = os.getenv('DiarioLibre3')
Diario3 = os.getenv('DiarioLibre4')
Diario4 = os.getenv('DiarioLibre5')

# Endpoint del periodico el dia
ElDia1 = os.getenv('PeriodicoDia1')
ElDia2 = os.getenv('PeriodicoDia2')
ElDia3 = os.getenv('PeriodicoDia3')

# Endpoint del periodico hoy
Hoy1 = os.getenv('PeriodicoHoy1')
Hoy2 = os.getenv('PeriodicoHoy2')
Hoy3 = os.getenv('PeriodicoHoy3')
Hoy4 = os.getenv('PeriodicoHoy4')
Hoy5 = os.getenv('PeriodicoHoy5')

# Endpoint del periodico el dia
Listin1 = os.getenv('ListinDiario1')
Listin2 = os.getenv('ListinDiario2')
Listin3 = os.getenv('ListinDiario3')
Listin4 = os.getenv('ListinDiario4')
Listin5 = os.getenv('ListinDiario5')

F_Periodico = os.getenv('F_Periodio_General')

# esta parte esta hecha por mi
firebase = firebase.FirebaseApplication(FIREBASE, None)


result = firebase.get(Diario, None) + firebase.get(Diario1, None) + firebase.get(Diario2, None) + firebase.get(Diario3, None) + firebase.get(Diario4, None)
result1 = firebase.get(ElDia1, None) + firebase.get(ElDia2, None) + firebase.get(ElDia3, None)
result2 = firebase.get(Hoy1, None) + firebase.get(Hoy2, None) + firebase.get(Hoy3, None) + firebase.get(Hoy4, None) + firebase.get(Hoy5, None)
result3 = firebase.get(Listin1, None) + firebase.get(Listin2, None) + firebase.get(Listin3, None) + firebase.get(Listin4, None) + firebase.get(Listin5, None)
resultFinal = result + result1 + result2 + result3
# for item in result:
#     print(item["href"])

periodicos = dict(
    title=[],
    fecha=[],
    fuente=[],
    href=[],
)

keys = [key for key in periodicos.keys()]
for s in resultFinal:
    for key in keys:
        try:
            periodicos[key].append(s[key])
        except KeyError:
            periodicos[key].append("N/A")

pedro = pd.DataFrame(periodicos)

print(pedro)
# pedro = pd.DataFrame(periodico, columns=['Periodico'])


#si quito el parametro de la columna me imprime los datos en una sola fila
#antes me daba un error porque no estaba encasulando los datos de firebasse en un arreglo

Ruta_excel = os.getenv('Ruta')

pedro.to_excel('D:/Defensoria del pueblo/Web_Scraping&Firebase/assets/WebScraping.xlsx', sheet_name='WebScraping')
