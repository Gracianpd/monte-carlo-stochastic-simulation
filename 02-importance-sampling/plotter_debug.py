import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def hist_x_only(xs, L, bins=60, title=None, savepath=None):
    xs = np.asarray(xs, dtype=float)

    plt.figure(figsize=(6,4))
    plt.hist(xs, bins=bins, range=(0, L), density=True, alpha=0.8)
    plt.xlabel("x")
    plt.ylabel("densidad")
    if title:
        plt.title(title)
    plt.tight_layout()

    if savepath:
        plt.savefig(savepath, dpi=200)
    plt.show()


def plot_rho_and_rectangles(L, savepath=None):
    def rho(x):
        return 1 - x * x

    x = np.linspace(0, L, 500)
    y = rho(x)

    y_min_good, y_max_good = 0.0, 1.0
    y_min_bad, y_max_bad = rho(L), 1.0  # [rho(L), rho(0)]

    plt.figure(figsize=(6, 4))

    # Rectángulo "bueno": [0,L] x [0,1]
    rect_good = Rectangle((0, y_min_good), L, y_max_good - y_min_good,
                          fill=False, linewidth=2, linestyle='-')
    plt.gca().add_patch(rect_good)
    plt.text(0.02 * L, 0.02, "y∈[0,1]", fontsize=10)

    # Rectángulo "malo/enunciado": [0,L] x [rho(L), 1]
    rect_bad = Rectangle((0, y_min_bad), L, y_max_bad - y_min_bad,
                         fill=False, linewidth=2, linestyle='--')
    plt.gca().add_patch(rect_bad)
    plt.text(0.02 * L, y_min_bad + 0.02, r"y∈[$\rho(L)$,1]", fontsize=10)

    # Curva rho(x)
    plt.plot(x, y, linewidth=2)
    plt.text(0.65 * L, rho(0.65 * L) + 0.02, r"$\rho(x)=1-x^2$", fontsize=11)

    plt.xlim(0, L)
    plt.ylim(0, 1.02)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()

    if savepath:
        plt.savefig(savepath, dpi=200)
    plt.show()
