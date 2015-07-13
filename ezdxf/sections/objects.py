from ezdxf.sections.entity import ClassesSection


class ObjectsSection(ClassesSection):
    name = 'objects'

    def roothandle(self):
        return self._entity_space[0]