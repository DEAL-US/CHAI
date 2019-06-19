import sys
from os import listdir
import matplotlib.pyplot as plt

folder = sys.argv[1]
datasets = [x[:-4] for x in listdir(folder) if x[-3:] == "txt"]
current_rel = ""

def get_recall_shi(dset, rel_find):
    with open(f"results_shi/{dset}.txt", "r") as f:
        for line in f:
            rel, _, recall, rr, _ = line.strip().split(";")
            if rel == rel_find:
                return float(recall), float(rr)

for dset in datasets:
    points = []
    current_rel = ""
    with open(f"{folder}/{dset}.txt", "r") as f:
        recalls = []
        rrs = []

        for line in f:
            spl = line.strip().split(";")
            try:
                rel, recall, rr = spl[0], float(spl[2]), float(spl[3])
            except ValueError:
                if line: continue

            if not line or rel != current_rel:
                if current_rel:
                    xs = [x+1 for x in range(len(recalls))]
                    plt.axis([0, max(10, len(xs)), 0, 1])
                    recall_shi, rr_shi = get_recall_shi(dset, current_rel)
                    recall_line, = plt.plot(xs, recalls, '-o', label="Recall", color="#0060fc")
                    recall_line.set_markersize(6)
                    rr_line, = plt.plot(xs, rrs, '-o', label="RR", color="#ff0000")
                    rr_line.set_markersize(6)
                    recalls_shi_line, = plt.plot(xs, [recall_shi for _ in xs], '-', label="Shi-Recall", color="#7fafff")
                    #recalls_shi_line.set_markersize(6)
                    rrs_shi_line, = plt.plot(xs, [rr_shi for _ in xs], '-', label="Shi-RR", color="#ffa0a0")
                    plt.legend(
                        (recall_line, rr_line, recalls_shi_line, rrs_shi_line), 
                        ("Recall", "Reduction Rate", "Shi-Recall", "Shi-RR")
                    )
                    plt.title(f"{dset} {current_rel}")
                    try:
                        plt.savefig(f"{folder}/{dset}_rel_{current_rel}.png", bbox_inches='tight')
                        #plt.savefig(f"{folder}/{dset}_{current_rel}.eps", bbox_inches='tight')
                    except: pass
                    plt.clf()
                recalls = []
                rrs = []
                current_rel = rel

            recalls.append(recall)
            rrs.append(rr)
