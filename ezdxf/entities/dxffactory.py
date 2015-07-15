from ezdxf import DXFVersionError
from ezdxf.const import unsupported_dxf_versions, acadrelease
from ezdxf.entities.legacy import LegacyDXFFactory
from ezdxf.entities.modern import ModernDXFFactory


def get_dxffactory(drawing):
    dxfversion = drawing.dxfversion
    if dxfversion in unsupported_dxf_versions:
        acad_version = acadrelease.get(dxfversion, "unknown")
        raise DXFVersionError("DXF Version {} (AutoCAD Release: {}) not supported.".format(dxfversion, acad_version))
    factory_class = LegacyDXFFactory if dxfversion <= 'AC1009' else ModernDXFFactory
    return factory_class(drawing)