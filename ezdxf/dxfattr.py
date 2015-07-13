# Copyright (C) 2011, Manfred Moitzi
# License: MIT License

from __future__ import unicode_literals
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


class SubClassedDXFAttr(DXFAttr):
    def __init__(self, code, xtype, subclass, default, dxfversion):
        self.subclass = subclass
        super(SubClassedDXFAttr, self).__init__(code, xtype, default, dxfversion)


class DXFMeta(type):
    def __new__(cls, name, parents, dct):
        dct["_parent"] = []

        def add_parent(parent):
            dct["_parent"].append(parent)
            #for key, value in parent.items():
            #    dct[key] = value

        for p in parents:
            add_parent(p)
        print("jo", name)
        res = super(DXFMeta, cls).__new__(cls, name, parents, dct)
        print("meta", res)
        return res


class DXFAttributes(metaclass=DXFMeta):
    @classmethod
    def __getitem__(self, name):
        return getattr(self, name)

    def __contains__(self, name):
        return name in self.keys()

    @classmethod
    def keys(cls):
        return [key for key in dir(cls) if not key.startswith("_")]


    @classmethod
    def items(cls):
        return [(key, getattr(cls, key)) for key in cls.keys()]
