import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_hist_ran(nums, output, i):
    plt.hist(nums, bins=50, density=True, edgecolor="black")
    plt.title("Distribución de números generados por ran1")
    plt.xlabel("Valor")
    plt.ylabel("Frecuencia normalizada")
    folder = os.path.join(output, "RanNumHist", str(len(nums)))
    os.makedirs(folder, exist_ok=True)
    output = os.path.join(folder, "RanNumHist_" + str(len(nums)) + "_" + str(i) + ".png")
    plt.savefig(output)
    plt.show()

def plot_variance(file):
    df = pd.read_csv(file)
    os.makedirs("Outputs", exist_ok=True)
    output = os.path.join("Outputs", "plot_varianza.png")
    # Gráfico log-log
    plt.loglog(df["N"], df["std_pi"], 'o-', label=r"Valor calculado")
    plt.loglog(df["N"], 0.05/np.sqrt(df["N"]), '--', label="~1/sqrt(N)")
    plt.xlabel("N")
    plt.ylabel("Desviación estándar de π")
    plt.title("Varianza y varianza esperada respecto a N")
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.savefig(output)
    plt.show()
