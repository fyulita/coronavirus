import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib.animation as anim


# %% Datos (Actualizado: 02/04/2020)

dias = np.arange(0, 28)
# El primer dia es el 05/03/2020. La cuarentena nacional empezo el 19/03/2020 y es hasta el 12/04/2020 (Extendido del
# 31/03/2020 el 29/03/2020).

casos = np.array([1, 2, 12, 17, 19, 21, 31, 34, 45, 56, 65, 79, 97, 128, 158, 225, 266, 301, 387, 502, 589, 690,
                  745, 820, 966, 1054, 1133, 1265])

casos_importados = np.array([1, 2, 12, 17, 19, 21, 28, 30, 40, 48, 56, 68, 81, 101, 123, 168, 185, 202, 243, 246, 283,
                             386, 408, 442, 485, 529, 580, 622])
casos_locales = np.array([0, 0, 0, 0, 0, 0, 0, 1, 2, 5, 6, 8, 13, 18, 22, 34, 45, 50, 70, 88, 112, 167, 185, 207, 251,
                          295, 349, 398])
casos_desconocidos = casos - casos_importados - casos_locales

muertos = np.array([0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 4, 6, 8, 12, 17, 19, 20, 24, 27, 32, 36])


# %% Ajustes


def lineal(x, m, c):
    y = m * x + c
    return y


def exponencial(x, A, b):
    y = A * np.exp(b * x)
    return y


def logistica(x, A, k, d):
    y = A / (1 + np.exp(-k * (x - d)))
    return y


# Ajustamos las funciones a los datos. El ajuste exponencial lo hacemos para los dias anteriores a la cuarentena
# obligatoria. El ajuste logistico lo hacemos para todos los dias.
param_lin, err_lin = curve_fit(lineal, dias[2:15], np.log(casos[2:15]))
param_log, err_log = curve_fit(logistica, dias[2:], casos[2:], p0=[2400, 1, 23])
param_lin_muertos, err_lin_muertos = curve_fit(lineal, dias[3:], np.log(muertos[3:]))

# Este es el error caudratico medio de los ajustes.
mse_lin = np.mean(lineal(dias[2:15], param_lin[0], param_lin[1]) - np.log(casos[2:15]))
mse_log = np.mean((logistica(dias, param_log[0], param_log[1], param_log[2]) - casos) ** 2)
mse_lin_muertos = np.mean(lineal(dias[3:], param_lin_muertos[0], param_lin_muertos[1]) - np.log(casos[3:]))


# %% Analisis

# Hacemos una lista con los casos nuevos de cada dia.
casos_nuevos = [casos[0]]
for i in range(1, len(casos)):
    casos_nuevos.append(casos[i] - casos[i - 1])
np.asarray(casos_nuevos)

# Hacemos una lista con los muertos nuevos de cada dia.
muertos_nuevos = [muertos[0]]
for i in range(1, len(muertos)):
    muertos_nuevos.append(muertos[i] - muertos[i - 1])
np.asarray(muertos_nuevos)

# Hacemos una lista que sume la cantidad de casos nuevos de los ultimos 7 dias.
casos_nuevos_semanales = [casos_nuevos[0]]
i = 1
while i < len(casos_nuevos):
    if i < 7:
        casos_nuevos_semanales.append(casos_nuevos[i] + casos_nuevos_semanales[i - 1])
        i += 1
    else:
        casos_nuevos_semanales.append(np.sum(casos_nuevos[i - 7:i + 1]))
        i += 1
np.asarray(casos_nuevos_semanales)


# %% Graficos

plt.figure("Casos Confirmados de COVID-19 en Argentina")
plt.title("Casos Confirmados de COVID-19 en Argentina")
plt.plot(dias, casos, "o", label="Casos Confirmados")
plt.plot(dias, exponencial(dias, np.exp(param_lin[1]), param_lin[0]), "-", label="Ajuste Exponencial")
plt.plot(np.arange(50), logistica(np.arange(50), param_log[0], param_log[1], param_log[2]), ":", label="Ajuste Logístico")
plt.grid()
plt.legend()
plt.xlabel("Días desde el 05/03/2020")
plt.ylabel("Casos Confirmados")
plt.savefig("Casos Confirmados de COVID-19 en Argentina.png")
plt.show()

width = 0.4
plt.figure("Casos Confirmados Importados y Locales de COVID-19 en Argentina")
plt.title("Casos Confirmados Importados y Locales de COVID-19 en Argentina")
plt.bar(dias - width / 2, casos_importados, width, label="Casos Importados")
plt.bar(dias + width / 2, casos_locales, width, label="Casos Locales")
plt.grid()
plt.legend()
plt.xlabel("Días desde el 05/03/2020")
plt.ylabel("Casos Confirmados")
plt.savefig("Casos Confirmados Importados y Locales de COVID-19 en Argentina.png")
plt.show()

plt.figure("Muertos Confirmados con COVID-19 en Argentina")
plt.title("Muertos Confirmados con COVID-19 en Argentina")
plt.plot(dias, muertos, "o", label="Muertos Confirmados")
plt.plot(dias, exponencial(dias, np.exp(param_lin_muertos[1]), param_lin_muertos[0]), "-", label="Ajuste Exponencial")
plt.grid()
plt.legend()
plt.xlabel("Días desde el 05/03/2020")
plt.ylabel("Muertos Confirmados")
plt.savefig("Muertos Confirmados con COVID-19 en Argentina.png")
plt.show()

plt.figure("Trayectoria de Casos Confirmados de COVID-19 en Argentina (Estatico)")
plt.title("Trayectoria de Casos Confirmados de COVID-19 en Argentina")
plt.loglog(casos, casos_nuevos_semanales, "-o")
plt.grid()
plt.xlabel("Casos Confirmados")
plt.ylabel("Casos Nuevos Confirmados en los Últimos 7 días")
plt.savefig("Trayectoria de Casos Confirmados de COVID-19 en Argentina.png")
plt.show()


#%% Animacion


# Creamos una figura vacia para graficar.
fig = plt.figure("Trayectoria de Casos Confirmados de COVID-19 en Argentina")
ax = plt.axes(xlim=(0, casos[-1] + 1000), ylim=(0, np.max(casos_nuevos_semanales) + 1000))
line, = plt.plot([], [], "-o")

# Le cambiamos la escala al grafico a logaritmica en ambos ejes. Usamos symlog en vez de log porque log tira error
# intentamos graficar [] ya que no tiene valor mayor que 0.
ax.set_xscale("symlog")
ax.set_yscale("symlog")

# Creamos listas donde se van a guardar los datos de x e y a medida que se van graficando.
xdata, ydata = [], []


# Esta funcion se va a usar para empezar a graficar y no grafica nada.
def init():
    line.set_data([], [])
    return line,


# Esta funcion se va a usar para graficar cada punto.
def animate(i):
    x = casos[i]
    y = casos_nuevos_semanales[i]

    xdata.append(x)
    ydata.append(y)

    line.set_data(xdata, ydata)
    return line,


# Le agregamos detalles al grafico.
plt.title("Trayectoria de Casos Confirmados de COVID-19 en Argentina")
plt.grid()
plt.xlabel("Casos Confirmados")
plt.ylabel("Casos Nuevos Confirmados en los Últimos 7 días")

# Usamos la funcion FuncAnimation, que va a llamar la funcion animate que creamos para graficar cada punto.
animacion = anim.FuncAnimation(fig, animate, init_func=init, frames=len(casos), blit=True)

# Guardamos la animacion como .gif o como .mp4
animacion.save("Trayectoria de Casos Confirmados de COVID-19 en Argentina.gif", writer="imagemagick")
# animacion.save("Trayectoria de Casos Confirmados de COVID-19 en Argentina.mp4")

# Este plt.show() es necesario porque si corres el programa varias veces se empiezan a sobreponer los graficos.
plt.show()
