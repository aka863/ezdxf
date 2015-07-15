from ezdxf.entity_new.entity import Entity
from ezdxf.entity_new import fields


class GraphicsEntity(Entity):
    handle = fields.Hex(8)
    owner = fields.Field(2)


class Circle(Entity):
    _subclasses = [
        "first",
        "second",
        "third"
    ]

    position = fields.Point2D(10, default=[0, 0])
    r = fields.Field(8, default=0)


if __name__ == "__main__":
    c=Circle()
    print(list(c._tags))
    c.r = 10
    c.position = [1,2]
    print(list(c._tags))
