# calculos.py
import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class SimConfig:
    a: float = 2.0
    b: float = 1.0
    T: float = 50.0
    h: float = 1e-3
    x0: float = 1.0
    n_sim: int = 100_000
    batch_size: int = 10_000
    seed: int | None = None
    sample_dt: float = 0.5   # t_p = p/2

    # Histograma para p(x,T)
    x_min_hist: float = 0.0
    x_max_hist: float = 5.0
    n_bins: int = 200

    # Integración numérica para estacionaria (normalización/momentos)
    x_max_norm: float = 25.0
    n_grid_norm: int = 200_000

    # Tratamiento de frontera x>=0: "clip" o None
    boundary: str = "clip"


def f(x: np.ndarray, a: float, b: float) -> np.ndarray:
    return a * x - x**2 - b * (x / (1.0 + x))


def g(x: np.ndarray) -> np.ndarray:
    return x / (1.0 + x)


def make_time_grid(cfg: SimConfig) -> Tuple[np.ndarray, np.ndarray]:
    """Devuelve tiempos de muestreo t_p y los pasos (índices) donde muestrear."""
    n_steps = int(cfg.T / cfg.h)
    sample_every = int(cfg.sample_dt / cfg.h)
    tp = np.arange(0.0, cfg.T + 1e-12, cfg.sample_dt)
    sample_steps = np.arange(0, n_steps + 1, sample_every, dtype=np.int64)
    if len(tp) != len(sample_steps):
        raise ValueError("Inconsistencia: tp y sample_steps no tienen la misma longitud.")
    return tp, sample_steps


def stationary_density_unnormalized(x: np.ndarray, sigma: float) -> np.ndarray:
    """
    p_st(x) (sin normalizar) para el caso particular a=2,b=1 ya integrado:
    p_st(x) ∝ (1+x) * x^{2/s^2 - 1} * exp(4x/s^2 - 2x^3/(3 s^2)), x>0
    """
    x = np.asarray(x, dtype=np.float64)
    out = np.zeros_like(x)
    mask = x > 0.0
    xm = x[mask]
    s2 = sigma * sigma

    # log para estabilidad numérica
    logp = np.log1p(xm) + (2.0 / s2 - 1.0) * np.log(xm) + (4.0 * xm / s2) - (2.0 * xm**3 / (3.0 * s2))
    out[mask] = np.exp(logp)
    return out


def stationary_stats(cfg: SimConfig, sigma: float) -> Optional[dict]:
    """
    Normaliza p_st en [0,∞) aproximando con [0, x_max_norm], y calcula:
    N (constante), media y varianza estacionarias, y la malla (x,p_st).
    """
    x = np.linspace(0.0, cfg.x_max_norm, cfg.n_grid_norm)
    p_unn = stationary_density_unnormalized(x, sigma)

    Z = np.trapezoid(p_unn, x)
    if not np.isfinite(Z) or Z <= 0:
        return None

    p = p_unn / Z
    mean = np.trapezoid(x * p, x)
    mean2 = np.trapezoid((x**2) * p, x)
    var = mean2 - mean**2

    return {
        "Z": Z,
        "mean": mean,
        "var": var,
        "x": x,
        "p": p
    }

def box_muller_normals(rng: np.random.Generator, n: int) -> np.ndarray:
    """
    Genera n variables ~ N(0,1) usando Box–Muller a partir de U(0,1).
    Devuelve un array de tamaño n.
    """
    if n <= 0:
        return np.empty(0, dtype=np.float64)

    # Necesitamos pares para Box–Muller (cada par de uniformes da 2 gaussianas)
    m = (n + 1) // 2  # número de pares necesarios
    a1 = rng.random(m)  # U(0,1)
    a2 = rng.random(m)  # U(0,1)

    # Evitar log(0): forzamos a1 a estar en (0,1] de forma segura
    # (si a1=0 -> ln(0) -> -inf)
    eps = np.finfo(np.float64).tiny
    a1 = np.clip(a1, eps, 1.0)

    r = np.sqrt(-2.0 * np.log(a1))
    theta = 2.0 * np.pi * a2

    b1 = r * np.cos(theta)
    b2 = r * np.sin(theta)

    out = np.empty(2 * m, dtype=np.float64)
    out[0::2] = b1
    out[1::2] = b2
    return out[:n]

def simulate_heun_stratonovich(cfg: SimConfig, sigma: float) -> dict:
    """
    Simula con Heun (predictor-corrector) para interpretación Stratonovich,
    usando mu_i ~ N(0,1) y el MISMO mu_i en predictor y corrector.

    Devuelve:
      - tp: tiempos de muestreo
      - mean_t: media estimada en tp
      - var_t: varianza estimada en tp
      - bin_centers: centros de bins
      - pT: densidad estimada en T=50 en [x_min_hist,x_max_hist]
    """
    rng = np.random.default_rng(cfg.seed)

    tp, sample_steps = make_time_grid(cfg)
    n_tp = len(tp)

    n_steps = int(cfg.T / cfg.h)
    sqrt_h = np.sqrt(cfg.h)

    # acumuladores para media/varianza
    sum_x = np.zeros(n_tp, dtype=np.float64)
    sum_x2 = np.zeros(n_tp, dtype=np.float64)

    # histograma final
    bin_edges = np.linspace(cfg.x_min_hist, cfg.x_max_hist, cfg.n_bins + 1)
    dx = (cfg.x_max_hist - cfg.x_min_hist) / cfg.n_bins
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    hist_counts = np.zeros(cfg.n_bins, dtype=np.int64)

    done = 0
    while done < cfg.n_sim:
        m = min(cfg.batch_size, cfg.n_sim - done)
        done += m

        x = np.full(m, cfg.x0, dtype=np.float64)

        # muestreo en t=0
        sum_x[0] += x.sum()
        sum_x2[0] += np.square(x).sum()

        next_k = 1
        next_step = sample_steps[next_k] if next_k < n_tp else None

        for i in range(n_steps):
            if cfg.boundary == "clip":
                x = np.maximum(x, 0.0)
            elif cfg.boundary == "bounce":
                x = abs(x)

            mu = box_muller_normals(rng, m)  # N(0,1)

            fx = f(x, cfg.a, cfg.b)
            gx = g(x)

            # Predictor de Euler: x_tilde = x + h f(x) + sigma g(x) mu sqrt(h)
            x_tilde = x + cfg.h * fx + sigma * gx * mu * sqrt_h
            if cfg.boundary == "clip":
                x_tilde = np.maximum(x_tilde, 0.0)
            elif cfg.boundary == "bounce":
                x_tilde = abs(x_tilde)

            # Corrector Heun:
            # x_{i+1} = x_i + 0.5*h*(f(x_i)+f(x_tilde)) + 0.5*sigma*(g(x_i)+g(x_tilde))*mu*sqrt(h)
            fx_t = f(x_tilde, cfg.a, cfg.b)
            gx_t = g(x_tilde)
            x = x + 0.5 * cfg.h * (fx + fx_t) + 0.5 * sigma * (gx + gx_t) * mu * sqrt_h

            step_now = i + 1
            if next_step is not None and step_now == next_step:
                sum_x[next_k] += x.sum()
                sum_x2[next_k] += np.square(x).sum()
                next_k += 1
                next_step = sample_steps[next_k] if next_k < n_tp else None

        # histograma de x(T)
        counts, _ = np.histogram(x, bins=bin_edges)
        hist_counts += counts

    mean_t = sum_x / cfg.n_sim
    mean2_t = sum_x2 / cfg.n_sim
    var_t = mean2_t - mean_t**2
    pT = hist_counts / (cfg.n_sim * dx)

    return {
        "tp": tp,
        "mean_t": mean_t,
        "var_t": var_t,
        "bin_centers": bin_centers,
        "pT": pT
    }
