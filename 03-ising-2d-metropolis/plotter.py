import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# ---------------------------------------------------------
# 1. Energía/espín vs Temperatura
# ---------------------------------------------------------
def plot_energia(T, e):
    plt.figure(figsize=(6,4))
    plt.plot(T, e, 'r.', markersize=4)
    plt.xlabel("Temperatura")
    plt.ylabel("Energía por espín")
    plt.title("Energía/espín vs Temperatura")
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# 2. Calor específico vs Temperatura
# ---------------------------------------------------------
def plot_calor(T, Cv):
    plt.figure(figsize=(6,4))
    plt.plot(T, Cv, 'r.', markersize=4)
    plt.xlabel("Temperatura")
    plt.ylabel("C_V")
    plt.title("Calor específico vs Temperatura")
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# 3. Magnetización vs Temperatura
# ---------------------------------------------------------
def plot_magnetizacion(T, m):
    plt.figure(figsize=(6,4))
    plt.plot(T, m, 'r.', markersize=4)
    plt.xlabel("Temperatura")
    plt.ylabel("Magnetización por espín")
    plt.title("Magnetización vs Temperatura")
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------
# 4. Susceptibilidad vs Temperatura
# ---------------------------------------------------------
def plot_susceptibilidad(T, chi):
    plt.figure(figsize=(6,4))
    plt.plot(T, chi, 'r.', markersize=4)
    plt.xlabel("Temperatura")
    plt.ylabel("Susceptibilidad")
    plt.title("Susceptibilidad vs Temperatura")
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))
    plt.tight_layout()
    plt.show()
