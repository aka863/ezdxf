# Copyright (C) 2011, Manfred Moitzi
# License: MIT License

from __future__ import unicode_literals
import copy

__author__ = "mozman <mozman@gmx.at>"

from collections import namedtuple

DefSubclass = namedtuple('DefSubclass', 'name attribs')


# *dxfversion* == None - valid for all supported DXF versions managed by the dxffactory:
# dxffactory AC1009 - manages just DXF version AC1009, but dxffactory AC1015 manages the DXF version AC1015 and all
# later DXF versions! Set *dxfversion* to 'AC1018' and this attribute can only be set in drawings with DXF version
# AC1018 or later.
class DXFAttr(object):
    def __init__(self, code, xtype=None, default=None, dxfversion=None):
        self.code = code
        self.xtype = xtype
        self.default = default
        self.dxfversion = dxfversion
        self.subclass = 0


class SubClassedDXFAttr(DXFAttr):
    def __init__(self, code, xtype, subclass, default, dxfversion):
        self.subclass = subclass
        super(SubClassedDXFAttr, self).__init__(code, xtype, default, dxfversion)


class DXFMeta(type):
    def __new__(cls, name, parents, dct):
        META = dct.pop("META", None)

        dct["_parent"] = parents
        assert len(parents) <= 1

        subclass = -1
        if parents:
            subclass = getattr(parents[0], "_subclass", -1)
            #subclass = max([getattr(field, "subclass", 0) for field in parents[0].values()], default=-1)

        if getattr(META, "add_subclass", True):
            subclass += 1

        dct["_subclass"] = subclass
        for key, value in dct.items():
            if isinstance(value, DXFAttr):
                dct[key] = copy.copy(value)
                dct[key].subclass = subclass

        res = super(DXFMeta, cls).__new__(cls, name, parents, dct)
        return res


class DXFAttributes(metaclass=DXFMeta):
    class META:
        add_subclass = False

    @classmethod
    def __getitem__(cls, name):
        return getattr(cls, name)

    def __contains__(self, name):
        return name in self.keys()

    @classmethod
    def __iter__(cls):
        return iter(cls.values())

    @classmethod
    def keys(cls):
        exclude = ["keys", "items", "values"]
        return [key for key in dir(cls) if not key.startswith("_") and not key in exclude]


    @classmethod
    def items(cls):
        return [(key, getattr(cls, key)) for key in cls.keys()]

    @classmethod
    def values(cls):
        return [getattr(cls, key) for key in cls.keys()]
