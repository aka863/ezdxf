from ezdxf.entity_new.fields import Field
from ezdxf.entity_new.tags import TagContainer, Tag


class EntityMeta(type):
    def __new__(cls, name, parent, dct):
        """
        Set subclass index on entity/fields
        """
        meta = dct.get("META", object)

        # get current subclass index
        subclass = getattr(meta, "subclass", None)
        if subclass is None:
            subclass = getattr(parent[0], "_subclass")

        dct["_subclass"] = subclass
        for key, value in dct.items():
            if isinstance(value, Field):
                dct[key].subclass = subclass

        res = super(EntityMeta, cls).__new__(cls, name, parent, dct)

        return res


class Entity(object, metaclass=EntityMeta):
    class META:
        subclass = 0

    def __init__(self, **kwargs):
        self._tags = TagContainer()
        for fieldname, field in self._fields().items():
            if fieldname in kwargs:
                setattr(self, fieldname, kwargs.pop(fieldname))
            elif field.default is not None and fieldname not in self._tags:
                setattr(self, fieldname, field.default)

        assert len(kwargs) == 0  # check if there are no additional keyword arguments

    @classmethod
    def from_tags(cls, tags):
        instance = cls()
        instance._tags = tags

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
        handle = self.get_values(100, multiple=True) + self.get_values(105, multiple=True)
        return handle[0]

    def write(self, stream):
        """
        Write entity tags to output stream
        """
        for tag in self._tags:
            tag.write(stream)

    def copy(self):
        tags = [tag.copy() for tag in self._tags]
        instance = self.from_tags(tags)
        # todo:
        # instance.handle = None
        return instance


# '(.*)': (DXFAttr.*\)),(.*)



