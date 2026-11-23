import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = {
    "N": [1e4, 1e5, 1e6, 1e7],
    "Err_Unif": [5.74e-4, 1.35e-4, 4.80e-5, 2.19e-5],
    "Err_NoUnif_yparcial": [5.55e-3, 5.53e-3, 5.48e-3, 5.48e-3],
    "Err_NoUnif_ycompleto": [8.01e-5, 1.43e-5, 3.30e-6, 4.35e-7],
}

df = pd.DataFrame(data)
df["1/sqrt(N)"] = 1 / np.sqrt(df["N"])


plt.figure(figsize=(7,5))
plt.loglog(df["N"], df["Err_Unif"], "o-", label="Uniforme")
plt.loglog(df["N"], df["Err_NoUnif_yparcial"], "s-", label="No-Uni [ρ(L),ρ(0)]")
plt.loglog(df["N"], df["Err_NoUnif_ycompleto"], "^-", label="No-Uni [0,ρmax]")
plt.loglog(df["N"], df["1/sqrt(N)"], "--", color="gray", label="1/√N (teórico)")


plt.xlabel("N")
plt.ylabel("Err abs |I_est - I_exact|")
plt.title("Variación del error con N Integración Monte Carlo")
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.tight_layout()
os.makedirs("Outputs", exist_ok=True)
plt.savefig(os.path.join("Outputs", "comparacion_Errores.png"))
#plt.show()

# Rango de x
x = np.linspace(0, 0.8, 500)

# Funciones
f1 = np.cos(np.pi * x / 2)
f2 = 1 - x**2
f3 = np.ones_like(x)

plt.figure(figsize=(8, 5))
plt.plot(x, f1, label=r'$\cos(\pi x / 2)$', linewidth=2)
plt.plot(x, f2, label=r'$\rho_{\text{no uniforme}}$', linewidth=2)
plt.plot(x, f3, label=r'$p_{\text{uniforme}}$', linewidth=2, linestyle='--', color='gray')


plt.title('Coseno y distribuciones')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join("Outputs", "comparacion_funciones.png"))


plt.show()
