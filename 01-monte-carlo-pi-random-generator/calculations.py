import random

import numpy as np
from ran_generator import ran1
import random as rand

def estimate_pi(N, seed):
    #inputs: num points, seed
    sphere_point_counter = 0
    state = {"x": seed}
    #generate ran numbers. Out ran generator shuffles the values so we dont have to worry about correlation in succesive xi+1
    for i in range(N):
        x = ran1(seed)
        y = ran1(seed)
        z = ran1(seed)
        w = ran1(seed)
        point_module = x*x + y*y + z*z + w*w
        if point_module <= 1:
            sphere_point_counter += 1

    proportion = sphere_point_counter/N
    pi = np.sqrt(32* proportion)

    return pi

def estimate_pi_python_ran(N):
    sphere_point_counter = 0
    rng = random.Random()
    for i in range(N):
        x = rng.random()
        y = rng.random()
        z = rng.random()
        w = rng.random()
        point_module = x * x + y * y + z * z + w * w
        if point_module <= 1:
            sphere_point_counter += 1

    proportion = sphere_point_counter / N
    pi = np.sqrt(32 * proportion)

    return pi


