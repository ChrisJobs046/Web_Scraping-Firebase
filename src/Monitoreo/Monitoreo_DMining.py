import pandas as pd
import os
from dotenv import load_dotenv
from openpyxl import Workbook
import numpy as np
import collections
import matplotlib as mpl
import matplotlib.pyplot as plt



load_dotenv()


Ruta_M = os.getenv('Ruta_M')

Ruta_p = os.getenv('Ruta_Periodicos')

ruta_definitiva = os.getenv('Ruta_D')

rd = pd.read_excel(io = ruta_definitiva)

df = pd.read_excel(io = Ruta_M)

dp = pd.read_excel(io = Ruta_p)

# df.info()

# print(df)

# def Mineria():

#     for num in df:
#         if len(df.count(num)) > 1:
#             return num
#     print(num)

# set([num for num in df if df.count(num) > 1])

# df.info()

# df = df.dropna(subset=['item'])

# df["item"].value_counts().nlargest(n=1).values[0]

# df['keys'].value_counts().max()

# df['item'].value_counts().idxmax()


# se supone que value_counts sirve para enumerar los valores que se repiten
# repetido = df['title'].value_counts()

# for num in df['title']:
#     num 

# repetido1 = df['title'].value_counts()

# df.to_numpy()

# df.numpy.unique(df,return_counts = True)

# print(repetido)

# print(repetido)
# print(repetido1)


# frecuencia = df.groupby(['title']).count()

# print(frecuencia)

n = 9

C_Derechos = [

    'violencia', 
    'agresion', 
    'golpear', 
    'maltrato', 
    'educacion', 
    'libertad', 
    'discriminación', 
    'integridad', 
    'vida',
    'seguridad',
    'protección '
    ]

# for num in C_Derechos:
#     req =  rd[rd['title'].str.contains(num)]['title']

#     # print(req)

# freq = rd['title'].value_counts()[:n]

# print(freq)


# freq = rd[['title']].value_counts()[:n]

# print(freq)

# nmp = rd.to_numpy()

# print(nmp)


# for i in range(len(rd)):
#     print(rd) 


#pandas.DataFrame.iterrows() devuelve el índice de la fila y todos los datos de la fila como una Series. 
# Por lo tanto, podríamos usar esta función para iterar sobre filas en Pandas DataFrame.

# for index, row in rd.iterrows():
#     (row['title']).value_counts
#     print(row) 

# C = rd['title'].value_counts()[:n]

A = rd[['title']].value_counts()[:n]
# print(A)

for data in A.index:
    # print(data[0])
    C_calculos = rd[rd['title'] == data[0]][['title','clasificados']]
    pedro = pd.DataFrame(C_calculos)
    f=C_calculos.append(C_calculos , ignore_index=True)
    print(C_calculos)

# pedro = pd.DataFrame(C_calculos)

# Ruta_excel = os.getenv('Ruta')

f.to_excel('D:/Defensoria del pueblo/Web_Scraping&Firebase/assets/WebScraping12.xlsx', sheet_name='WebScraping')

# freq2 = dp['title'].value_counts
# print(freq2)

# frecuencia = pd.DataFrame(freq)

# frecuencia.to_excel('D:/Defensoria del pueblo/Web_Scraping&Firebase/assets/TrendingTopic.xlsx', sheet_name='WebScraping')

# juan = pd.read_excel(io = ruta_definitiva)

# n = 10
# joel = juan['title'].value_counts()[:n].to_dict()

# print(joel)