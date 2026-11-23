import numpy as np
import math
from ran_generator import ran1

def tablero_damas(nfilas: int, ncolum: int) -> np.ndarray:
    #crea config tablero damas iniccial. Para suma indices impares el spin 1, impares -1
    A = np.empty((nfilas, ncolum), dtype=np.int8)
    for i in range(nfilas):
        for j in range(ncolum):
            A[i, j] = 1 if (i + j) % 2 == 0 else -1
    return A


def magnetizacion(A: np.ndarray) -> float:
    return float(A.sum())


def energia_total(A, J):
    #calcula energia total del sistema
    nfilas, ncolum = A.shape
    E = 0.0

    for i in range(nfilas):
        for j in range(ncolum):
            s = A[i, j]
            up    = A[(i - 1) % nfilas, j]
            down  = A[(i + 1) % nfilas, j]
            left  = A[i, (j - 1) % ncolum]
            right = A[i, (j + 1) % ncolum]
            E += -J * s * (up + down + left + right)
    return E * 0.5


def delta_E(A: np.ndarray, i: int, j: int, J: float, h: float = 0.0) -> float:
    #calcula difernecia de energia entre dos estados
    nfilas, ncolum = A.shape
    s = int(A[i, j])

    up = A[(i - 1) % nfilas, j]
    down = A[(i + 1) % nfilas, j]
    left = A[i, (j - 1) % ncolum]
    right = A[i, (j + 1) % ncolum]

    nn_sum = up + down + left + right
    return 2.0 * s * (J * nn_sum)

def ran_int(state, n):
    #Devuelve entero aleatorio 0..n-1 usando ran1
    return int(ran1(state) * n)

def metropolis_sweep(A, beta, J, state):
    #PASO 3 algoritmo metropolis
    nfilas, ncolum = A.shape
    N = nfilas * ncolum

    dE_tot = 0.0
    dM_tot = 0.0

    for _ in range(N):
        i = ran_int(state, nfilas)
        j = ran_int(state, ncolum)

        s = A[i, j]
        dE = delta_E(A, i, j, J)

        if dE <= 0 or ran1(state) < math.exp(-beta * dE):
            A[i, j] = -s
            dE_tot += dE
            dM_tot += -2 * s

    return dE_tot, dM_tot


def check_thermalization(E_prev, E_curr, eps=0.01):
    if E_prev is None:
        return False

    diff = abs(E_curr - E_prev) / (abs(E_curr) + abs(E_prev))

    return diff < eps


def todos_arriba(nfilas: int, ncolum: int, spin: int = 1) -> np.ndarray:
    #crea distribucion con todos espines en una direccion
    return np.full((nfilas, ncolum), spin, dtype=np.int8)
