
class Field():
    def __init__(self, key, default=None, subclass=None):
        self.key = key
        self.default = default
        self.subclass = subclass

    def __get__(self, instance, owner):
        if not instance:
            return self
        else:
            return self.getter(instance)

    def __set__(self, instance, value):
        # todo None->delete (required-fields?)
        self.validate(value)
        self.setter(instance, value)

    def setter(self, instance, value):
        instance.set_values(self.key, [value])

    def getter(self, parent):
        value = parent.get_values(self.key)
        return value[0]

    def validate(self, value):
        return value

    def parse(self, string):
        pass


class Point2D(Field):
    def validate(self, value):
        assert not isinstance(value, str)
        assert len(value) == 2


class Point3D(Field):
    def validate(self, value):
        assert not isinstance(value, str)
        assert len(value) in (2, 3)

    def setter(self, instance, value):
        # Append z-coordinate
        if len(value) == 2:
            value = value + [0]
        print(value)
        instance.set_values(self.key, value[0])
        instance.set_values(self.key+10, value[1])
        instance.set_values(self.key+20, value[2])

    def getter(self, parent):
        x = parent.get_values(self.key)
        y = parent.get_values(self.key + 10)
        z = parent.get_values(self.key + 20)
        print(x,y,z)
        print("jo", list(parent._tags))
        return [x, y, z]


class Integer(Field):
    def validate(self, value):
        assert isinstance(value, int)


class Hex(Field):
    def validate(self, value):
        int(value, 16)

