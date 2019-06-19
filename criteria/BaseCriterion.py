class BaseCriterion():

    def __init__(self, name):
        self.name = name

    def get_candidates_for_entity(self, entity):
        raise NotImplementedError

    '''
    def get_avg_recall_for_entities(self, entities, ground_truth):
        recalls = []
        for ent in entities:
            try:
                candidates = self.get_candidates_for_entity(ent)
                truth = ground_truth[ent]
                recalls.append(float(len([x for x in truth if x in candidates])) / len(truth))
            except KeyError:
                continue

        try:
            res = sum(recalls) / len(recalls)
        except ZeroDivisionError:
            res = 0.0

        return res

    def get_leveraged_avg_recall_for_entities(self, num_total_ents, entities, ground_truth):
        recalls = []
        for ent in entities:
            try:
                candidates = self.get_candidates_for_entity(ent)
                truth = ground_truth[ent]
                rec = float(len([x for x in truth if x in candidates])) / len(truth)
                rr = 1.0 - len(candidates) / num_total_ents
                leveraged = 2*rec*rr / (rec + rr)
                recalls.append(leveraged)
            except KeyError:
                continue

        try:
            res = sum(recalls) / len(recalls)
        except ZeroDivisionError:
            res = 0.0

        return res
    '''