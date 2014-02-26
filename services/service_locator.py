from collections import defaultdict

__author__ = 'john'


class ServiceLocator(object):
    """
    Simplistic implementation of ServiceLocator pattern.
    Ideally one day should be replaced by some kind of DI container. Or not.
    """
    _empty_tag = "###NO_TAG###"

    def __init__(self):
        self._registered_instances = defaultdict(lambda: defaultdict(list))

    def register_instance(self, instance_type, instance, instance_tag=None):
        """
         :param type instance_type: type of instance
         :param object instance: instance to register
         :param object instance_tag: Optional. Instance tag for precise lookups
         :rtype: None
        """
        if not isinstance(instance_type, type):
            raise ValueError("instance_type: expected type, {0} given".format(instance_type))
        if not isinstance(instance, instance_type):
            raise ValueError("instance is not of type {0}".format(instance_type.__name__))
        effective_tag = instance_tag if instance_tag else self._empty_tag
        self._registered_instances[instance_type][effective_tag].append(instance)

    def get_instances(self, instance_type, instance_tag=None):
        """
        :param type instance_type: type of instance to get
        :param object instance_tag: Optional. Instance tag for precise lookups
        :rtype: list[object]
        """
        effective_tag = instance_tag if instance_tag else self._empty_tag
        return self._registered_instances[instance_type][effective_tag]
