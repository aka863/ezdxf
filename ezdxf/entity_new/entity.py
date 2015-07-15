import copy
import collections
from ezdxf.entity_new.fields import Field, Point3D, Point2D
from ezdxf.entity_new.tags import Tags, Tag


class EntityMeta(type):
    def __new__(cls, name, parent, dct):
        """
        Register Fields
        """
        meta = dct.get("META", object)

        subclass = getattr(meta, "subclass", None)
        if subclass is None:
            subclass = getattr(parent[0], "_subclass")
        dct["_subclass"] = subclass
        for key, value in dct.items():
            if isinstance(value, Field):
                dct[key] = copy.copy(value)
                dct[key].subclass = subclass

        res = super(EntityMeta, cls).__new__(cls, name, parent, dct)

        return res


class Entity(object, metaclass=EntityMeta):
    class META:
        subclass = 0

    def __init__(self, tags=None, **kwargs):
        self._tags = tags or Tags()
        for fieldname, field in self._fields().items():
            if fieldname in kwargs:
                setattr(self, fieldname, kwargs.pop(fieldname))
            elif field.default is not None and fieldname not in self._tags:
                setattr(self, fieldname, field.default)

        assert len(kwargs) == 0  # check if there are no additional keyword arguments

    @classmethod
    def _fields(cls):
        # return all fields
        fields = {}
        for key in dir(cls):
            val = getattr(cls, key)
            if isinstance(val, Field):
                fields[key] = val
        return fields

    def get_values(self, key, multiple=False):
        values = [tag.value for tag in self._tags if tag.key == key]
        if multiple:
            return values
        elif len(values):
            return values[0]
        else:
            return None

    def set_values(self, key, values, subclass=0, multiple=False):
        self._tags.remove(key)
        if not multiple:
            values = [values]
        self._tags.insert([Tag(key, value) for value in values], subclass)

    def get_handle(self):
        """
        get handle property
        """
        handle = self.get_values(100) + self.get_values(105)
        return handle[0]







class Circle(Entity):
    r = Point3D(10, default=[1,2])

a = Circle()
print("a", a, a.r)
print("r", Circle.r)
Circle.r = Point2D(10,[1,3])
print("r", Circle.r, Circle.r.default)
a.r = [10,2]
b = Circle()
b.r= [1,2]
print("a", a.r)
print("b",b.r)
b.r=[2,3]
c=Circle()
print(b.r)
print(a.r)


# '(.*)': (DXFAttr.*\)),(.*)



