import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim


#%% Datos
datos = np.genfromtxt("Sudamerica/Datos.csv", delimiter=",")

infectados_arg = datos[1:, 1]
muertos_arg = datos[1:, 2]
infectados_py = datos[1:, 3]
muertos_py = datos[1:, 4]
infectados_br = datos[1:, 5]
muertos_br = datos[1:, 6]
infectados_ch = datos[1:, 7]
muertos_ch = datos[1:, 8]

infectados = [infectados_arg, infectados_py, infectados_br, infectados_ch]
muertos = [muertos_arg, muertos_py, muertos_br, muertos_ch]
paises = ["Argentina", "Paraguay", "Brasil", "Chile"]

dias = np.arange(len(infectados_arg))


#%% Analisis

# Hacemos una lista con los casos nuevos de cada dia.
infectados_nuevos = [[infectados_arg[0]], [infectados_py[0]], [infectados_br[0]], [infectados_ch[0]]]
for i in range(0, np.shape(infectados)[0]):
    for j in range(1, np.shape(infectados)[1]):
        infectados_nuevos[i].append(infectados[i][j] - infectados[i][j - 1])

# Hacemos una lista que sume la cantidad de casos nuevos de los ultimos 7 dias.
infectados_nuevos_semanales = [[infectados_nuevos[0][0]], [infectados_nuevos[1][0]], [infectados_nuevos[2][0]],
                               [infectados_nuevos[3][0]]]
for i in range(0, np.shape(infectados_nuevos)[0]):
    j = 1
    while j < len(infectados_nuevos[i]):
        if j < 7:
            infectados_nuevos_semanales[i].append(infectados_nuevos[i][j] + infectados_nuevos_semanales[i][j - 1])
            j += 1
        else:
            infectados_nuevos_semanales[i].append(np.sum(infectados_nuevos[i][j - 7:j + 1]))
            j += 1


#%% Graficos


def graficar_infectados():
    plt.figure("Casos Confirmados de COVID-19 en Sudamerica")
    plt.title("Casos Confirmados de COVID-19 en Sudamérica")
    for i in range(0, np.shape(infectados)[0]):
        plt.plot(dias, infectados[i], "o", label="{}".format(paises[i]))
    plt.grid()
    plt.legend()
    plt.xlabel("Días desde el 26/02/2020")
    plt.ylabel("Casos Confirmados")
    plt.savefig("Sudamerica/Casos-Confirmados-de-COVID-19-en-Sudamerica.png")
    plt.show()


def graficar_muertos():
    plt.figure("Muertos Confirmados con COVID-19 en Sudamerica")
    plt.title("Muertos Confirmados con COVID-19 en Sudamérica")
    for i in range(0, np.shape(muertos)[0]):
        plt.plot(dias, muertos[i], "o", label="{}".format(paises[i]))
    plt.grid()
    plt.legend()
    plt.xlabel("Días desde el 26/02/2020")
    plt.ylabel("Muertos Confirmados")
    plt.savefig("Sudamerica/Muertos-Confirmados-de-COVID-19-en-Sudamerica.png")
    plt.show()


def graficar_trayectorias():
    plt.figure("Trayectorias de Casos Confirmados de COVID-19 en Sudamerica (Estatico)")
    plt.title("Trayectorias de Casos Confirmados de COVID-19 en Sudamérica")
    for i in range(0, np.shape(infectados)[0]):
        plt.loglog(infectados[i], infectados_nuevos_semanales[i], "-o", label="{}".format(paises[i]))
    plt.grid()
    plt.legend()
    plt.xlabel("Casos Confirmados")
    plt.ylabel("Casos Nuevos Confirmados en los Últimos 7 días")
    plt.savefig("Sudamerica/Trayectorias-de-Casos-Confirmados-de-COVID-19-en-Sudamerica.png")
    plt.show()
