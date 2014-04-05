#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test generic wrapper
# Created: 22.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals

import unittest

from ezdxf.testtools import ClassifiedTags, DXFStructureError, DXFAttr, DXFAttributes, DefSubclass
from ezdxf.entity import GenericWrapper


class PointAccessor(GenericWrapper):
    DXFATTRIBS = DXFAttributes(DefSubclass(None, {
        'point': DXFAttr(10, 'Point3D'),
        'flat': DXFAttr(11, 'Point2D'),
        'xp': DXFAttr(12, 'Point3D'),
        'flex': DXFAttr(13, 'Point2D/3D'),
        'flags': DXFAttr(70, None),
    }))


class TestGenericWrapper(unittest.TestCase):
    def test_supports_dxfattrib(self):
        tags = ClassifiedTags.from_text("10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertTrue(point.supports_dxf_attrib('xp'))

    def test_supports_dxfattrib(self):
        tags = ClassifiedTags.from_text("10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertFalse(point.supports_dxf_attrib('mozman'))

    def test_getdxfattr_default(self):
        tags = ClassifiedTags.from_text("10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertEqual(17, point.get_dxf_attrib('flags', 17))

    def test_getdxfattr_exist(self):
        tags = ClassifiedTags.from_text("70\n9\n10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertEqual(9, point.get_dxf_attrib('flags', 17))

    def test_dxfattr_exists(self):
        tags = ClassifiedTags.from_text("70\n9\n10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertTrue(point.dxf_attrib_exists('flags'))

    def test_dxfattr_doesnt_exist(self):
        tags = ClassifiedTags.from_text("70\n9\n10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertFalse(point.dxf_attrib_exists('xp'))

    def test_value_error(self):
        tags = ClassifiedTags.from_text("10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        with self.assertRaises(ValueError):
            point.dxf.flags

    def test_attribute_error(self):
        tags = ClassifiedTags.from_text("10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        with self.assertRaises(AttributeError):
            point.dxf.xflag

    def test_valid_dxf_attrib_names(self):
        tags = ClassifiedTags.from_text("10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertEqual(['flags', 'flat', 'flex', 'point', 'xp'], sorted(point.valid_dxf_attrib_names()))

    def test_set_and_get_dxfattrib(self):
        tags = ClassifiedTags.from_text("10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        point.dxf.flags = 7
        self.assertEqual(7, point.dxf.flags)

    def test_delete_simple_dxfattrib(self):
        tags = ClassifiedTags.from_text("70\n7\n10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertEqual(7, point.dxf.flags)
        del point.dxf.flags
        self.assertFalse(point.dxf_attrib_exists('flags'))

    def test_delete_xtype_dxfattrib(self):
        tags = ClassifiedTags.from_text("70\n7\n10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertEqual((1.0, 2.0, 3.0), point.dxf.point)
        del point.dxf.point
        self.assertFalse(point.dxf_attrib_exists('point'))
        # low level check
        point_tags = [tag for tag in point.tags.noclass if tag.code in (10, 20, 30)]
        self.assertEqual(0, len(point_tags))

    def test_delete_not_supported_dxfattrib(self):
        tags = ClassifiedTags.from_text("70\n7\n10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        with self.assertRaises(AttributeError):
            del point.dxf.mozman

    def test_set_not_existing_3D_point(self):
        tags = ClassifiedTags.from_text("70\n7\n10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertFalse(point.dxf_attrib_exists('xp'))
        point.dxf.xp = (7, 8, 9)
        self.assertEqual((7, 8, 9), point.dxf.xp)

    def test_set_not_existing_3D_point_with_wrong_axis_count(self):
        tags = ClassifiedTags.from_text("70\n7\n10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertFalse(point.dxf_attrib_exists('xp'))
        with self.assertRaises(ValueError):
            point.dxf.xp = (7, 8)

    def test_set_not_existing_flex_point_as_3D(self):
        tags = ClassifiedTags.from_text("70\n7\n10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertFalse(point.dxf_attrib_exists('flex'))
        point.dxf.flex = (7, 8, 9)
        self.assertEqual((7, 8, 9), point.dxf.flex)

    def test_set_not_existing_flex_point_as_2D(self):
        tags = ClassifiedTags.from_text("70\n7\n10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertFalse(point.dxf_attrib_exists('flex'))
        point.dxf.flex = (7, 8)
        self.assertEqual((7, 8), point.dxf.flex)

class TestPoint3D(unittest.TestCase):
    def test_get_3d_point(self):
        tags = ClassifiedTags.from_text("10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        self.assertEqual((1., 2., 3.), point.dxf.point)

    def test_error_get_2d_point_for_required_3d_point(self):
        tags = ClassifiedTags.from_text("10\n1.0\n20\n2.0\n")
        point = PointAccessor(tags)
        with self.assertRaises(DXFStructureError):
            point.dxf.point

    def test_set_point(self):
        tags = ClassifiedTags.from_text("10\n1.0\n20\n2.0\n30\n3.0\n")
        point = PointAccessor(tags)
        point.dxf.point = (7, 8, 9)
        self.assertEqual(3, len(tags.noclass))
        self.assertEqual((7., 8., 9.), point.dxf.point)

    def test_error_only_2_axis_exists(self):
        tags = ClassifiedTags.from_text("10\n1.0\n20\n2.0\n70\n0\n")
        point = PointAccessor(tags)
        with self.assertRaises(DXFStructureError):
            point.dxf.point = (7, 8, 9)

    def test_error_only_1_axis_exists(self):
        tags = ClassifiedTags.from_text("10\n1.0\n70\n0\n")
        point = PointAccessor(tags)
        with self.assertRaises(DXFStructureError):
            point.dxf.point = (7, 8, 9)

    def test_get_3d_point_shift(self):
        tags = ClassifiedTags.from_text("12\n1.0\n22\n2.0\n32\n3.0\n")
        point = PointAccessor(tags)
        self.assertEqual((1., 2., 3.), point.dxf.xp)

    def test_error(self):
        tags = ClassifiedTags.from_text("12\n1.0\n22\n2.0\n32\n3.0\n")
        point = PointAccessor(tags)
        with self.assertRaises(ValueError):
            point.dxf.point


class TestPoint2D(unittest.TestCase):
    def test_get_2d_point(self):
        point = PointAccessor(ClassifiedTags.from_text("11\n1.0\n21\n2.0\n40\n3.0\n"))
        self.assertEqual((1., 2.), point.dxf.flat)

    def test_error_get_2d_point_form_3d_point(self):
        point = PointAccessor(ClassifiedTags.from_text("11\n1.0\n21\n2.0\n31\n3.0\n"))
        with self.assertRaises(DXFStructureError):
            point.dxf.flat

    def test_set_2d_point(self):
        point = PointAccessor(ClassifiedTags.from_text("11\n1.0\n21\n2.0\n40\n3.0\n"))
        point.dxf.flat = (4, 5)
        self.assertEqual(3, len(point.tags.noclass))
        self.assertEqual((4., 5.), point.dxf.flat)

    def test_error_set_2d_point_at_existing_3d_point(self):
        point = PointAccessor(ClassifiedTags.from_text("11\n1.0\n21\n2.0\n31\n3.0\n"))
        with self.assertRaises(DXFStructureError):
            point.dxf.flat = (4, 5)


class TestFlexPoint(unittest.TestCase):
    def test_get_2d_point(self):
        tags = ClassifiedTags.from_text("13\n1.0\n23\n2.0\n")
        point = PointAccessor(tags)
        self.assertEqual((1., 2.), point.dxf.flex)

    def test_get_3d_point(self):
        tags = ClassifiedTags.from_text("13\n1.0\n23\n2.0\n33\n3.0\n")
        point = PointAccessor(tags)
        self.assertEqual((1., 2., 3.), point.dxf.flex)

    def test_error_get_1d_point(self):
        point = PointAccessor(ClassifiedTags.from_text("13\n1.0\n"))
        with self.assertRaises(DXFStructureError):
            point.dxf.flex

    def test_set_2d_point(self):
        tags = ClassifiedTags.from_text("13\n1.0\n23\n2.0\n")
        point = PointAccessor(tags)
        point.dxf.flex = (3., 4.)
        self.assertEqual(2, len(tags.noclass))
        self.assertEqual((3., 4.), point.dxf.flex)

    def test_set_3d_point(self):
        tags = ClassifiedTags.from_text("13\n1.0\n23\n2.0\n40\n0.0\n")
        point = PointAccessor(tags)
        point.dxf.flex = (3., 4., 5.)
        self.assertEqual(4, len(tags.noclass))
        self.assertEqual((3., 4., 5.), point.dxf.flex)

    def test_set_2d_point_at_existing_3d_point(self):
        tags = ClassifiedTags.from_text("13\n1.0\n23\n2.0\n33\n3.0\n")
        point = PointAccessor(tags)
        point.dxf.flex = (3., 4.)
        self.assertEqual(2, len(tags.noclass))
        self.assertEqual((3., 4.), point.dxf.flex)

    def test_error_set_point_dxf_structure_error(self):
        tags = ClassifiedTags.from_text("13\n1.0\n40\n0.0\n")
        point = PointAccessor(tags)
        with self.assertRaises(DXFStructureError):
            point.dxf.flex = (3., 4., 5.)

    def test_error_set_point_with_wrong_axis_count(self):
        tags = ClassifiedTags.from_text("13\n1.0\n23\n2.0\n40\n0.0\n")
        point = PointAccessor(tags)
        with self.assertRaises(ValueError):
            point.dxf.flex = (3., 4., 5., 6.)
        with self.assertRaises(ValueError):
            point.dxf.flex = (3., )


if __name__ == '__main__':
    unittest.main()