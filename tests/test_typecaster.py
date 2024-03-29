#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test type caster
# Created: 10.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals

import unittest

from ezdxf.tags import cast_tag


class TestTypeCaster(unittest.TestCase):
    def test_cast_string(self):
        result = cast_tag((1, 'STRING'))
        self.assertEqual((1, 'STRING'), result)

    def test_cast_float(self):
        result = cast_tag((10, ('1', '2', '3')))
        self.assertEqual((10, (1, 2, 3)), result)

    def test_cast_int(self):
        result = cast_tag((60, '4711'))
        self.assertEqual((60, 4711), result)

    def test_cast_bool_True(self):
        result = cast_tag((290, '1'))
        self.assertEqual((290, 1), result)

    def test_cast_bool_False(self):
        result = cast_tag((290, '0'))
        self.assertEqual((290, 0), result)

    def test_cast_2d_point(self):
        result = cast_tag((10, ('1', '2')))
        self.assertEqual((10, (1, 2)), result)

    def test_cast_3d_point(self):
        result = cast_tag((10, ('1', '2', '3')))
        self.assertEqual((10, (1, 2, 3)), result)

if __name__ == '__main__':
    unittest.main()