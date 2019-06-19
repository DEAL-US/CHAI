import sys
from os import listdir
import matplotlib.pyplot as plt

folder = sys.argv[1]
datasets = [x[:-4] for x in listdir(folder) if x[-3:] == "txt"]

for dset in datasets:
    points = []
    with open(f"{folder}/{dset}.txt", "r") as f:
        for line in f:
            spl = line.strip().split(";")
            try:
                points.append((float(spl[2]), float(spl[3])))
            except ValueError: pass

    recalls, rrs = [p[0] for p in points], [p[1] for p in points]
    fontsize = 17
    plt.axis([0, 1, 0, 1])
    plt.xlabel("Reduction rate", fontsize=fontsize)
    plt.ylabel("Recall", fontsize=fontsize)
    plt.plot(rrs, recalls, 'o')
    plt.tick_params(labelsize=fontsize)
    plt.grid(True)
    plt.savefig(f"results/{dset}_points.png", bbox_inches='tight')
    plt.clf()