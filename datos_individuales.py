import numpy as np


pais = "Chile"
datos = np.genfromtxt("{}/Datos.csv".format(pais), delimiter=",")

infectados = datos[1:, 1]
dias = np.arange(len(infectados))
muertos = datos[1:, 2]

if pais == "Argentina":
    primer_dia = "05/03/2020"
    dia_de_cuarentena = 14
    infectados_importados = datos[1:, 3]
    infectados_estrechos = datos[1:, 4]
elif pais == "Paraguay":
    primer_dia = "07/03/2020"
    dia_de_cuarentena = 3
    muertos = datos[1:, 2]
    recuperados = datos[1:, 3]
elif pais == "Brasil":
    primer_dia = "26/02/2020"
elif pais == "Chile":
    primer_dia = "03/03/2020"

i = 0
while i < len(muertos) and muertos[i] == 0:
    i += 1

primer_muerto = i + 1
