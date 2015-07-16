import os
from random import random
import unittest
import math
import ezdxf.drawing
import ezdxf.const


def run_versions(*versions):
    def wrapper(func):
        def run(testcase):
            for version in versions:
                func(version)
        return run

    return wrapper


def run_with_versions(*versions):
    def wrapper(func):
        def run(testcase):
            for version in versions:
                filename = "{}_{}.dxf".format(func.__name__, version)
                dwg = ezdxf.new(version)
                func(testcase, dwg)
                dwg.saveas(os.path.join("files", filename))

        return run
    return wrapper

modern = ezdxf.const.versions_supported_by_new

class TestIntegration(unittest.TestCase):
    polyline_3d = [(323380.91750022338, 5184999.7255775109, 0.0),
                      (323377.13033454702, 5184994.8609992303, 0.0),
                      (323375.96284645743, 5184992.1182727059, 0.0),
                      (323374.72169714782, 5184989.8344467692, 0.0),
                      (323374.17676884111, 5184988.5392300664, 0.0),
                      (323373.39893951337, 5184986.7871434148, 0.0),
                      (323372.92717616714, 5184984.9566230336, 0.0),
                      (323372.37727835565, 5184982.897411068, 0.0),
                      (323371.90899244603, 5184981.601685036, 0.0),
                      (323375.99291780719, 5184981.3014478451, 0.0),
                      (323375.99841245974, 5184977.7365302956, 0.0),
                      (323377.32736607571, 5184977.6150565967, 0.0),
                      (323377.76792070246, 5184970.3801041171, 0.0),
                      (323378.56378788338, 5184967.413698026, 0.0),
                      (323379.38490772923, 5184964.9500029553, 0.0)]
    polyline_2d = [(0,0), (1,0), (1,1), (0,1), (0,0), (1,1), (.5, 1.5), (0, 1), (1,0)]
    def setUp(self):
        pass

    @run_with_versions(*modern)
    def test_anonymous_blocks(self, dwg):
        modelspace = dwg.modelspace()
        anonymous_block = dwg.blocks.new_anonymous_block()
        points2d = [(0,0), (1,0), (1,1), (0,1), (0,0), (1,1), (.5, 1.5), (0, 1), (1,0)]
        anonymous_block.add_polyline2d(points2d)
        modelspace.add_blockref(anonymous_block.name, (0, 0))

    def test_entities_iterator_ac1009(self):
        drawing = ezdxf.new('AC1009')
        modelspace = drawing.modelspace()

        modelspace.add_polyline3d(self.polyline_3d)

        drawing.saveas('files/test.dxf')

        dxf = ezdxf.readfile('files/test.dxf')

        for entity in dxf.entities:
            if entity.dxftype() == 'POLYLINE':
                for pt1, pt2 in zip(entity.points(), self.polyline_3d):
                    self.assertAlmostEqual(pt1[0], pt2[0])
                    self.assertAlmostEqual(pt1[1], pt2[1])
                    self.assertAlmostEqual(pt1[2], pt2[2])

    def test_entities_iterator_ac1015(self):
        drawing = ezdxf.new('AC1015')
        modelspace = drawing.modelspace()

        modelspace.add_polyline3d(self.polyline_3d)

        drawing.saveas('files/test.dxf')

        dxf = ezdxf.readfile('files/test.dxf')

        for entity in dxf.entities:
            if entity.dxftype() == 'POLYLINE':
                for pt1, pt2 in zip(entity.points(), self.polyline_3d):
                    self.assertAlmostEqual(pt1[0], pt2[0])
                    self.assertAlmostEqual(pt1[1], pt2[1])
                    self.assertAlmostEqual(pt1[2], pt2[2])

    def test_import_blocks(self):
        source_dwg = ezdxf.readfile('files/CustomBlocks.dxf')
        target_dwg = ezdxf.new(source_dwg.dxfversion)
        importer = ezdxf.Importer(source_dwg, target_dwg)
        importer.import_blocks(query='CustomBlock1')
        importer.import_modelspace_entities()
        target_dwg.saveas("files/CustomBlocks_Import.dxf")

    @run_with_versions(*modern)
    def test_new_entities(self, dwg):
        def add_line_entities(entityspace, offset):
            for color in range(1, 256):
                line = entityspace.add_line((offset+0, color), (offset+50, color), {'color': color})

        add_line_entities(dwg.modelspace(), 0)
        add_line_entities(dwg.layout(), 70)

        # add table entities
        dwg.layers.create('MOZMAN-LAYER')
        dwg.styles.create('MOZMAN-STY')
        dwg.linetypes.create('MOZMAN-LTY', {'pattern': [1.0, .5, -.5]})
        dwg.dimstyles.create('MOZMAN-DIMSTY')
        dwg.views.create('MOZMAN-VIEW')
        dwg.viewports.create('MOZMAN-VPORT')
        dwg.ucs.create('MOZMAN-UCS')
        dwg.appids.create('MOZMANAPP')


    FILE_1 = r"D:\Source\dxftest\ChineseChars_cp936_R2004.dxf"
    FILE_2 = r'D:\Source\dxftest\ChineseChars_utf8_R2004.dxf'
    FILE_3 = r"D:\Source\dxftest\ChineseChars_cp936_R2004.zip"
    FILE_4 = r"D:\Source\dxftest\ProE_AC1018.dxf"

    @unittest.skipIf(not os.path.exists(FILE_1), reason=None)
    def test_file1(self):
        self.read_plain_file(self.FILE_1)

    @unittest.skipIf(not os.path.exists(FILE_2), reason=None)
    def test_file2(self):
        self.read_plain_file(self.FILE_2)

    @unittest.skipIf(not os.path.exists(FILE_3), reason=None)
    def test_file3(self):
        dwg = ezdxf.readzip(self.FILE_3)
        stats = [dwg.filename, dwg.dxfversion, dwg.encoding]


    @unittest.skipIf(not os.path.exists(FILE_3), reason=None)
    def test_file4(self):
        self.read_plain_file(self.FILE_3)

    def read_plain_file(self, filename):
            #print("Open DXF file: '{}'".format(filename))
            dwg = ezdxf.readfile(filename)
            return [dwg.filename, dwg.dxfversion, dwg.encoding]



    @run_with_versions("AC1015", "AC1009")
    def test_cube(self, dwg):

        def build_cube(layout, basepoint, length):
            def scale(point):
                return ((basepoint[0]+point[0]*length),
                        (basepoint[1]+point[1]*length),
                        (basepoint[2]+point[2]*length))

            # cube corner points
            p1 = scale((0, 0, 0))
            p2 = scale((0, 0, 1))
            p3 = scale((0, 1, 0))
            p4 = scale((0, 1, 1))
            p5 = scale((1, 0, 0))
            p6 = scale((1, 0, 1))
            p7 = scale((1, 1, 0))
            p8 = scale((1, 1, 1))

            # define the 6 cube faces
            # look into -x direction
            # Every add_face adds 4 vertices 6x4 = 24 vertices
            pface = layout.add_polyface()
            pface.append_face([p1, p5, p7, p3], {'color': 1})  # base
            pface.append_face([p1, p5, p6, p2], {'color': 2})  # left
            pface.append_face([p5, p7, p8, p6], {'color': 3})  # front
            pface.append_face([p7, p8, p4, p3], {'color': 4})  # right
            pface.append_face([p1, p3, p4, p2], {'color': 5})  # back
            pface.append_face([p2, p6, p8, p4], {'color': 6})  # top


        def build_all_cubes(layout):
            for x in range(10):
                for y in range(10):
                    build_cube(layout, basepoint=(x, y, random()), length=random())

        layout = dwg.modelspace()
        build_all_cubes(layout)

    @run_with_versions(*modern)
    def test_polylines(self, dwg):
        dwg.modelspace().add_polyline2d(self.polyline_2d)
        points3d = [(3, 3, 0), (6, 3, 1), (6, 6, 2), (3, 6, 3), (3, 3, 4)]
        dwg.modelspace().add_polyline3d(points3d)

    @run_with_versions("AC1009", "AC1015")
    def test_mesh(self, dwg):
        layout = dwg.modelspace()

        def build_mesh(polymesh):

            m_size = polymesh.dxf.m_count
            n_size = polymesh.dxf.n_count
            m_delta = math.pi / m_size
            n_delta = math.pi / n_size

            for x in range(m_size):
                sinx = math.sin(float(x)*m_delta)
                for y in range(n_size):
                    cosy = math.cos(float(y)*n_delta)
                    z = sinx * cosy * HEIGHT
                    # set the m,n vertex to 3d point x,y,z
                    polymesh.set_mesh_vertex(pos=(x, y), point=(x, y, z))


        MSIZE = 20
        HEIGHT = 3.
        polymesh = layout.add_polymesh(size=(MSIZE, MSIZE))
        build_mesh(polymesh)

    @run_with_versions(*modern)
    def test_rotated_block_attr(self, dwg):
        # first create a block
        flag = dwg.blocks.new(name='FLAG')

        # add dxf entities to the block (the flag)
        # use basepoint = (x, y) to define an other basepoint than (0, 0)
        flag_symbol = [(0, 0), (0, 5), (4, 3), (0, 3)]
        flag.add_polyline2d(flag_symbol)
        flag.add_circle((0, 0), .4, dxfattribs={'color': 2})

        # define some attributes
        flag.add_attdef('NAME', (0.5, -0.5), {'height': 0.5, 'color': 3})
        flag.add_attdef('XPOS', (0.5, -1.0), {'height': 0.25, 'color': 4})
        flag.add_attdef('YPOS', (0.5, -1.5), {'height': 0.25, 'color': 4})

        # insert block
        layout = dwg.modelspace()
        point = (10, 12)
        values = {
            'NAME': "REFNAME",
            'XPOS': "x = %.3f" % point[0],
            'YPOS': "y = %.3f" % point[1]
        }
        scale = 1.75
        layout.add_auto_blockref('FLAG', point, values, dxfattribs={
            'xscale': scale,
            'yscale': scale,
            'layer': 'FLAGS',
            'rotation': -15
        })

