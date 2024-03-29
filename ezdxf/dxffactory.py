# Purpose: dxf-factory-factory
# Created: 11.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .legacy import LegacyDXFFactory
from .modern import ModernDXFFactory
from .const import acadrelease, DXFVersionError, unsupported_dxf_versions


def dxffactory(drawing):
    dxfversion = drawing.dxfversion
    if dxfversion in unsupported_dxf_versions:
        acad_version = acadrelease.get(dxfversion, "unknown")
        raise DXFVersionError("DXF Version {} (AutoCAD Release: {}) not supported.".format(dxfversion, acad_version))
    factory_class = LegacyDXFFactory if dxfversion <= 'AC1009' else ModernDXFFactory
    return factory_class(drawing)



