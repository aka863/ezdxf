# Purpose: dxf-factory-factory
# Created: 11.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: MIT License
from __future__ import unicode_literals
__author__ = "mozman <mozman@gmx.at>"

from .ac1009 import AC1009Factory
from .ac1015 import AC1015Factory
from .ac1018 import AC1018Factory
from .ac1021 import AC1021Factory
from .ac1024 import AC1024Factory
from .ac1027 import AC1027Factory

default_factory = AC1009Factory

factories = {
    'AC1009': default_factory,  # R11/12
    'AC1012': AC1015Factory,  # R13 - experimental
    'AC1014': AC1015Factory,  # R14 - experimental
    'AC1015': AC1015Factory,  # R2000
    'AC1018': AC1018Factory,  # R2004
    'AC1021': AC1021Factory,  # R2007
    'AC1024': AC1024Factory,  # R2010
    'AC1027': AC1027Factory,  # R2013
}


def dxffactory(dxfversion, drawing=None):
    factory_class = factories.get(dxfversion, default_factory)
    factory = factory_class()
    factory.drawing = drawing
    return factory


