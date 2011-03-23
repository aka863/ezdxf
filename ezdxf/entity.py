#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: entity module
# Created: 11.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from .tags import Tags, casttagvalue, DXFTag, DXFStructureError

class GenericWrapper:
    TEMPLATE = ""
    CODE = {
        'handle': 5,
    }
    def __init__(self, tags):
        self.tags = tags

    @classmethod
    def new(cls, handle, attribs=None, dxffactory=None):
        if cls.TEMPLATE == "":
            raise NotImplementedError("new() for type %s not implemented." % cls.__name__)
        entity = cls(Tags.fromtext(cls.TEMPLATE))
        entity.handle = handle
        if attribs is not None:
            entity.update(attribs)
        return entity

    def __getattr__(self, key):
        if key in self.CODE:
            code = self.CODE[key]
            if isinstance(code, tuple):
                return self._get_extended_type(code)
            else:
                return self.tags.getvalue(code)
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key in self.CODE:
            code = self.CODE[key]
            if isinstance(code, tuple):
                self._set_extended_type(code, value)
            else:
                self._settag(code, value)
        else:
            super(GenericWrapper, self).__setattr__(key, value)

    def _settag(self, code, value):
        self.tags.new_or_update(code, casttagvalue(code, value))

    def update(self, attribs):
        for key, value in attribs.items():
            self._settag(self.CODE[key], value)

    def _set_extended_type(self, extcode, value):
        def set_point(code, axis):
            if len(value) != axis:
                raise ValueError('%d axis required' % axis)
            self._set_point(code, value)

        code, type_ = extcode
        if type_ == 'Point2D':
            set_point(code, axis=2)
        elif type_ == 'Point3D':
            set_point(code, axis=3)
        elif type_ == 'Point2D/3D':
            self._set_flexible_point(code, value)
        else:
            raise TypeError('Unknown extended type: %s' % type_)

    def _set_point(self, code, value):
        def settag(index, tag):
            if self.tags[index].code == tag.code:
                self.tags[index] = tag
            else:
                raise DXFStructureError('DXF coordinate error')
        index = self.tags.findfirst(code)
        for x, coord in enumerate(value):
            settag(index + x, DXFTag(code + x*10, float(coord)))

    def _set_flexible_point(self, code, value):
        def insert_tag_if_required(pos, axiscode):
            if len(self.tags) <= pos or self.tags[pos]!= axiscode:
                self.tags.insert(pos, DXFTag(axiscode, 0.0))

        def extend_point(axis):
            index = self.tags.findfirst(code)
            for x in range(axis):
                insert_tag_if_required(index+x, code + x*10)

        axis = len(value)
        if axis not in (2, 3):
            raise ValueError("2D or 3D point required (tuple).")
        extend_point(axis)
        self._set_point(code, value)


    def _get_extended_type(self, extcode):
        code, type_ = extcode
        if type_ == 'Point2D':
            return self._point(code, axis=2)
        elif type_ == 'Point3D':
            return self._get_point(code, axis=3)
        elif type_ == 'Point2D/3D':
            return self._get_flexible_point(code)
        else:
            raise TypeError('Unknown extended type: %s' % type_)

    def _get_point(self, code, axis):
        index = self.tags.findfirst(code)
        coords = []
        for x in range(axis):
            try:
                tag = self.tags[index + x]
            except IndexError:
                raise DXFStructureError('DXF coordinate error')
            if tag.code != code + x*10:
                raise DXFStructureError('DXF coordinate error')
            coords.append(tag.value)
        return tuple(coords)

    def _get_flexible_point(self, code):
        try:
            return self._get_point(code, axis=3)
        except DXFStructureError:
            return self._get_point(code, axis=2)



