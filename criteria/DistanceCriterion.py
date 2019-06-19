from criteria.BaseCriterion import BaseCriterion
from json                   import loads

class DistanceCriterion(BaseCriterion):

    def __init__(self, name, dataset, size, entity_dict):
        self.data = {}
        with open(f"distances_data/{dataset}_{size}.txt", "r") as f:
            for line in f:
                spl = line.strip().split(";")
                self.data[entity_dict[spl[0]]] = loads("[" + spl[1] + "]")
        super().__init__(name)

    def get_candidates_for_entity(self, entity):
        return self.data.get(entity, [])
