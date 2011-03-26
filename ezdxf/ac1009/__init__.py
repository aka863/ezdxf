#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: dxf factory for R12/AC1009
# Created: 11.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

"""
File Sections
=============

The DXF file is subdivided into four editable sections, plus the END
OF FILE marker. File separator groups are used to delimit these file
sections. The following is an example of a void DXF file with only
the section markers and table headers present:

   0            (Begin HEADER section)
  SECTION
   2
  HEADER
               <<<<Header variable items go here>>>>
  0
  ENDSEC       (End HEADER section)
   0           (Begin TABLES section)
  SECTION
   2
  TABLES
   0
  TABLE
   2
  VPORT
   70
  (viewport table maximum item count)
               <<<<viewport table items go here>>>>
  0
  ENDTAB
  0
  TABLE
  2
  APPID, DIMSTYLE, LTYPE, LAYER, STYLE, UCS, VIEW, or VPORT
  70
  (Table maximum item count)
               <<<<Table items go here>>>>
  0
  ENDTAB
  0
  ENDSEC       (End TABLES section)
  0            (Begin BLOCKS section)
  SECTION
  2
  BLOCKS
               <<<<Block definition entities go here>>>>
  0
  ENDSEC       (End BLOCKS section)
  0            (Begin ENTITIES section)
  SECTION
  2
  ENTITIES
               <<<<Drawing entities go here>>>>
  0
  ENDSEC       (End ENTITIES section)
  0
  EOF          (End of file)

"""

from ..tags import Tags

from .headervars import VARMAP
from .tableentries import AC1009Layer, AC1009DimStyle, AC1009AppID, AC1009Style
from .tableentries import AC1009Linetype, AC1009View, AC1009Viewport, AC1009UCS
from .graphics import AC1009Line

from ..dxfobjects import DXFDictionary, DXFLayout
from .layouts import AC1009Layouts
from ..entity import GenericWrapper

ENTITY_WRAPPERS =  {
    # tables entries
    'LAYER': AC1009Layer,
    'DIMSTYLE': AC1009DimStyle,
    'LTYPE': AC1009Linetype,
    'APPID': AC1009AppID,
    'STYLE': AC1009Style,
    'UCS': AC1009UCS,
    'VIEW': AC1009View,
    'VPORT': AC1009Viewport,
    # dxf objects
    'DICTIONARY': DXFDictionary,
    'LAYOUT': DXFLayout,
    # dxf entities
    'LINE': AC1009Line,
}

class AC1009Factory:
    HEADERVARS = dict(VARMAP)
    def __init__(self):
        self.ENTITY_WRAPPERS = dict(ENTITY_WRAPPERS)
        self.drawing = None

    def new_header_var(self, key, value):
        factory = self.HEADERVARS[key]
        return factory(value)

    def new_entity(self, type_, handle, attribs):
        """ Create a new entity.

        :returns: wrapper class
        """
        try:
            class_ = self.ENTITY_WRAPPERS[type_]
            return class_.new(handle, attribs, self)
        except KeyError:
            raise ValueError('Unsupported entity type: %s' % type_)

    def wrap_entity(self, tags):
        """ :returns: wrapper class """
        type_ = tags[0].value
        wrapper = self.ENTITY_WRAPPERS.get(type_, GenericWrapper)
        return wrapper(tags)

    def create_db_entry(self, type_, attribs):
        """ Create new entity and add to drawing-database.

        :returns: wrapper class
        """
        handle = self.drawing.handles.next
        dbentry = self.new_entity(type_, handle, attribs)
        self.drawing.entitydb[handle] = dbentry.tags
        return dbentry

    def get_layouts(self):
        return AC1009Layouts(self.drawing)

    def table_wrapper(self, table):
        return TableWrapper(table)

class TableWrapper:
    """
    Encapsulate all DXF-Version specific details for all DXF tables.

    Tables are: LTYPE, LAYER, STYLE, ... in the TABLES section

    """
    def __init__(self, table):
        self. _table = table

    @property
    def name(self):
        return self._table.name

    def set_count(self, count):
        self._table._table_header.update(70, count)

