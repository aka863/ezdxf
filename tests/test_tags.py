#!/usr/bin/env python
#coding:utf-8
# Author:  mozman -- <mozman@gmx.at>
# Purpose: test tagreader
# Created: 10.03.2011
# Copyright (C) 2011, Manfred Moitzi
# License: GPLv3

import sys
import unittest
from io import StringIO

from ezdxf.tags import StringIterator, Tags
from ezdxf.tags import dxfinfo, strtag

TEST_TAGREADER = """  0
SECTION
  2
HEADER
  9
$ACADVER
  1
AC1018
  9
$DWGCODEPAGE
  3
ANSI_1252
  0
ENDSEC
  0
EOF
"""

TEST_NO_EOF = """  0
SECTION
  2
HEADER
  9
$ACADVER
  1
AC1018
  9
$DWGCODEPAGE
  3
ANSI_1252
  0
ENDSEC

"""

class TestTagReader(unittest.TestCase):
    def setUp(self):
        self.reader = StringIterator(TEST_TAGREADER)

    def test_next(self):
        self.assertEqual((0, 'SECTION'), next(self.reader))

    def test_undo_last(self):
        self.reader.__next__()
        self.reader.undotag()
        self.assertEqual((0, 'SECTION'), next(self.reader))

    def test_error_on_multiple_undo_last(self):
        next(self.reader)
        self.reader.undotag()
        with self.assertRaises(ValueError):
            self.reader.undotag()

    def test_error_undo_last_before_first_read(self):
        with self.assertRaises(ValueError):
            self.reader.undotag()

    def test_lineno(self):
        next(self.reader)
        self.assertEqual(2, self.reader.lineno)

    def test_lineno_with_undo(self):
        next(self.reader)
        self.reader.undotag()
        self.assertEqual(0, self.reader.lineno)

    def test_lineno_with_undo_next(self):
        next(self.reader)
        self.reader.undotag()
        next(self.reader)
        self.assertEqual(2, self.reader.lineno)

    def test_to_list(self):
        tags = list(self.reader)
        self.assertEqual(8, len(tags))

    def test_undo_eof(self):
        for tag in self.reader:
            if tag == (0, 'EOF'):
                self.reader.undotag()
                break
        tag = next(self.reader)
        self.assertEqual((0, 'EOF'), tag)
        with self.assertRaises(StopIteration):
            self.reader.__next__()

    def test_no_eof(self):
        tags = list(StringIterator(TEST_NO_EOF))
        self.assertEqual(7, len(tags))
        self.assertEqual((0, 'ENDSEC'), tags[-1])

    def test_strtag_int(self):
        self.assertEqual('  1\n1\n', strtag( (1,1) ))

    def test_strtag_float(self):
        self.assertEqual(' 10\n3.1415\n', strtag( (10, 3.1415) ))

    def test_strtag_str(self):
        self.assertEqual('  0\nSECTION\n', strtag( (0, 'SECTION') ))

class TestGetDXFInfo(unittest.TestCase):
    def test_dxfinfo(self):
        info = dxfinfo(StringIO(TEST_TAGREADER))
        self.assertEqual(info.release, 'R2004')
        self.assertEqual(info.encoding, 'cp1252')

TESTHANDLE5 = """ 0
TEST
  5
F5
"""

TESTHANDLE105 = """ 0
TEST
105
F105
"""

TESTFINDALL = """  0
TEST0
  0
TEST1
  0
TEST2
"""

class HandlesMock:
    calls = 0
    @property
    def next(self):
        self.calls = self.calls + 1
        return 'FF'

class TestTags(unittest.TestCase):
    def setUp(self):
        self.tags = Tags.fromtext(TEST_TAGREADER)

    def test_from_text(self):
        self.assertEqual(8, len(self.tags))

    def test_write(self):
        stream = StringIO()
        self.tags.write(stream)
        result = stream.getvalue()
        stream.close()
        self.assertEqual(TEST_TAGREADER, result)

    def test_settag(self):
        self.tags.settag(2, 'XHEADER')
        self.assertEqual('XHEADER', self.tags[1].value)

    def test_gethandle_5(self):
        tags = Tags.fromtext(TESTHANDLE5)
        handles = HandlesMock()
        self.assertEqual('F5', tags.gethandle(handles))
        self.assertEqual(0, handles.calls)

    def test_gethandle_105(self):
        tags = Tags.fromtext(TESTHANDLE105)
        handles = HandlesMock()
        self.assertEqual('F105', tags.gethandle(handles))
        self.assertEqual(0, handles.calls)

    def test_gethandle_create_new(self):
        handles = HandlesMock()
        self.assertEqual('FF', self.tags.gethandle(handles))
        self.assertEqual(1, handles.calls)

    def test_findall(self):
        tags = Tags.fromtext(TESTFINDALL)
        self.assertEqual(3, len(tags.findall(0)))

    def test_findfirst(self):
        tags = Tags.fromtext(TESTFINDALL)
        index = tags.findfirst(0)
        self.assertEqual(0, index)
        index = tags.findnext(0, index+1)
        self.assertEqual(1, index)

    def test_findfirst_value_error(self):
        tags = Tags.fromtext(TESTFINDALL)
        with self.assertRaises(ValueError):
            tags.findfirst(1)


if __name__=='__main__':
    unittest.main()