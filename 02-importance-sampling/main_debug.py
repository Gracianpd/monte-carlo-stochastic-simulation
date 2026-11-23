import os
import time
from calculations import L, mc_uniform, mc_no_uniform, mc_no_uniform_good_result, I_exact
from plotter_debug import hist_x_only, plot_rho_and_rectangles

if __name__ == "__main__":
    N = 200000
    seed = -int(time.time())
    out_base = "Outputs"
    os.makedirs(out_base, exist_ok=True)

    # 0) Curva y rectángulos (explica el esquema)
    plot_rho_and_rectangles(L, savepath=os.path.join(out_base, "rho_rectangulos.png"))

    # 1) Uniforme
    Iu, xs_u = mc_uniform(N, seed, return_x=True)
    hist_x_only(xs_u, L, title="Uniforme (x usados)",
                savepath=os.path.join(out_base, "hist_uniforme.png"))

    # 2) No uniforme correcto (y en [0,1])
    Ia, xs_a, acc_a = mc_no_uniform_good_result(N, seed-123, return_x=True, return_acceptance=True)
    hist_x_only(xs_a, L, title="No-unif bueno (x aceptados)",
                savepath=os.path.join(out_base, "hist_no_unif_bueno.png"))

    # 3) No uniforme enunciado/sesgado (y en [rho(L),1])
    Ib, xs_b, acc_b = mc_no_uniform(N, seed-456, return_x=True, return_acceptance=True)
    hist_x_only(xs_b, L, title="No-unif sesgado (x aceptados)",
                savepath=os.path.join(out_base, "hist_no_unif_enunciado.png"))

    print("I_exact:", I_exact())
    print("Uniforme:", Iu)
    print("No-unif bueno:", Ia, " | acceptance:", acc_a)
    print("No-unif enunciado:", Ib, " | acceptance:", acc_b)
