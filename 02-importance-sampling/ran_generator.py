#constants:
IA = 16807
IM = 2147483647
AM = 1.0 / IM
IQ = 127773
IR = 2836
NTAB = 32
NDIV = 1 + (IM - 1) // NTAB
EPS = 1.2e-7
RNMX = 1.0 - EPS

def ran1(state):
    #esta funcion recibe un valor inicial "seed" y a partir de él crea el próximo valor aleatorio

    # recordamos valores entre llamadas a ran1
    if not hasattr(ran1, "iv"):
        ran1.iv = [0] * NTAB
        ran1.iy = 0

    #estado anterior
    x = state["x"]

    #primera llamada
    if x <= 0 or ran1.iy == 0:
        x = max(-x,1)
        for j in range(NTAB + 7, -1, -1):
            k = x // IQ
            x = IA * (x - k * IQ) - IR * k
            if x < 0:
                x += IM
            if j < NTAB:
                ran1.iv[j] = x
        ran1.iy = ran1.iv[0]

    k = x // IQ
    x = IA * (x - k * IQ) - IR * k
    if x < 0:
        x += IM

    j = ran1.iy // NDIV
    ran1.iy = ran1.iv[j]
    ran1.iv[j] = x

    temp = AM * ran1.iy
    state["x"] = x

    return min(temp, RNMX)
