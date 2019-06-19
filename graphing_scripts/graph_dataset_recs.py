import sys
from os import listdir
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

folder = sys.argv[1]
datasets = [x[:-4] for x in listdir(folder) if x[-3:] == "txt"]
current_rel = ""

for dset in datasets:
    current_rel = ""
    recalls = []
    current_recall = []
    with open(f"{folder}/{dset}.txt", "r") as f:
        for line in f:
            spl = line.strip().split(";")
            try:
                rel, recall, rr, fitness = spl[0], float(spl[2]), float(spl[3]), float(spl[4])
            except ValueError: continue

            if not current_rel: current_rel = rel
            
            if rel != current_rel:
                recalls.append(current_recall)
                current_recall = []
                current_rel = rel

            current_recall.append(recall)

    max_len = 13 if dset.lower() in ("fb13", "wn18-ar") else 9
    for rec in recalls:
        while len(rec) < max_len:
            rec.append(rec[-1])
    
    xs = [i+1 for i in range(max_len)]

    plt.clf()
    plt.axis([0, max_len, 0, 1])
    for rec in recalls:
        line, = plt.plot(xs, rec[:max_len], '-o')
        line.set_markersize(3)

    fontsize = 17

    plt.xlabel("Rule size", fontsize=fontsize)
    plt.ylabel("Recall", fontsize=fontsize)

    plt.tick_params(
    axis='both',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=True)
        
    plt.xticks([i for i in range(len(xs)) if i % 2 == 1])
    plt.tick_params(labelsize=fontsize)
    plt.savefig(f"results/{dset}_recall.png", bbox_inches='tight')

