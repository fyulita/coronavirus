from scipy.optimize import curve_fit
from datos import *


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
if pais == "Argentina":
    param_lin, err_lin = curve_fit(lineal, dias[3:dia_de_cuarentena + 1], np.log(infectados[3:dia_de_cuarentena + 1]))
    param_log, err_log = curve_fit(logistica, dias, infectados, p0=[2400, 1, 23])
elif pais == "Paraguay":
    param_lin, err_lin = curve_fit(lineal, dias, np.log(infectados))
    param_log, err_log = curve_fit(logistica, dias, infectados, p0=[200, 1, 28])
param_lin_muertos, err_lin_muertos = curve_fit(lineal, dias[primer_muerto:], np.log(muertos[primer_muerto:]))

# Este es el error caudratico medio de los ajustes.
mse_lin = np.mean(lineal(dias[:dia_de_cuarentena], param_lin[0], param_lin[1]) -
                  np.log(infectados[:dia_de_cuarentena]) ** 2)
mse_log = np.mean((logistica(dias, param_log[0], param_log[1], param_log[2]) - infectados) ** 2)
mse_lin_muertos = np.mean(lineal(dias[primer_muerto:], param_lin_muertos[0], param_lin_muertos[1]) -
                          np.log(infectados[primer_muerto:]) ** 2)


# %% Analisis

# Hacemos una lista con los casos nuevos de cada dia.
infectados_nuevos = [infectados[0]]
for i in range(1, len(infectados)):
    infectados_nuevos.append(infectados[i] - infectados[i - 1])

# Hacemos una lista con los muertos nuevos de cada dia.
muertos_nuevos = [muertos[0]]
for i in range(1, len(muertos)):
    muertos_nuevos.append(muertos[i] - muertos[i - 1])

# Hacemos una lista que sume la cantidad de casos nuevos de los ultimos 7 dias.
infectados_nuevos_semanales = [infectados_nuevos[0]]
i = 1
while i < len(infectados_nuevos):
    if i < 7:
        infectados_nuevos_semanales.append(infectados_nuevos[i] + infectados_nuevos_semanales[i - 1])
        i += 1
    else:
        infectados_nuevos_semanales.append(np.sum(infectados_nuevos[i - 7:i + 1]))
        i += 1
