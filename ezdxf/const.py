#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: constant values
# Created: 10.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

acadrelease = {
    'AC1009': 'R12',
    'AC1012': 'R13',
    'AC1014': 'R14',
    'AC1015': 'R2000',
    'AC1018': 'R2004',
    'AC1021': 'R2007',
    'AC1024': 'R2010',
}

dxfversion = {
    acad: dxf for dxf, acad in acadrelease.items()
}

# Entity: Polyline, Polymesh
# 70 flags
POLYLINE_CLOSED = 1
POLYLINE_MESH_CLOSED_M_DIRECTION = POLYLINE_CLOSED
POLYLINE_CURVE_FIT_VERTICES_ADDED = 2
POLYLINE_SPLINE_FIT_VERTICES_ADDED = 4
POLYLINE_3D_POLYLINE = 8
POLYLINE_3D_POLYMESH = 16
POLYLINE_MESH_CLOSED_N_DIRECTION = 32
POLYLINE_POLYFACE = 64
POLYLINE_GENERATE_LINETYPE_PATTERN =128

# Entity: Polymesh
# 75 surface smooth type
POLYMESH_NO_SMOOTH = 0
POLYMESH_QUADRIC_BSPLINE = 5
POLYMESH_CUBIC_BSPLINE = 6
POLYMESH_BEZIER_SURFACE = 8

#Entity: Vertex
# 70 flags
VTX_EXTRA_VERTEX_CREATED = 1 ## Extra vertex created by curve-fitting
VTX_CURVE_FIT_TANGENT = 2    ## Curve-fit tangent defined for this vertex.
## A curve-fit tangent direction of 0 may be omitted from the DXF output, but is
## significant if this bit is set.
## 4 = unused, never set in dxf files
VTX_SPLINE_VERTEX_CREATED = 8 ##Spline vertex created by spline-fitting
VTX_SPLINE_FRAME_CONTROL_POINT = 16
VTX_3D_POLYLINE_VERTEX = 32
VTX_3D_POLYGON_MESH_VERTEX = 64
VTX_3D_POLYFACE_MESH_VERTEX = 128

VERTEX_FLAGS = {
    'polyline2d': 0,
    'polyline3d': VTX_3D_POLYLINE_VERTEX,
    'polymesh': VTX_3D_POLYGON_MESH_VERTEX,
    'polyface': VTX_3D_POLYGON_MESH_VERTEX | VTX_3D_POLYFACE_MESH_VERTEX,
}
POLYLINE_FLAGS = {
    'polyline2d': 0,
    'polyline3d': POLYLINE_3D_POLYLINE,
    'polymesh': POLYLINE_3D_POLYMESH,
    'polyface': POLYLINE_POLYFACE,
}
