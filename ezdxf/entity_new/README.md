Entities
========

In dxf entities consist of several key-value attributes.
Here is an example for a (2D-) Polyline going from [0,0,0] to [100, 100, 100]:
```
 0
LINE
 8
2
 62
4
 10
0
 20
0
 30
0
 11
100
 21
100
 31
100
```

When using the BaseEntity class, those attributes are parsed as DXFTags (key-value namedtuples) and kept in
the class' `_tags` attribute.

To simplify access one can use a orm-like attribute declaration using field-properties.
In this example the Line class would look like this:

```
class Line(BaseEntity):
    handle = HEXField(5)
    owner = Field(8)
    something = Field(62)
    from = Point3D(10)
    to = Point3D(11)
```

Then those attributes are available as attributes like so:

```
line = Line(from=[0,0,0])
line.to = [0,0,0]
```

Setting a wrong attribute fails due to validation

```
>>> line = Line(from=[0,0,0])
>>> line.to = -1
Traceback (most recent call last):
  File "ezdxf/entity_new/fields.py", line 24, in __set__
0 10 (10, 20)
    self.validate(value)
  File "ezdxf/entity_new/fields.py", line 50, in validate
    assert len(value) == 2
TypeError: object of type 'int' has no len()

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "entity_new/fields.py", line 30, in __set__
    raise ValueError("Invalid Value {} on field {}/{}".format(value, instance, fieldname))
ValueError: Invalid Value -1 on field <__main__.Circle object at 0x7f0e8d3882b0>/position
```