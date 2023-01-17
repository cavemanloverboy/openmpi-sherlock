import numpy as np
from time import perf_counter as time


ITERATIONS = 10000
N = 1000

counter = 0
# We don't want to benchmark this allocation
A = np.ones((N,N))
x = np.ones((N,))
for i in range(-100, ITERATIONS):

    # Only include the matmul
    start_iter = time()
    b = A.dot(x)
    if i >= 0:
        counter += time()-start_iter

print(f"Finished {ITERATIONS} ({N} x {N}) x ({N} x 1) matmuls in {counter} seconds\n")
