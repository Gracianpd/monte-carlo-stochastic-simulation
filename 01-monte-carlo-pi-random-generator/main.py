import os
import math
import time
from ran_generator import ran1
from plotter import *
from calculations import estimate_pi, estimate_pi_python_ran
import csv

if __name__ == "__main__":
    mode = "plot_variance" #can be estimate_pi_value or "variance"
    if mode == "estimate_pi_value":
        # modo simple que solo calcula pi. Se utilizan 5 semillas diferentes para mejorar error. Inputs:
        N, av_pi, av_pi_python, i = 10000, 0, 0, 1
        output = "Outputs"
        Ns = [N, N / 10, 3 * N / 10, 5 * N / 10, 7 * N / 10, 9 * N / 10]
        for var in Ns:
            var = int(var)
            seed = {"x": -int(time.time()) + var}
            nums = [ran1(seed) for _ in range(N)]
            plot_hist_ran(nums, output, i)
            pi = estimate_pi(N, seed)
            pi_python_ran = estimate_pi_python_ran(N)
            print (str(pi))
            av_pi += pi
            av_pi_python += pi_python_ran
            i += 1
        av_pi /= len(Ns)
        av_pi_python /= len(Ns)
        print("av pi:" + str(av_pi))
        print("av pi_python:" + str(av_pi_python))
    elif mode == "variance":
        # modo que repite para cada N varias veces el cáclulo de pi para poder estudiar la varianza
        os.makedirs("Outputs", exist_ok=True)
        output_file = os.path.join("Outputs", "estudio_varianza.csv")
        N = [10000, 100000, 1000000, 10000000]
        header = ["N", "avg_pi", "std_pi", "1/sqrt(N)"]
        with open(output_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            repeat = 50

            for n in N:
                estimates = []
                for r in range(repeat):
                    seed = {"x": -((int(time.time()) + r) * 5099)}
                    estimates.append(estimate_pi(n, seed))
                avg = sum(estimates) / repeat
                var = sum((x - avg) ** 2 for x in estimates) / repeat
                std = math.sqrt(var)

                writer.writerow([n, avg, std, 1/math.sqrt(n)])
                print(f"calculated values for {n} points")

        print(f"Resultados guardados en '{output_file}' correctamente ✅")

    elif mode == "plot_variance":
        plot_variance(os.path.join("Outputs", "estudio_varianza.csv"))

