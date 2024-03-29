#!/usr/bin/env python3
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: create new drawings for all supported DXF versions and create new
# graphic entities  - check if AutoCAD accepts the new created data structures.
# Created: 25.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License

import ezdxf
from ezdxf.const import versions_supported_by_new

def add_line_entities(entityspace, offset):
    for color in range(1, 256):
        line = entityspace.add_line((offset+0, color), (offset+50, color), {'color': color})


def make_drawing(version):
    dwg = ezdxf.new(version)
    add_line_entities(dwg.modelspace(), 0)
    add_line_entities(dwg.layout(), 70)
    dwg.saveas('basic_graphics_%s.dxf' % version)


def main():
    for version in versions_supported_by_new:
        make_drawing(version)

if __name__ == '__main__':
    main()
