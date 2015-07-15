from ezdxf.entity_new.entity import Entity
from ezdxf.entity_new import fields


class GraphicsEntity(Entity):
    handle = fields.Hex(5)
    owner = fields.Field(330)


class Circle(GraphicsEntity):
    _subclasses = [
        "first",
        "second",
        "third"
    ]

    position = fields.Point2D(10, default=[0, 0])
    r = fields.Field(8, default=0)


if __name__ == "__main__":
    c=Circle()
    c.handle = "FF"
    c.owner = 0
    c.r = 10
    c.position = [1,2]
    c.position = (10, 20)
    print(list(c._tags))
    print(c.owner, c.r, c.position)
    c.position = -1

    # outputs:
    # [TAG(key=5, value='FF'), TAG(key=330, value=0), TAG(key=8, value=10), TAG(key=10, value=10), TAG(key=20, value=20)]
    # 0 10 [10, 20]
    # c.handle = "XY" raises ValueError
