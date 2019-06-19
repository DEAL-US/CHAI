from criteria.BaseCriterion import BaseCriterion

class RelationCriterion(BaseCriterion):

    def __init__(self, name, entities):
        self.entities = entities
        super().__init__(name)

    def get_candidates_for_entity(self, entity):
        return self.entities
