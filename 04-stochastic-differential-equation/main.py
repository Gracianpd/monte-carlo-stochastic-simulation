# main.py
import numpy as np
from calculos import SimConfig, simulate_heun_stratonovich, stationary_stats
from plotting import plot_mean, plot_variance, plot_pdf


def main():
    cfg = SimConfig(
        n_sim=100_000,      # enunciado
        batch_size=10_000,  # ajusta según RAM
        seed=2026,
        boundary="bounce"     # mantener x>=0
    )

    cases = [
        ("Caso I", 2.2, (0.0, 2.0)),
        ("Caso II", np.sqrt(2.0), (0.0, 0.8)),
        ("Caso III", 1.0, (0.0, 1.2)),
    ]

    for name, sigma, ylims_pdf in cases:
        print(f"=== {name} | sigma={sigma} ===")

        # Simulación
        sim = simulate_heun_stratonovich(cfg, sigma=sigma)

        # Estacionaria (para superponer y para líneas horizontales)
        st = stationary_stats(cfg, sigma=sigma)
        if st is None:
            mean_st = None
            var_st = None
            x_st = None
            p_st = None
        else:
            mean_st = st["mean"]
            var_st = st["var"]
            x_st = st["x"]
            p_st = st["p"]

        # Figuras
        plot_mean(
            sim["tp"], sim["mean_t"], mean_st,
            title=f"{name}: Media (sigma={sigma})",
            outpath=f"{name.replace(' ', '_')}_media.png"
        )

        plot_variance(
            sim["tp"], sim["var_t"], var_st,
            title=f"{name}: Varianza (sigma={sigma})",
            outpath=f"{name.replace(' ', '_')}_varianza.png"
        )

        plot_pdf(
            sim["bin_centers"], sim["pT"], ylims_pdf,
            x_st=x_st, p_st=p_st,
            title=f"{name}: PDF en T=50 (sigma={sigma})",
            outpath=f"{name.replace(' ', '_')}_pdf_T50.png"
        )

        if mean_st is not None:
            print(f"  <x>_st ≈ {mean_st:.6g}")
            print(f"  Var_st ≈ {var_st:.6g}")

    print("Listo: guardadas 9 figuras (media/varianza/pdf por caso).")


if __name__ == "__main__":
    main()
