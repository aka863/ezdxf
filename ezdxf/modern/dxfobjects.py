# Purpose: dxf objects wrapper, dxf-objects are non-graphical entities
# all dxf objects resides in the OBJECTS SECTION
# Created: 22.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT-License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from contextlib import contextmanager

from ..tags import DXFTag
from ..classifiedtags import ClassifiedTags
from ..dxfattr import DXFAttr, DXFAttributes, DefSubclass
from ..dxfentity import DXFEntity
from ..c23 import isstring

ENTRY_NAME_CODE = 3

none_subclass = DefSubclass(None, {
    'handle': DXFAttr(5),
    'owner': DXFAttr(330),
})


class DXFDictionary(DXFEntity):
    DXFATTRIBS = DXFAttributes(
        none_subclass,
        DefSubclass('AcDbDictionary', {
            'hard_owned': DXFAttr(280),
            'cloning': DXFAttr(281),
        }),
    )

    @property
    def AcDbDictinary(self):
        return self.tags.subclasses[1]

    def keys(self):
        """Generator for the dictionary's keys.
        """
        return (item[0] for item in self.items())

    def items(self):
        """Generator for the dictionary's items (``(key, value)`` pairs).
        """
        for code, value in self.AcDbDictinary:
            if code == ENTRY_NAME_CODE:  # Entry name
                key = value
            elif code == 350:  # handle to entry object
                yield key, value

    def __getitem__(self, key):
        """Return the value for *key* if *key* is in the dictionary, else raises a :class:`KeyError()`.
        """
        return self.get(key)

    def __setitem__(self, key, value):
        """Add item *(key, value)* to dictionary.
        """
        return self.add(key, value)

    def __delitem__(self, key):
        """Remove element *key* from the dictionary. *KeyError* if *key* is not contained in the
        dictionary.
        """
        return self.remove(key)

    def __contains__(self, key):
        """Return *True* if the dictionary has a key *key*, else *False*.
        """
        return False if self._get_item_index(key) is None else True

    def __len__(self):
        """Return the number of items in the dictionary.
        """
        return self.count()

    def count(self):
        """Return the number of items in the dictionary.
        """
        return sum(1 for tag in self.AcDbDictinary if tag.code == ENTRY_NAME_CODE)

    def get(self, key, default=KeyError):
        """Return the value for *key* if *key* is in the dictionary, else *default*. If *default* is not given, it
        defaults to :class:`KeyError()`, so that this method raises a *KeyError*.
        """
        index = self._get_item_index(key)
        if index is None:
            if default is KeyError:
                raise KeyError("KeyError: '{}'".format(key))
            else:
                return default
        else:
            return self.AcDbDictinary[index + 1].value

    def add(self, key, value, code=350):
        """Add item ``(key, value)`` to dictionary. The key parameter *code* specifies the group code of the *value*
        data and defaults to ``350`` (soft-owner handle).
        """
        index = self._get_item_index(key)
        value_tag = DXFTag(code, value)
        content_tags = self.AcDbDictinary
        if index is None:  # create new entry
            content_tags.append(DXFTag(ENTRY_NAME_CODE, key))
            content_tags.append(value_tag)
        else:  # always replace existing values, until I understand the 281-tag (name mangling)
            content_tags[index + 1] = value_tag

    def remove(self, key):
        """Remove element *key* from the dictionary. Raises *KeyError* if *key* is not contained in the
        dictionary.
        """
        index = self._get_item_index(key)
        if index is None:
            raise KeyError("KeyError: '{}'".format(key))
        else:
            self._discard(index)

    def discard(self, key):
        """Remove *key* from the dictionary if it is present.
        """
        self._discard(self._get_item_index(key))

    def _discard(self, index):
        if index:
            del self.AcDbDictinary[index:index+1]

    def _get_item_index(self, key):
        for index, tag in enumerate(self.AcDbDictinary):
            if tag.code == ENTRY_NAME_CODE and tag.value == key:
                return index
        return None

    def clear(self):
        try:
            start_index = self.AcDbDictinary.tag_index(code=ENTRY_NAME_CODE)
        except ValueError:  # no entries found
            return
        del self.AcDbDictinary[start_index:]


class DXFDictionaryWithDefault(DXFDictionary):
    DXFATTRIBS = DXFAttributes(
        none_subclass,
        DefSubclass('AcDbDictionary', {
            'hard_owned': DXFAttr(280),
            'cloning': DXFAttr(281),
        }),
        DefSubclass('AcDbDictionaryWithDefault', {
            'default': DXFAttr(340),
        }),
    )

    def get(self, key, default=KeyError):
        """Return the value for *key* if *key* is in the dictionary, else the predefined dictionary wide *default*
        value. Parameter *default* is always ignored!
        """
        return super(DXFDictionaryWithDefault, self).get(key, default=self.dxf.default)


plot_settings_subclass = DefSubclass('AcDbPlotSettings', {
    'page_setup_name': DXFAttr(1),
    'plot_configuration_file': DXFAttr(2),
    'paper_size': DXFAttr(4),
    'plot_view_name': DXFAttr(6),
    'left_margin': DXFAttr(40),  # in mm
    'bottom_margin': DXFAttr(41),  # in mm
    'right_margin': DXFAttr(42),  # in mm
    'top_margin': DXFAttr(43),  # in mm
    'paper_width': DXFAttr(44),  # in mm
    'paper_height': DXFAttr(45),  # in mm
    'plot_origin_x_offset': DXFAttr(46),  # in mm
    'plot_origin_y_offset': DXFAttr(47),  # in mm
    'plot_window_x1': DXFAttr(48),
    'plot_window_y1': DXFAttr(49),
    'plot_window_x2': DXFAttr(140),
    'plot_window_y2': DXFAttr(141),
    'custom_print_scale_numerator': DXFAttr(142),  # Numerator of custom print scale: real world (paper) units
    'custom_print_scale_denominator': DXFAttr(142),  # Denominator of custom print scale: drawing units
    'plot_layout_flags': DXFAttr(70),
        # 1 = Plot Viewport Borders
        # 2 = Show Plot Styles
        # 4 = Plot Centered
        # 8 = Plot Hidden
        # 16 = Use Standard Scale
        # 32 = Plot Plot Styles
        # 64 = Scale Lineweights
        # 128 = Print Lineweights
        # 512 = Draw Viewports First
        # 1024 = Model Type
        # 2048 = Update Paper
        # 4096 = Zoom To Paper On Update
        # 8192 = Initializing
        # 16384 = Prev PlotInit
    'plot_paper_units': DXFAttr(72),  # 0 = Plot in inches; 1 = Plot in millimeters; 2 = Plot in pixels
    'plot_rotation': DXFAttr(73),
        # 0 = No rotation
        # 1 = 90 degrees counterclockwise
        # 2 = Upside-down
        # 3 = 90 degrees clockwise
    'plot_type': DXFAttr(74),
        # 0 = Last screen display
        # 1 = Drawing extents
        # 2 = Drawing limits
        # 3 = View specified by code 6
        # 4 = Window specified by codes 48, 49, 140, and 141
        # 5 = Layout information
    'current_style_sheet': DXFAttr(7),
    'standard_scale_type': DXFAttr(75),
        # 0 = Scaled to Fit
        # 1 = 1/128"=1'
        # 2 = 1/64"=1'
        # 3 = 1/32"=1'
        # 4 = 1/16"=1'
        # 5 = 3/32"=1'
        # 6 = 1/8"=1'
        # 7 = 3/16"=1'
        # 8 = 1/4"=1'
        # 9 = 3/8"=1'
        # 10 = 1/2"=1'
        # 11 = 3/4"=1'
        # 12 = 1"=1'
        # 13 = 3"=1'
        # 14 = 6"=1'
        # 15 = 1'=1'
        # 16 = 1:1
        # 17 = 1:2
        # 18 = 1:4
        # 19 = 1:8
        # 20 = 1:10
        # 21 = 1:16
        # 22 = 1:20
        # 23 = 1:30
        # 24 = 1:40
        # 25 = 1:50
        # 26 = 1:100
        # 27 = 2:1
        # 28 = 4:1
        # 29 = 8:1
        # 30 = 10:1
        # 31 = 100:1
        # 32 = 1000:1
    'shade_plot_mode': DXFAttr(76),  # 0 = As Displayed; 1 = Wireframe; 2 = Hidden; 3 = Rendered
    'shade_plot_resolution_level': DXFAttr(77),
        # 0 = Draft
        # 1 = Preview
        # 2 = Normal
        # 3 = Presentation
        # 4 = Maximum
        # 5 = Custom
    'shade_plot_custom_dpi': DXFAttr(78),
    # Valid range: 100 to 32767, Only applied when the shade_plot_resolution level is set to 5 (Custom)
    'scale_factor': DXFAttr(147),
    # A floating point scale factor that represents the standard scale value specified in code 75
    'paper_image_origin_x': DXFAttr(148),
    'paper_image_origin_y': DXFAttr(149),
    'shade_plot_handle': DXFAttr(333),
})


class DXFPlotSettings(DXFEntity):
    DXFATTRIBS = DXFAttributes(none_subclass, plot_settings_subclass)


_LAYOUT_TPL = """  0
LAYOUT
  5
0
102
{ACAD_REACTORS
330
0
102
}
330
1A
100
AcDbPlotSettings
  1

  2
Adobe PDF
  4
A4
  6

 40
3.174999952316284
 41
3.174999952316284
 42
3.175003051757812
 43
3.17498779296875
 44
209.9098358154297
 45
297.0318298339844
 46
0.0
 47
0.0
 48
0.0
 49
0.0
140
0.0
141
0.0
142
1.0
143
1.0
 70
688
 72
0
 73
1
 74
5
  7

 75
16
147
1.0
 76
0
 77
2
 78
300
148
0.0
149
0.0
100
AcDbLayout
  1
Layoutname
 70
1
 71
1
 10
-3.17498779296875
 20
-3.174999952316284
 11
293.8568420410156
 21
206.7348358631134
 12
0.0
 22
0.0
 32
0.0
 14
29.06818420886992
 24
20.35598328113557
 34
0.0
 15
261.6136578798294
 25
183.20384953022
 35
0.0
146
0.0
 13
0.0
 23
0.0
 33
0.0
 16
1.0
 26
0.0
 36
0.0
 17
0.0
 27
1.0
 37
0.0
 76
1
330
0
"""


class DXFLayout(DXFEntity):
    TEMPLATE = ClassifiedTags.from_text(_LAYOUT_TPL)
    DXFATTRIBS = DXFAttributes(
        none_subclass,
        plot_settings_subclass,
        DefSubclass('AcDbLayout', {
            'name': DXFAttr(1),  # layout name
            'layout_flags': DXFAttr(70),
            'taborder': DXFAttr(71),
            'limmin': DXFAttr(10, 'Point2D'),  # minimum limits
            'limmax': DXFAttr(11, 'Point2D'),  # maximum limits
            'insert_base': DXFAttr(12, 'Point3D'),  # Insertion base point for this layout
            'extmin': DXFAttr(14, 'Point3D'),  # Minimum extents for this layout
            'extmax': DXFAttr(15, 'Point3D'),  # Maximum extents for this layout
            'elevation': DXFAttr(146),
            'ucs_origin': DXFAttr(13, 'Point3D'),
            'ucs_xaxis': DXFAttr(16, 'Point3D'),
            'ucs_yaxis': DXFAttr(17, 'Point3D'),
            'ucs_type': DXFAttr(76),
            # Orthographic type of UCS 0 = UCS is not orthographic;
            # 1 = Top; 2 = Bottom; 3 = Front; 4 = Back; 5 = Left; 6 = Right
            'block_record': DXFAttr(330),
            'viewport': DXFAttr(331),
            # ID/handle to the viewport that was last active in this
            # layout when the layout was current
            'ucs': DXFAttr(345),
            # ID/handle of AcDbUCSTableRecord if UCS is a named
            # UCS. If not present, then UCS is unnamed
            'base_ucs': DXFAttr(346),
            #ID/handle of AcDbUCSTableRecord of base UCS if UCS is
            # orthographic (76 code is non-zero). If not present and
            # 76 code is non-zero, then base UCS is taken to be WORLD
        }))

    def post_new_hook(self):
        try:
            acad_reactors = self.tags.get_appdata('{ACAD_REACTORS')
        except ValueError:
            pass
        else:
            acad_reactors.set_first(330, self.dxf.owner)


class XRecord(DXFEntity):
    DXFATTRIBS = DXFAttributes(
        none_subclass,
        DefSubclass('AcDbXrecord', {
            'cloning': DXFAttr(280),
        }),
    )

    @property
    def content_tags(self):
        return self.tags.get_subclass('AcDbXrecord')

    @staticmethod
    def _adjust_index(index):
        return index if index < 0 else index + 2

    def __len__(self):
        # ignore first tags = (100, 'AcDbXrecord'), (280, ...)
        return len(self.content_tags) - 2

    def __getitem__(self, index):
        """Returns DXF tag at position *index*.
        """
        # skip first tags = (100, 'AcDbXrecord'), (280, ...)
        return self.content_tags[XRecord._adjust_index(index)]

    def __setitem__(self, index, dxftag):
        """Replace DXF tag at position *index* with *dxftag*.
        """
        # skip first tags = (100, 'AcDbXrecord'), (280, ...)
        self.content_tags[XRecord._adjust_index(index)] = dxftag

    def __iter__(self):
        """Iterate over data, yielding DXF tags as named tuple *(code, value)*.
        """
        tags = iter(self.content_tags)
        next(tags)  # skip (100, 'AcDbXrecord')
        next(tags)  # skip (280, ...)
        return tags

    def append(self, dxftag):
        """Append *dxftag* at the end of the tag list.
        """
        self.content_tags.append(dxftag)


class DXFDataTable(DXFEntity):
    DXFATTRIBS = DXFAttributes(
        none_subclass,
        DefSubclass('AcDbDataTable', {
            'version': DXFAttr(70),
            'columns': DXFAttr(90),
            'rows': DXFAttr(91),
            'tabel_name': DXFAttr(1),
        }),
    )

_GROUP_TPL = """  0
GROUP
  5
0
330
0
100
AcDbGroup
300

 70
     1
 71
     1
"""
GROUP_ITEM_CODE = 340

class DXFGroup(DXFEntity):
    TEMPLATE = ClassifiedTags.from_text(_GROUP_TPL)
    DXFATTRIBS = DXFAttributes(
        none_subclass,
        DefSubclass('AcDbGroup', {
            'description': DXFAttr(300),
            'unnamed': DXFAttr(70),
            'selectable': DXFAttr(71),
        }),
    )

    @property
    def AcDbGroup(self):
        return self.tags.subclasses[1]

    def __iter__(self):
        """ Yields all DXF entities of this group as wrapped DXFEntity (LINE, CIRCLE, ...) objects.
        """
        wrap = self.dxffactory.wrap_handle
        for handle in self.handles():
            yield wrap(handle)

    def __len__(self):
        return sum(1 for tag in self.AcDbGroup if tag.code == GROUP_ITEM_CODE)

    def handles(self):
        return (tag.value for tag in self.AcDbGroup if tag.code == GROUP_ITEM_CODE)

    def get_name(self):
        owner_dict = self.dxffactory.wrap_handle(self.dxf.owner)
        my_handle = self.dxf.handle
        for name, handle in owner_dict.items():
            if handle == my_handle:
                return name
        return None

    @contextmanager
    def edit_data(self):
        data = list(self)
        yield data
        self.set_data(data)

    def set_data(self, data):
        self.clear()
        self.AcDbGroup.extend(DXFTag(GROUP_ITEM_CODE, entity.dxf.handle) for entity in data)

    def clear(self):
        self.AcDbGroup.remove_tags((GROUP_ITEM_CODE,))


class DXFGroupTable(object):
    def __init__(self, dxfgroups):
        self.dxfgroups = dxfgroups  # AcDbDictionary
        self.objects_section = dxfgroups.drawing.objects
        self._next_unnamed_number = 0

    def __iter__(self):
        wrap = self.dxfgroups.dxffactory.wrap_handle
        for name, handle in self.dxfgroups.items():
            yield name, wrap(handle)

    def __len__(self):
        return len(self.dxfgroups)

    def __contains__(self, key):
        return key in self.dxfgroups

    def next_name(self):
        name = self._next_name()
        while name in self.dxfgroups:
            name = self._next_name()
        return name

    def _next_name(self):
        self._next_unnamed_number += 1
        return "*A{}".format(self._next_unnamed_number)

    def add(self, name=None, description="", selectable=1):
        if name in self.dxfgroups:
            raise ValueError("Group '{}' already exists. Group name has to be unique.".format(name))
        unnamed = 0
        if name is None:
            name = self.next_name()
            unnamed = 1
        # The group name isn't stored in the group entity itself.
        group = self.objects_section.create_new_dxf_entity("GROUP", dxfattribs={
            'description': description,
            'unnamed': unnamed,
            'selectable': selectable,
        })
        self.dxfgroups[name] = group.dxf.handle  #
        return group

    def get(self, name):
        for group_name, group in self:
            if name == group_name:
                return group
        raise KeyError("KeyError: '{}'".format(name))

    def delete(self, group):
        if isstring(group):  # delete group by name
            name = group
            group_handle = self.dxfgroups[name]
            del self.dxfgroups[name]
        else:  # group should be a DXFEntity
            group_handle = group.dxf.handle
            for name, _group in self:
                if group_handle == _group.dxf.handle:
                    del self.dxfgroups[name]
                    return
            raise ValueError("Group not in group table registered.")
        self._destroy_dxf_group_entity(group_handle)

    def _destroy_dxf_group_entity(self, handle):
        self.objects_section.remove_handle(handle)  # remove from entity space
        self.objects_section.entitydb.delete_handle(handle)  # remove from drawing database

    def clear(self):
        for name, group in self:  # destroy dxf entities
            self._destroy_dxf_group_entity(group.dxf.handle)
        self.dxfgroups.clear()  # delete all references

