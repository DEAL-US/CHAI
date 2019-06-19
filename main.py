from criteria.RelationCriterion import RelationCriterion
from criteria.DistanceCriterion import DistanceCriterion

from tqdm       import tqdm
from os.path    import exists

import sys
import re


FITNESS_THRESHOLD = 0.99

def get_fitness(recall, rr):
    return (2*recall*rr) / (recall+rr)

def get_metrics_for_criteria(criteria, n_ents, s_s, test, test_dict):
    n_total = 0
    n_appear_test = 0

    for s in s_s:
        cands = []
        for crit in criteria:
            cands.extend(crit.get_candidates_for_entity(s))
        if len(criteria) > 1:
            cands = list(set(cands))

        n_total += len(cands)
        if s in test_dict:
            n_appear_test += sum(1 for x in test_dict[s] if x in cands)

    recall = n_appear_test / len(test)
    rr = 1 - n_total / (len(set(s_s)) * n_ents)
    fitness = get_fitness(recall, rr)
    return recall, rr, fitness

for DATASET in sys.argv[1:]:
    print("Dataset:", DATASET)
    entities = []
    relations = []
    train_triples = []
    test_data = {}
    all_criteria = []
    entity_dict = {}

    print("Using dataset", DATASET)

    print("Loading entities")
    with open(f"datasets/{DATASET}/entities.txt", "r") as f:
        for i, line in enumerate(f, start=1):
            ent = line.strip().split("\t")[0]
            entities.append(ent)
            entity_dict[ent] = i

    total_entities = len(entities)

    print("Loading relations")
    with open(f"datasets/{DATASET}/relations.txt", "r") as f:
        for line in f:
            rel = line.strip().split("\t")[0]
            relations.append(rel)

    print("Loading training data")
    with open(f"datasets/{DATASET}/train.txt", "r") as f:
        for line in f:
            split = line.strip().split("\t")
            if len(split) == 3:
                s, p, o = split
            else:
                if int(split[3]) != 1: continue
                s, p, o = split[:3]
            train_triples.append((entity_dict[s], p, entity_dict[o]))

    print("Loading testing data")
    with open(f"datasets/{DATASET}/test.txt", "r") as f:
        for line in f:
            s, p, o, label = line.strip().split("\t")[:4]
            if label != "1": continue

            s = entity_dict[s]
            o = entity_dict[o]

            if s not in test_data:
                test_data[s] = {}

            if p not in test_data[s]:
                test_data[s][p] = []
            
            test_data[s][p].append(o)

    print("Loading criteria... ", end="", flush=True)
    ### Relation range and domain criteria
    ranges = {rel: {'dom': [], 'ran': []} for rel in relations}
    for s, p, o in train_triples:
        ranges[p]['dom'].append(s)
        ranges[p]['ran'].append(o)

    for rel in relations:
        all_criteria.append(
            RelationCriterion(rel + "_DOMAIN", list(set(ranges[rel]['dom'])))
        )
        all_criteria.append(
            RelationCriterion(rel + "_RANGE", list(set(ranges[rel]['ran'])))
        )
    
    ### Distance criteria
    for i in (1,2,3,4):
        all_criteria.append(DistanceCriterion(f"subg{i}", DATASET, i, entity_dict))

    print("done.")

    open(f"results/{DATASET}.txt", "w").write("relation;criteria;recall;rr;fitness\n")

    rels_to_study_path = f"datasets/{DATASET}/relations_to_study.txt"
    if not exists(rels_to_study_path):
        relations_to_study = relations
    else:
        relations_to_study = []
        with open(rels_to_study_path, "r") as f:
            for line in f:
                relations_to_study.append(line.strip().split("\t")[0])

    for rel in relations_to_study:
        print("=======================================")
        print("Using relation", rel)
        print("=======================================")

        criteria = all_criteria
        #criteria = list(filter(lambda x: x.name == rel + "_RANGE", all_criteria))

        print("Selecting entities to evaluate")
        ents_to_eval = [s for s, _, _ in train_triples 
                        if s in test_data and rel in test_data[s]]
        
        print("Creating ground truth")
        ground_truth_for_rel = {ent: test_data[ent][rel] for ent in ents_to_eval}

        #################################################################################
        print("Creating testing triples")
        test_triples_ff = []
        for s in ground_truth_for_rel:
            for o in ground_truth_for_rel[s]:
                test_triples_ff.append((s,rel,o))

        print("Creating training triples")
        s_s = list(set(
            [s for s, p, _ in train_triples if p == rel] + 
            [s for s in test_data if rel in test_data[s]]
        ))

        #################################################################################
        print("Sorting criteria by fitness")
        criteria.sort(
            reverse=True, 
            key=lambda x: get_metrics_for_criteria(
                [x],
                total_entities,
                s_s,
                test_triples_ff,
                ground_truth_for_rel
            )[2]
        )

        last_recall_value = None
        same_recall_count = 0
        file_lines_simple = []
        file_lines_full = []
        
        for i in range(len(criteria)):
            print("Adding criteria:", criteria[i].name)
            selected_criteria = criteria[:i+1]
            recall, rr, fitness = get_metrics_for_criteria(
                selected_criteria,
                total_entities,
                s_s,
                test_triples_ff,
                ground_truth_for_rel
            )

            print(f"Fitness is {fitness:.2f} (recall {recall:.2f}, RR {rr:.2f})")
            file_lines_simple.append(
                f"{rel};" + \
                ",".join(criteria[j].name for j in range(i+1)) + ";" + \
                f"{recall};{rr};{fitness}\n"
            )
            
            if recall != last_recall_value:
                last_recall_value = recall
                same_recall_count = 0
            else:
                same_recall_count += 1
                print(f"Recall hasn't changed ({same_recall_count})", end='\n' if same_recall_count != 3 else '')
                if same_recall_count == 3:
                    print(". Stopping.")
                    break

            if fitness >= FITNESS_THRESHOLD: break
        
        open(f"results/{DATASET}.txt", "a").writelines(file_lines_simple)



