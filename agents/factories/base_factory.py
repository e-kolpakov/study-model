__author__ = 'john'


class BaseFactory:
    def produce(self, product_spec):
        """
        :rtype: T <= BaseAgent
        """
        raise NotImplemented
