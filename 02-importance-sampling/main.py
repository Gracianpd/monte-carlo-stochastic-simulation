import time
from calculations import *

if __name__ == "__main__":
    N = 10000000
    Ns = [N, N / 10, 3 * N / 10, 5 * N / 10, 7 * N / 10, 9 * N / 10]
    I_uni_av, I_non_uni_av, I_non_uni_good_av =0, 0, 0
    I_exact = I_exact()
    for n in Ns:
        n = int(n)
        seed = -int(time.time()) + n
        I_uniform = mc_uniform(N,seed)
        I_non_uniform = mc_no_uniform(N, seed)
        I_non_uniform_good_result = mc_no_uniform_good_result(N,seed)
        I_uni_av += I_uniform
        I_non_uni_av += I_non_uniform
        I_non_uni_good_av += I_non_uniform_good_result
    I_uni_av /= len(Ns)
    I_non_uni_av /= len(Ns)
    I_non_uni_good_av /= len(Ns)
    print(f"Exact: {I_exact}, Uniform: {I_uni_av}, Non-uniform: {I_non_uni_av}, Non-uniform Good: {I_non_uni_good_av}")
    print(f"{I_exact}\t{I_uni_av}\t{I_non_uni_av}\t{I_non_uni_good_av}")