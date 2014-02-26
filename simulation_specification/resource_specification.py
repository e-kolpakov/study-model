__author__ = 'john'


class ResourceSpecification(object):
    def __init__(self, resource_name, provides_knowledge, behavior, resource_id = None):
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.provides_knowledge = provides_knowledge
        self.behavior = behavior
