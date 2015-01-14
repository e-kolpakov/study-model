__author__ = 'e.kolpakov'


class TypedDescriptor:
    def __init__(self, target_type, label):
        self._type = target_type
        self._lbl = '_'+label

    @property
    def _label(self):
        return self._lbl

    def __get__(self, instance, owner):
        if instance is None:
            return None
        return getattr(instance, self._label, None)

    def __set__(self, instance, value):
        if not isinstance(value, self._type):
            raise ValueError
        setattr(instance, self._label, value)

    def __delete__(self, instance):
        delattr(instance, self._label)


class TypedDescriptorWithDefault(TypedDescriptor):
    def __init__(self, target_type, label):
        super(TypedDescriptorWithDefault, self).__init__(target_type, label)
        self._default = target_type

    def __get__(self, instance, owner):
        if instance is None:
            return None
        existing_value = getattr(instance, self._label, None)
        if existing_value is not None:
            return existing_value
        if self._default is not None:
            new_value = self._default()
            setattr(instance, self._label, new_value)
            return new_value
        return None
