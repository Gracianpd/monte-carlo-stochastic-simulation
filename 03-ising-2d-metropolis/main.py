# ising.py  --- Modelo de Ising 2D con Metrópolis y argumentos por CLI
from soporte import *
from plotter import *
import argparse
import numpy as np
import time


# -----------------------------
#   MAIN
# -----------------------------

def main():
    parser = argparse.ArgumentParser(description="Simulación Monte Carlo de Ising 2D")

    parser.add_argument("--nfilas", type=int, required=True)
    parser.add_argument("--ncolum", type=int, required=True)
    parser.add_argument("--npasos", type=int, required=True)
    parser.add_argument("--nequil", type=int, required=True)
    parser.add_argument("--J", type=float, default=1.0)
    parser.add_argument("--kB", type=float, default=1.0)


    args = parser.parse_args()

    state = {"x": -int(time.time())}

    #valores basicos
    N = args.nfilas * args.ncolum
    temps = np.linspace(0.2, 5, 200)
    #arrays para guardar datos
    T_vals = []
    E_vals = []
    Cv_vals = []
    M_vals = []
    Chi_vals = []

    for temp in temps:
        print(f"Calculo de una red Ising en 2D con MC, T = {temp}")

        # cte termalizacion
        #bloque = 200
        #E_bloq_prev = None
        #E_bloq_acc = 0.0
        #contador_en_bloques = 0
        #terma = False

        beta = 1.0 / (args.kB * temp)

        # Acumuladores
        contador = 0
        ener_sum = 0.0
        ener2_sum = 0.0
        magne_abs_sum = 0.0
        magne_sum = 0.0
        magne2_sum = 0.0

        # Configuración inicial tipo damas
        A = tablero_damas(args.nfilas, args.ncolum)
        #A = todos_arriba(args.nfilas, args.ncolum)
        #calculo de energia inicial. despues solamente se sumara la diferencia entre microestados
        E = energia_total(A, args.J)
        M = magnetizacion(A)

        # Bucle Monte Carlo
        for imc in range(args.npasos):
            # sweep metropolis
            dE, dM = metropolis_sweep(A, beta, args.J, state)
            E += dE
            M += dM            # energia instantanea
            #E_inst = energia_total(A, args.J) / N

            #if not terma:
             #   E_bloq_acc += E_inst
              #  contador_en_bloques += 1

               # if contador_en_bloques == bloque:
                #    E_bloq_curr = E_bloq_acc / bloque

              #      if check_thermalization(E_bloq_prev, E_bloq_curr, eps=0.01):
               #         print(f" Sistema termalizado en paso {imc}")
                #        terma = True
                 #   else:
                        # seguimos acumulando hasta que converja
                  #      E_bloq_prev = E_bloq_curr

                    # reiniciar bloque
                   # E_bloq_acc = 0.0
                    #contador_en_bloques = 0

                # si no termalizado aun no apuntamos datos
                #if not terma:
                 #   continue

            if imc < args.nequil:
                #no estamos termalizados
                continue

            contador += 1

            # una vez alcanzada la termalizacion empezamos a apuntar valores
            m = M / N
            magne_sum += m
            magne2_sum += m * m
            magne_abs_sum += abs(m)

            e = E / N
            ener_sum += e
            ener2_sum += e * e
        #magnitudes por espin
        e_mean  = ener_sum / contador
        e2_mean = ener2_sum / contador
        magne_abs_sum = magne_abs_sum / contador
        m_mean  = magne_sum / contador
        m2_mean = magne2_sum / contador

        # calor específico y susceptibilidad (intensivos por espín)
        Cv  = N * (e2_mean - e_mean * e_mean) / (temp * temp)
        chi = N * (m2_mean - m_mean * m_mean) / (temp)


        # guardar para gráficas
        T_vals.append(temp)
        E_vals.append(e_mean)
        Cv_vals.append(Cv)
        M_vals.append(magne_abs_sum)
        Chi_vals.append(chi)
    print("Cálculo completado. Archivos: Magneti.dat, Energia.dat")

    T = np.array(T_vals)
    plot_energia(T, np.array(E_vals))
    plot_calor(T, np.array(Cv_vals))
    plot_magnetizacion(T, np.array(M_vals))
    plot_susceptibilidad(T, np.array(Chi_vals))
if __name__ == "__main__":
    main()