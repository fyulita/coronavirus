import matplotlib.pyplot as plt
import matplotlib.animation as anim
from analisis import *


# %% Graficos


def graficar_infectados(exp=False, log=False):
    plt.figure("Casos Confirmados de COVID-19 en {}".format(pais))
    plt.title("Casos Confirmados de COVID-19 en {}".format(pais))
    plt.plot(dias, infectados, "o", label="Casos Confirmados")
    if exp:
        plt.plot(dias, exponencial(dias, np.exp(param_lin[1]), param_lin[0]), "-", label="Ajuste Exponencial")
    if log:
        plt.plot(np.arange(50), logistica(np.arange(50), param_log[0], param_log[1], param_log[2]), ":",
                 label="Ajuste Logístico")
    plt.grid()
    if exp or log:
        plt.legend()
    plt.xlabel("Días desde el {}".format(primer_dia))
    plt.ylabel("Casos Confirmados")
    plt.savefig("{}/Casos-Confirmados-de-COVID-19-en-{}.png".format(pais, pais))
    plt.show()


def graficar_origen_infectados():
    width = 0.4
    plt.figure("Origen de Casos Confirmados de COVID-19 en {}".format(pais))
    plt.title("Origen de Casos Confirmados de COVID-19 en {}".format(pais))
    plt.bar(dias - width / 2, infectados_importados, width, label="Casos Importados")
    plt.bar(dias + width / 2, infectados_estrechos, width, label="Casos Locales")
    plt.grid()
    plt.legend()
    plt.xlabel("Días desde el {}".format(primer_dia))
    plt.ylabel("Casos Confirmados")
    plt.savefig("{}/Origen-de-Casos-Confirmados-de-COVID-19-en-{}.png".format(pais, pais))
    plt.show()


def graficar_muertos(exp=False):
    plt.figure("Muertos Confirmados con COVID-19 en {}".format(pais))
    plt.title("Muertos Confirmados con COVID-19 en {}".format(pais))
    plt.plot(dias, muertos, "o", label="Muertos Confirmados")
    if exp:
        plt.plot(dias, exponencial(dias, np.exp(param_lin_muertos[1]), param_lin_muertos[0]), "-",
                 label="Ajuste Exponencial")
    plt.grid()
    if exp:
        plt.legend()
    plt.xlabel("Días desde el {}".format(primer_dia))
    plt.ylabel("Muertos Confirmados")
    plt.savefig("{}/Muertos-Confirmados-con-COVID-19-en-{}.png".format(pais, pais))
    plt.show()


def graficar_trayectoria():
    plt.figure("Trayectoria de Casos Confirmados de COVID-19 en {} (Estatico)".format(pais))
    plt.title("Trayectoria de Casos Confirmados de COVID-19 en {}".format(pais))
    plt.loglog(infectados, infectados_nuevos_semanales, "-o")
    plt.grid()
    plt.xlabel("Casos Confirmados")
    plt.ylabel("Casos Nuevos Confirmados en los Últimos 7 días")
    plt.savefig("{}/Trayectoria-de-Casos-Confirmados-de-COVID-19-en-{}.png".format(pais, pais))
    plt.show()


def graficar_recuperados():
    plt.figure("Recuperados Confirmados de COVID-19 en {}".format(pais))
    plt.title("Recuperados Confirmados de COVID-19 en {}".format(pais))
    plt.plot(dias, recuperados, "o", label="Recuperados")
    plt.grid()
    plt.xlabel("Días desde el {}".format(primer_dia))
    plt.ylabel("Recuperados")
    plt.savefig("{}/Recuperados-Confirmados-de-COVID-19-en-{}.png".format(pais, pais))
    plt.show()


# %% Animacion


def hacer_animacion():
    # Creamos una figura vacia para graficar.
    fig = plt.figure("Trayectoria de Casos Confirmados de COVID-19 en {}".format(pais))
    ax = plt.axes(xlim=(0, infectados[-1]), ylim=(0, np.max(infectados_nuevos_semanales)))
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
        x = infectados[i]
        y = infectados_nuevos_semanales[i]

        xdata.append(x)
        ydata.append(y)

        line.set_data(xdata, ydata)
        return line,

    # Le agregamos detalles al grafico.
    plt.title("Trayectoria de Casos Confirmados de COVID-19 en {}".format(pais))
    plt.grid()
    plt.xlabel("Casos Confirmados")
    plt.ylabel("Casos Nuevos Confirmados en los Últimos 7 días")

    # Usamos la funcion FuncAnimation, que va a llamar la funcion animate que creamos para graficar cada punto.
    animacion = anim.FuncAnimation(fig, animate, init_func=init, frames=len(infectados), blit=True)

    # Guardamos la animacion como .gif o como .mp4
    animacion.save("{}/Trayectoria-de-Casos-Confirmados-de-COVID-19-en-{}.gif".format(pais, pais), writer="imagemagick")
    # animacion.save("{}/Trayectoria-de-Casos-Confirmados-de-COVID-19-en-{}.mp4".format(pais, pais))

    # Este plt.show() es necesario porque si corres el programa varias veces se empiezan a sobreponer los graficos.
    plt.show()
