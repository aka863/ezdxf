#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test basic graphic entities
# Created: 25.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import sys
import unittest

from ezdxf.handle import HandleGenerator
from ezdxf.dxffactory import dxffactory
from ezdxf.entityspace import EntitySpace


class DrawingProxy:
    def __init__(self, version):
        self.handles = HandleGenerator()
        self.entitydb = {}
        self.dxffactory = dxffactory(version, self)

from ezdxf.ac1009.layouts import AC1009ModelSpaceLayout, AC1009PaperSpaceLayout

class SetupDrawing(unittest.TestCase):
    def setUp(self):
        self.dwg = DrawingProxy('AC1009')
        self.workspace = EntitySpace(self.dwg)
        self.layout = AC1009ModelSpaceLayout(self.workspace, self.dwg.dxffactory)

class TestPaperSpace(SetupDrawing):
    def test_paper_space(self):
        paperspace = AC1009PaperSpaceLayout(self.workspace, self.dwg.dxffactory)
        line = paperspace.add_line((0, 0), (1, 1))
        self.assertEqual(1, line.paperspace)

class TestLine(SetupDrawing):
    def test_create_line(self):
        line = self.layout.add_line((0, 0), (1, 1))
        self.assertEqual((0.,0.), line.start)
        self.assertEqual((1.,1.), line.end)

if __name__=='__main__':
    unittest.main()