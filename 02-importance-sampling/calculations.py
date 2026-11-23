import numpy as np
from ran_generator import ran1

# general params
L = 0.8
C = L - (L**3) / 3.0                # C_A = ∫_0^L (1-x^2) dx
C_B = (2.0/3.0) * (L**3)            # ∫_0^L (L^2-x^2) dx

def function(x):
    return np.cos(0.5 * np.pi * x)

def I_exact():
    return (2 / np.pi) * np.sin(0.5 * np.pi * L)

def mc_uniform(N, seed, return_x=False, max_store=200000):
    s = 0.0
    xs = [] if return_x else None

    state = {"x": seed}
    for i in range(N):
        t = ran1(state)
        x = L * t
        s += function(x)
        if return_x and len(xs) < max_store:
            xs.append(x)

    I_est = L * s / N
    return (I_est, xs) if return_x else I_est


def mc_no_uniform(N, seed, return_x=False, max_store=200000, return_acceptance=False):
    """
    Tu método 'sesgado': y en [1-L^2, 1].
    Los x aceptados NO siguen (1-x^2), sino (L^2 - x^2).
    """
    state = {"x": seed}
    s = 0.0
    accepted_points = 0
    trials = 0
    xs = [] if return_x else None

    while accepted_points < N:
        trials += 1
        x1 = ran1(state) * L

        # y en [1 - L^2, 1]
        y1 = 1 - (L * L) * ran1(state)

        if y1 < (1 - x1 * x1):
            # OJO: este peso asume p(x) ∝ (1-x^2) -> aquí está el sesgo
            s += function(x1) / ((1 - x1 * x1) / C)
            accepted_points += 1

            if return_x and len(xs) < max_store:
                xs.append(x1)

    I_est = s / N

    if return_acceptance:
        acc_rate = accepted_points / trials
        if return_x:
            return I_est, xs, acc_rate
        return I_est, acc_rate

    return (I_est, xs) if return_x else I_est


def mc_no_uniform_good_result(N, seed, return_x=False, max_store=200000, return_acceptance=False):
    """
    Método correcto: y en [0,1] -> x aceptado sigue p(x) ∝ (1-x^2).
    """
    state = {"x": seed}
    s = 0.0
    accepted_points = 0
    trials = 0
    xs = [] if return_x else None

    while accepted_points < N:
        trials += 1
        x1 = ran1(state) * L
        y1 = ran1(state)  # U[0,1]

        if y1 < (1 - x1 * x1):
            s += function(x1) / ((1 - x1 * x1) / C)
            accepted_points += 1

            if return_x and len(xs) < max_store:
                xs.append(x1)

    I_est = s / N

    if return_acceptance:
        acc_rate = accepted_points / trials
        if return_x:
            return I_est, xs, acc_rate
        return I_est, acc_rate

    return (I_est, xs) if return_x else I_est
