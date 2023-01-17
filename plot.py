import numpy as np
import matplotlib.pyplot as plt
from glob import glob

# All datasets
datasets = glob("*.npy")
datasets.sort()

# Average
avgs = []
for dataset in datasets:
	avgs.append(np.load(dataset))

#avgs = np.concatenate(avgs, axis=0).T
avgs = np.array(avgs).T

plt.imshow(avgs, origin = "lower", aspect="auto")
plt.colorbar()
plt.savefig("sol.png")

