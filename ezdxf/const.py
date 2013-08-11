# Purpose: constant values
# Created: 10.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

acadrelease = {
    'AC1009': 'R12',
    'AC1012': 'R13',
    'AC1014': 'R14',
    'AC1015': 'R2000',
    'AC1018': 'R2004',
    'AC1021': 'R2007',
    'AC1024': 'R2010',
    'AC1027': 'R2013',
}

versions_supported_by_new = ['AC1009', 'AC1015', 'AC1018', 'AC1021', 'AC1024', 'AC1027']

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
POLYLINE_GENERATE_LINETYPE_PATTERN = 128

# Entity: Polymesh
# 75 surface smooth type
POLYMESH_NO_SMOOTH = 0
POLYMESH_QUADRIC_BSPLINE = 5
POLYMESH_CUBIC_BSPLINE = 6
POLYMESH_BEZIER_SURFACE = 8

# Entity: Vertex
# 70 flags
VERTEXNAMES = ('vtx0', 'vtx1', 'vtx2', 'vtx3')
VTX_EXTRA_VERTEX_CREATED = 1  # Extra vertex created by curve-fitting
VTX_CURVE_FIT_TANGENT = 2  # Curve-fit tangent defined for this vertex.
# A curve-fit tangent direction of 0 may be omitted from the DXF output, but is
# significant if this bit is set.
# 4 = unused, never set in dxf files
VTX_SPLINE_VERTEX_CREATED = 8  # Spline vertex created by spline-fitting
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

# block-type flags (bit coded values, may be combined):
# Entity: BLOCK
# 70 flags

# This is an anonymous block generated by hatching, associative dimensioning, other internal operations, or an
# application
BLK_ANONYMOUS = 1

# This block has non-constant attribute definitions (this bit is not set if the block has any attribute definitions that
# are constant, or has no attribute definitions at all)
BLK_NON_CONSTANT_ATTRIBUTES = 2

BLK_XREF = 4  # This block is an external reference (xref)
BLK_XREF_OVERLAY = 8  # This block is an xref overlay
BLK_EXTERNAL = 16  # This block is externally dependent
BLK_RESOLVED = 32  # This is a resolved external reference, or dependent of an external reference (ignored on input)
BLK_REFERENCED = 64  # This definition is a referenced external reference (ignored on input)

LWPOLYLINE_CLOSED = 1
LWPOLYLINE_PLINEGEN = 128

TEXT_ALIGN_FLAGS = {
    'LEFT' : (0, 0),
    'CENTER' : (1, 0),
    'RIGHT' : (2, 0),
    'ALIGNED' : (3, 0),
    'MIDDLE' : (4, 0),
    'FIT' : (5, 0),
    'BOTTOM_LEFT' : (0, 1),
    'BOTTOM_CENTER' : (1, 1),
    'BOTTOM_RIGHT' : (2, 1),
    'MIDDLE_LEFT' : (0, 2),
    'MIDDLE_CENTER' : (1, 2),
    'MIDDLE_RIGHT' : (2, 2),
    'TOP_LEFT' : (0, 3),
    'TOP_CENTER' : (1, 3),
    'TOP_RIGHT' : (2, 3),
}
TEXT_ALIGNMENT_BY_FLAGS = dict( (flags, name) for name, flags in TEXT_ALIGN_FLAGS.items() )

MTEXT_ALIGN_FLAGS = {
    'TOP_LEFT' : 1,
    'TOP_CENTER' : 2,
    'TOP_RIGHT' : 3,
    'MIDDLE_LEFT' : 4,
    'MIDDLE_CENTER' : 5,
    'MIDDLE_RIGHT' : 6,
    'BOTTOM_LEFT' : 7,
    'BOTTOM_CENTER' : 8,
    'BOTTOM_RIGHT' : 9,
}
MTEXT_ALIGNMENT_BY_FLAGS = dict( (flags, name) for name, flags in MTEXT_ALIGN_FLAGS.items() )

MTEXT_LEFT_TO_RIGHT = 1
MTEXT_TOP_TO_BOTTOM = 3
MTEXT_BY_STYLE = 5
MTEXT_AT_LEAST = 1
MTEXT_EXACT = 2

MTEXT_WRITE_DIRECTION_FLAGS = {
    'LEFT_TO_RIGHT': MTEXT_LEFT_TO_RIGHT,
    'TOP_TO_BOTTOM': MTEXT_TOP_TO_BOTTOM,
    'BY_STYLE': MTEXT_BY_STYLE,
}
MTEXT_WRITE_DIRECTION_BY_FLAGS = dict( (flags, name) for name, flags in MTEXT_WRITE_DIRECTION_FLAGS.items() )