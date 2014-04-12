#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test basic graphic entities
# Created: 25.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals

import unittest

import ezdxf


class SetupDrawing(unittest.TestCase):
    def setUp(self):
        self.dwg = ezdxf.new('AC1015')
        self.layout = self.dwg.modelspace()


class TestGraphicsDefaultSettings(SetupDrawing):
    def test_default_settings(self):
        line = self.layout.add_line((0, 0), (1, 1))
        self.assertEqual('0', line.dxf.layer)
        self.assertEqual(256, line.dxf.color)
        self.assertEqual('BYLAYER', line.dxf.linetype)
        self.assertEqual(1.0, line.dxf.ltscale)
        self.assertEqual(0, line.dxf.invisible)
        self.assertEqual((0.0, 0.0, 1.0), line.dxf.extrusion)


class TestBasicEntities(SetupDrawing):
    def test_iter_layout(self):
        self.layout.add_line((0, 0), (1, 1))
        self.layout.add_line((0, 0), (1, 1))
        self.assertEqual(2, len(list(self.layout)))

    def test_create_line(self):
        line = self.layout.add_line((0, 0), (1, 1))
        self.assertEqual((0., 0.), line.dxf.start)
        self.assertEqual((1., 1.), line.dxf.end)

    def test_create_circle(self):
        circle = self.layout.add_circle((3, 3), 5)
        self.assertEqual((3., 3.), circle.dxf.center)
        self.assertEqual(5., circle.dxf.radius)

    def test_create_arc(self):
        arc = self.layout.add_arc((3, 3), 5, 30, 60)
        self.assertEqual((3., 3.), arc.dxf.center)
        self.assertEqual(5., arc.dxf.radius)
        self.assertEqual(30., arc.dxf.start_angle)
        self.assertEqual(60., arc.dxf.end_angle)

    def test_create_trace(self):
        trace = self.layout.add_trace([(0, 0), (1, 0), (1, 1), (0, 1)])
        self.assertEqual((0, 0), trace[0])
        self.assertEqual((1, 0), trace.dxf.vtx1)
        self.assertEqual((1, 1), trace[2])
        self.assertEqual((0, 1), trace.dxf.vtx3)

    def test_create_solid(self):
        trace = self.layout.add_solid([(0, 0), (1, 0), (1, 1)])
        self.assertEqual((0, 0), trace.dxf.vtx0)
        self.assertEqual((1, 0), trace[1])
        self.assertEqual((1, 1), trace.dxf.vtx2)
        self.assertEqual((1, 1), trace[3])

    def test_create_3dface(self):
        trace = self.layout.add_3Dface([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
        self.assertEqual((0, 0, 0), trace.dxf.vtx0)
        self.assertEqual((1, 0, 0), trace[1])
        self.assertEqual((1, 1, 0), trace.dxf.vtx2)
        self.assertEqual((0, 1, 0), trace[3])

    def test_create_text(self):
        text = self.layout.add_text('text')
        self.assertEqual('text', text.dxf.text)


class TestText(SetupDrawing):
    def test_create_text(self):
        text = self.layout.add_text('text')
        self.assertEqual('text', text.dxf.text)

    def test_set_alignment(self):
        text = self.layout.add_text('text')
        text.set_pos((2, 2), align="TOP_CENTER")
        self.assertEqual(1, text.dxf.halign)
        self.assertEqual(3, text.dxf.valign)
        self.assertEqual((2, 2), text.dxf.align_point)

    def test_set_fit_alignment(self):
        text = self.layout.add_text('text')
        text.set_pos((2, 2), (4, 2), align="FIT")
        self.assertEqual(5, text.dxf.halign)
        self.assertEqual(0, text.dxf.valign)
        self.assertEqual((2, 2), text.dxf.insert)
        self.assertEqual((4, 2), text.dxf.align_point)

    def test_get_alignment(self):
        text = self.layout.add_text('text')
        text.dxf.halign = 1
        text.dxf.valign = 3
        self.assertEqual('TOP_CENTER', text.get_align())


if __name__ == '__main__':
    unittest.main()