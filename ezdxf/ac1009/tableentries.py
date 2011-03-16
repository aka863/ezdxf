#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: ac1009 tableentries
# Created: 16.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

from ..tags import casttagvalue

class TableEntry:
    def __init__(self, tags, handle):
        # __init__ is also the wrapper interface!
        assert tags[0] == (0, 'LAYER')
        self.tags = tags
        self.update_handle(handle)

    def update_handle(self, handle):
        try:
            self.tags.update(5, handle)
        except ValueError:
            # for AC1009: handles must not be present
            # important insert as second tag
            self.tags.insert(1, (5, handle))

    def __getattr__(self, key):
        if key in self.CODE:
            return self.tags.getvalue(self.CODE[key])
        else:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if key in self.CODE:
            self._set_tag(key, value)
        else:
            super(TableEntry, self).__setattr__(key, value)

    def _set_tag(self, key, value):
        code = self.CODE[key]
        self.tags.new_or_update(code, casttagvalue(code, value))

    def update(self, attribmap):
        for key, value in attribmap.items():
            self._set_tag(key, code)

_LAYERTEMPLATE = """  0
LAYER
  5
XXXX
  2
DEFAULT
 70
     0
 62
     7
  6
CONTINUOUS
"""

LAYER_LOCK = 0b00000100
LAYER_UNLOCK = 0b11111011

class Layer(TableEntry):
    TEMPLATE = _LAYERTEMPLATE
    CODE = {
        'handle': 5,
        'name': 2, # layer name
        'flags': 70,
        'color': 62, # dxf color index, if < 0 layer is off
        'linetype': 6, # linetype name
    }

    def is_locked(self):
        return self.flags & LAYER_LOCK > 0
    def lock(self):
        self.flags = self.flags | LAYERLOCK
    def unlock(self):
        self.flags = self.flags & LAYERUNLOCK

    def is_off(self):
        return self.color < 0
    def is_on(self):
        return not self.is_off()
    def on(self):
        self.color = abs(self.color)
    def off(self):
        self.color = -(abs(self.color))

    def get_color(self):
        return abs(self.color)
    def set_color(self, color):
        sign = -1 if self.color < 0 else 1
        self.color = color * sign


"""
ATTRIBUTES = {
    'LTYPE': {
        'name': AttribDef(DXFString, 2, priority=52),
        'flags': AttribDef(DXFInt, 70, priority=53),
        'description': AttribDef(DXFString, 3, priority=101),
        'pattern': AttribDef(PassThroughFactory, priority=102),
        },
    'STYLE': {
        'name': AttribDef(DXFString, 2, priority=52),
        'flags': AttribDef(DXFInt, 70, priority=53),
        'height': AttribDef(DXFFloat, 40, priority=101),
        'width': AttribDef(DXFFloat, 41, priority=102),
        'last_height': AttribDef(DXFFloat, 42, priority=103),
        'oblique': AttribDef(DXFAngle, 50, priority=104),
        'generation_flags': AttribDef(DXFInt, 71, priority=105),
        'font': AttribDef(DXFString, 3, priority=106),
        'bigfont': AttribDef(DXFString, 4, priority=107),
        },
    'VIEW': {
        'name': AttribDef(DXFString, 2, priority=52),
        'flags': AttribDef(DXFInt, 70, priority=53),
        'height': AttribDef(DXFFloat, 40, priority=101),
        'width': AttribDef(DXFFloat, 41, priority=102),
        'center_point': AttribDef(DXFPoint2D, 0, priority=103),
        'direction_point': AttribDef(DXFPoint3D, 1, priority=104),
        'target_point': AttribDef(DXFPoint3D, 2, priority=105),
        'lens_length': AttribDef(DXFFloat, 42, priority=106),
        'front_clipping': AttribDef(DXFFloat, 43, priority=107),
        'back_clipping': AttribDef(DXFFloat, 44, priority=108),
        'view_twist': AttribDef(DXFAngle, 50, priority=109),
        'view_mode': AttribDef(DXFInt, 71, priority=110),
        },
    'VPORT': {
        'name': AttribDef(DXFString, 2, priority=52),
        'flags': AttribDef(DXFInt, 70, priority=53),
        'lower_left': AttribDef(DXFPoint2D, 0,priority=101),
        'upper_right': AttribDef(DXFPoint2D, 1, priority=102),
        'center_point': AttribDef(DXFPoint2D, 2, priority=103),
        'snap_base': AttribDef(DXFPoint2D, 3, priority=104),
        'snap_spacing': AttribDef(DXFPoint2D, 4, priority=105),
        'grid_spacing': AttribDef(DXFPoint2D, 5, priority=106),
        'direction_point': AttribDef(DXFPoint3D, 6, priority=107),
        'target_point': AttribDef(DXFPoint3D, 7, priority=108),
        'height': AttribDef(DXFFloat, 40, priority=112),
        'aspect_ratio': AttribDef(DXFFloat, 41, priority=113),
        'lens_length': AttribDef(DXFFloat, 42, priority=109),
        'front_clipping': AttribDef(DXFFloat, 43, priority=110),
        'back_clipping': AttribDef(DXFFloat, 44, priority=111),
        'snap_rotation': AttribDef(DXFAngle, 50, priority=115),
        'view_twist': AttribDef(DXFAngle, 51, priority=116),
        'status': AttribDef(DXFInt, 68, priority=117),
        'id': AttribDef(DXFInt, 69, priority=118),
        'view_mode': AttribDef(DXFInt, 71, priority=122),
        'circle_zoom': AttribDef(DXFInt, 72, priority=123),
        'fast_zoom': AttribDef(DXFInt, 73, priority=124),
        'ucs_icon': AttribDef(DXFInt, 74, priority=126),
        'snap_on': AttribDef(DXFInt, 75, priority=127),
        'grid_on': AttribDef(DXFInt, 76, priority=128),
        'snap_style': AttribDef(DXFInt, 77, priority=129),
        'snap_isopair': AttribDef(DXFInt, 78, priority=130)
        },
    'APPID': {
        'name': AttribDef(DXFString, 2, priority=52),
        'flags': AttribDef(DXFInt, 70, priority=53),
        },
    'UCS': {
        'name': AttribDef(DXFString, 2, priority=52),
        'flags': AttribDef(DXFInt, 70, priority=53),
        'origin': AttribDef(DXFPoint3D, 0,priority=101),
        'xaxis': AttribDef(DXFPoint3D, 1, priority=102),
        'yaxis': AttribDef(DXFPoint3D, 2, priority=103),
        },
    }

"""