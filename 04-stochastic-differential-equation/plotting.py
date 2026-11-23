# plotting.py
import numpy as np
import matplotlib.pyplot as plt
from typing import Optional


def plot_mean(tp, mean_t, mean_st: Optional[float], title: str, outpath: str):
    plt.figure()
    plt.plot(tp, mean_t, label=r'$\langle x(t_p)\rangle$')
    if mean_st is not None:
        plt.hlines(mean_st, tp[0], tp[-1], linestyles='--', label=r'$\langle x\rangle_{st}$ (FP)')
    plt.xlim(tp[0], tp[-1])
    plt.xlabel(r'$t_p$')
    plt.ylabel(r'$\langle x\rangle$')
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


def plot_variance(tp, var_t, var_st: Optional[float], title: str, outpath: str):
    plt.figure()
    plt.plot(tp, var_t, label=r'$\mathrm{Var}[x(t_p)]$')
    if var_st is not None:
        plt.hlines(var_st, tp[0], tp[-1], linestyles='--', label=r'$\mathrm{Var}[x]_{st}$ (FP)')
    plt.xlim(tp[0], tp[-1])
    plt.xlabel(r'$t_p$')
    plt.ylabel(r'$\mathrm{Var}[x]$')
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


def plot_pdf(bin_centers, pT, ylims, x_st=None, p_st=None, title: str = "", outpath: str = ""):
    plt.figure()

    # Anchura de bin a partir de los centros (asumiendo bins uniformes)
    dx = bin_centers[1] - bin_centers[0] if len(bin_centers) > 1 else 0.025

    # Histograma sólido (barras rellenas)
    plt.bar(bin_centers, pT, width=dx, align='center', edgecolor='black', linewidth=0.3,
            label=r'$\hat p(x,T)$ (hist.)')

    # Curva estacionaria encima
    if x_st is not None and p_st is not None:
        mask = (x_st >= 0.0) & (x_st <= 5.0)
        plt.plot(x_st[mask], p_st[mask], label=r'$p_{st}(x)$ (FP)')

    plt.xlim(0.0, 5.0)
    plt.ylim(*ylims)
    plt.xlabel(r'$x$')
    plt.ylabel(r'$p(x,T)$')
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()

